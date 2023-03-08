from typing import Any, TypeVar

from .contour import Contour
from .drawing import Drawing, LineDrawing, CubicDrawing
from .bitmap import Bitmap
from .svg import SvgDocument
from .tracing import Tracing
from .unification import unify_glyphs
from .approximation import Approximation


TContour = TypeVar('TContour', bound=Contour)

def trace(
        input_bitmap_file: str,
        output_svg_file: str,
        tracing: Tracing,
        approximation: Approximation[TContour],
        scale: float=1.0
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
    traced = unify_glyphs(traced, 3)
    approximated = approximation.approximate_drawing(traced)
    
    svg = SvgDocument(bitmap.width, bitmap.height)
    
    _add_drawing(svg, approximated, scale)
    
    svg.save(output_svg_file)


def _add_drawing(
        svg: SvgDocument,
        drawing: Drawing[TContour],
        scale: float
) -> None:
    match drawing:
        case LineDrawing():
            svg.add_line_drawing(drawing, scale)
        case CubicDrawing():
            svg.add_cubic_drawing(drawing, scale)
        case _:
            raise TypeError('Unsupported drawing type.')
