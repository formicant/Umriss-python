from typing import Any, TypeVar

from .drawing import ExactDrawing, LineDrawing, QuadraticDrawing, CubicDrawing
from .image import Image
from .svg import SvgDocument
from .approximation import Approximation, Exact


TContour = TypeVar('TContour')

def trace(
        input_bitmap_file: str,
        output_svg_file: str,
        approximation: Approximation[TContour],
        scale: float=1.0,
        debug_mode: bool=False
) -> None:
    """
    Traces the `input_bitmap_file` into SVG and saves it as `output_svg_file`.
    A contour `approximation` is used if specified.
    `scale` affects only the coordinates in paths (e.g. to make them integer),
    it is cancelled out by a group transform.
    In `debug_mode`, the approximated contours are drawn as stroke over the exact ones.
    """
    image = Image(input_bitmap_file)
    svg = SvgDocument(image.width, image.height)
    
    if debug_mode:
        _add_drawing(svg, image.drawing, Exact(), 1.0, opacity=0.1)
        _add_drawing(svg, image.drawing, approximation, scale, fill='none', stroke='blue', stroke_width=0.1)
    else:
        _add_drawing(svg, image.drawing, approximation, scale)
    
    svg.save(output_svg_file)


def _add_drawing(
        svg: SvgDocument,
        drawing: ExactDrawing,
        approximation: Approximation[TContour],
        scale: float,
        **attributes: Any
) -> None:
    approximated_drawing = approximation.approximate_drawing(drawing)
    
    match approximated_drawing:
        case ExactDrawing() | LineDrawing():
            svg.add_line_drawing(approximated_drawing, scale, **attributes)
        case QuadraticDrawing():
            svg.add_quadratic_drawing(approximated_drawing, scale, **attributes)
        case CubicDrawing():
            svg.add_cubic_drawing(approximated_drawing, scale, **attributes)
        case _:
            raise TypeError('Unsupported drawing type.')
