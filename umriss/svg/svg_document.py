from typing import Any, Callable, TypeVar
from umriss.contour import LineContour

from umriss.contour import Contour, CubicContour
from umriss.drawing import Drawing, LineDrawing, CubicDrawing
from umriss.glyph import GlyphInstance, GlyphReference
from .debug_colors import get_debug_color
from .element import Element
from .path_data import PathData


class SvgDocument:
    """
    Generates a simple SVG document with some groups of paths inside.
    
    Create an `SvgDocument`, add some drawings, then, `render` or `save` it.
    Drawings can be linear, quadratic, or cubic.
    All the coordinates are rounded to the specified number of `decimals`.
    """
    
    def __init__(self, width: float=0, height: float=0, is_shared=False, decimals: int=2):
        self.is_shared = is_shared
        self.decimals = decimals
        if is_shared:
            self.svg = Element('svg', xmlns=_xmlns)
        else:
            self.svg = Element('svg', width=width, height=height, xmlns=_xmlns, xmlns__x=_xmlns_x)
    
    
    def render(self) -> str:
        return _xml_declaration + self.svg.render()
    
    
    def save(self, filename: str) -> None:
        with open(filename, 'w') as file:
            file.write(self.render())
    
    
    def add_line_drawing(self, drawing: LineDrawing, scale: float=1.0) -> None:
        self._add_drawing(self._add_line_contour, drawing, scale)
    
    
    def add_cubic_drawing(self, drawing: CubicDrawing, scale: float=1.0) -> None:
        self._add_drawing(self._add_cubic_contour, drawing, scale)
    
    
    _TContour = TypeVar('_TContour', bound=Contour)
    
    def _add_drawing(self,
            add_contour: Callable[[PathData, _TContour, float], None],
            drawing: Drawing[Any],
            scale: float,
    ) -> None:
        attributes = dict()
        if scale != 1.0:
            attributes['transform'] = f'scale({1 / scale})'
        
        if len(drawing.referenced_glyphs) > 0:
            defs = Element('defs')
            for index, glyph in enumerate(drawing.referenced_glyphs):
                path_data = PathData(self.decimals)
                for contour in glyph.contours:
                    add_contour(path_data, contour, scale)
                defs.add_child(Element('path',
                    id=f's{index}' if self.is_shared else f'r{index}',
                    d=path_data,
                    fill='gray' if self.is_shared else get_debug_color(index)  # for debugging purposes
                ))
            self.svg.add_child(defs)
        
        if self.is_shared:
            return
        
        group = Element('g', **attributes)
        for occurrence in drawing.glyph_occurrences:
            match occurrence:
                case GlyphInstance():
                    path_data = PathData(self.decimals)
                    for contour in occurrence.glyph.contours:
                        add_contour(path_data, contour.offset(occurrence.position), scale)
                    group.add_child(Element('path', d=path_data))
                case GlyphReference():
                    href = f'_.svg#s{occurrence.index}' if occurrence.is_shared else f'#r{occurrence.index}'
                    group.add_child(Element('use',
                        x__href=href,
                        x=self._format_value(occurrence.position[0]),
                        y=self._format_value(occurrence.position[1])
                    ))
                case _:
                    raise TypeError('Unsupported glyph occurrence type')
        
        self.svg.add_child(group)
    
    
    def _add_line_contour(self, path_data: PathData, contour: LineContour, scale: float) -> None:
        points = contour.points if scale == 1.0 else scale * contour.points
        
        start_point = points[0]
        path_data.add_move_node(start_point)
        
        for point in points[1:]:
            path_data.add_line_node(point)
        
        path_data.add_close_node()
    
    
    def _add_cubic_contour(self, path_data: PathData, contour: CubicContour, scale: float) -> None:
        nodes = contour.nodes if scale == 1.0 else scale * contour.nodes
        
        [_, _, end_point] = nodes[-1]
        path_data.add_move_node(end_point)
        
        for node in nodes:
            path_data.add_cubic_node(node)
        
        path_data.add_close_node()
    
    
    def _format_value(self, value: float) -> str:
        formatted = '{:.{d}f}'.format(value, d=self.decimals)
        if self.decimals > 0:
            return formatted.rstrip('0').rstrip('.')
        else:
            return formatted


_xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>\n'

_xmlns = "http://www.w3.org/2000/svg"
_xmlns_x = "http://www.w3.org/1999/xlink"
