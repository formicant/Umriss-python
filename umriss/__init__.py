from typing import Any, TypeVar

from .contour import Contour
from .drawing import Drawing, LineDrawing, CubicDrawing
from .bitmap import Bitmap
from .svg import SvgDocument
from .tracing import Tracing
from .approximation import Approximation


TContour = TypeVar('TContour', bound=Contour)

def trace(
        input_bitmap_file: str,
        output_svg_file: str,
        tracing: Tracing,
        approximation: Approximation[TContour],
        scale: float=1.0,
        debug_mode: bool=False
) -> None:
    """
    Traces the `input_bitmap_file` using the given `tracing` method,
    then, uses the given contour `approximation`,
    renders the result as an SVG document, and saves it as `output_svg_file`.
    `scale` affects only the coordinates in paths (e.g. to make them integer),
    it is cancelled out by a group transform.
    In `debug_mode`, the approximated contours are drawn as stroke over the exact ones.
    """
    bitmap = Bitmap(input_bitmap_file)
    traced = tracing.trace_bitmap(bitmap)
    approximated = approximation.approximate_drawing(traced)
    
    svg = SvgDocument(bitmap.width, bitmap.height)
    
    if debug_mode:
        _add_drawing(svg, traced, scale, opacity=0.1)
        _add_drawing(svg, approximated, scale, fill='none', stroke='blue', stroke_width=0.1)
    else:
        _add_drawing(svg, approximated, scale)
    
    svg.save(output_svg_file)


def _add_drawing(
        svg: SvgDocument,
        drawing: Drawing[TContour],
        scale: float,
        **attributes: Any
) -> None:
    match drawing:
        case LineDrawing():
            svg.add_line_drawing(drawing, scale, **attributes)
        case CubicDrawing():
            svg.add_cubic_drawing(drawing, scale, **attributes)
        case _:
            raise TypeError('Unsupported drawing type.')
