from typing import Any, Callable
from nptyping import NDArray, Shape, Number

from umriss.types import Contour, QuadraticContour, CubicContour
from umriss.drawing import Drawing, ExactDrawing, LineDrawing, QuadraticDrawing, CubicDrawing
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
    
    
    def add_line_drawing(self, drawing: LineDrawing | ExactDrawing, scale: float=1.0, **attributes: Any) -> None:
        self._add_drawing(self._add_line_contour, drawing, scale, attributes)
    
    
    def add_quadratic_drawing(self, drawing: QuadraticDrawing, scale: float=1.0, **attributes: Any) -> None:
        self._add_drawing(self._add_quadratic_contour, drawing, scale, attributes)
    
    
    def add_cubic_drawing(self, drawing: CubicDrawing, scale: float=1.0, **attributes: Any) -> None:
        self._add_drawing(self._add_cubic_contour, drawing, scale, attributes)


    def _add_drawing(self,
            add_contour: Callable[[Path, NDArray[Shape['*, ...'], Number]], None],
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
                if scale != 1.0:
                    contour = scale * contour;
                
                add_contour(path, contour)
            
            group.add_path(path)
        
        self.groups.append(group)
    
    
    def _add_line_contour(self, path: Path, contour: Contour) -> None:
        start_point = contour[0]
        path.add_move_node(start_point)
        for point in contour[1:]:
            path.add_line_node(point)
        path.add_close_node()
    
    
    def _add_quadratic_contour(self, path: Path, contour: QuadraticContour) -> None:
        [_, end_point] = contour[-1]
        path.add_move_node(end_point)
        for node in contour:
            path.add_quadratic_node(node)
        path.add_close_node()
    
    
    def _add_cubic_contour(self, path: Path, contour: CubicContour) -> None:
        [_, _, end_point] = contour[-1]
        path.add_move_node(end_point)
        for node in contour:
            path.add_cubic_node(node)
        path.add_close_node()


_svg_template = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
 {groups}
</svg>
'''
