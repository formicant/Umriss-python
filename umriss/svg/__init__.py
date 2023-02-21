from typing import Any, Callable, TypeVar
from umriss.contour import LineContour

from umriss.contour import Contour, CubicContour
from umriss.drawing import Drawing, LineDrawing, CubicDrawing
from .group import Group
from .path import Path


class SvgDocument:
    """
    Generates a simple SVG document with some groups of paths inside.
    
    Create an `SvgDocument`, add some drawings, then, `render` or `save` it.
    Drawings can be linear, quadratic, or cubic.
    All the coordinates are rounded to the specified number of `decimals`.
    """
    
    def __init__(self, width: float, height: float, decimals: int=2):
        self.width = width
        self.height = height
        self.decimals = decimals
        
        self.groups: list[Group] = []
    
    
    def render(self) -> str:
        groups = (group.render() for group in self.groups)
        return _svg_template.format(
            width=self.width,
            height=self.height,
            groups='\n '.join(groups)
        )
    
    
    def save(self, filename: str) -> None:
        with open(filename, 'w') as file:
            file.write(self.render())
    
    
    def add_line_drawing(self, drawing: LineDrawing, scale: float=1.0, **attributes: Any) -> None:
        self._add_drawing(self._add_line_contour, drawing, scale, attributes)
    
    
    def add_cubic_drawing(self, drawing: CubicDrawing, scale: float=1.0, **attributes: Any) -> None:
        self._add_drawing(self._add_cubic_contour, drawing, scale, attributes)
    
    
    _TContour = TypeVar('_TContour', bound=Contour)
    
    def _add_drawing(self,
            add_contour: Callable[[Path, _TContour, float], None],
            drawing: Drawing[Any],
            scale: float,
            attributes: dict[str, Any]
    ) -> None:
        if scale != 1.0:
            attributes['transform'] = f'scale({1 / scale})'
        
        group = Group(attributes, self.decimals)
        
        for glyph in drawing.glyphs:
            path = Path(self.decimals)
            for contour in glyph.contours:
                add_contour(path, contour, scale)
            group.add_path(path)
        
        self.groups.append(group)
    
    
    def _add_line_contour(self, path: Path, contour: LineContour, scale: float) -> None:
        points = contour.points if scale == 1.0 else scale * contour.points
        
        start_point = points[0]
        path.add_move_node(start_point)
        
        for point in points[1:]:
            path.add_line_node(point)
        
        path.add_close_node()
    
    
    def _add_cubic_contour(self, path: Path, contour: CubicContour, scale: float) -> None:
        nodes = contour.nodes if scale == 1.0 else scale * contour.nodes
        
        [_, _, end_point] = nodes[-1]
        path.add_move_node(end_point)
        
        for node in nodes:
            path.add_cubic_node(node)
        
        path.add_close_node()


_svg_template = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
 {groups}
</svg>
'''
