from typing import TypeVar

from .contour import Contour
from .drawing import Drawing, LineDrawing, CubicDrawing
from .bitmap import Bitmap
from .svg import save_as_svg
from .tracing import Tracing
from .approximation import Approximation
from .unification import unify_identical_glyphs
from .document import LineDocument

TContour = TypeVar('TContour', bound=Contour)

def trace(
        input_bitmap_files: list[str],
        output_directory: str,
        tracing: Tracing,
        approximation: Approximation[TContour],
        scale: float=1.0
) -> None:
    """
    Traces the `input_bitmap_files` using the given `tracing` method,
    then, uses the given contour `approximation`,
    renders the result as SVG files, and saves them into `output_directory`.
    `scale` affects only the coordinates in paths (e.g. to make them integer),
    it is cancelled out by a group transform.
    """
    print('tracing')
    pages: list[LineDrawing] = []
    for file in input_bitmap_files:
        print(f'  {file}')
        bitmap = Bitmap(file)
        pages.append(tracing.trace_bitmap(bitmap))
    traced = LineDocument(pages)
    print('unifying glyphs')
    traced = unify_identical_glyphs(traced, use_shared=True)
    print('approximating')
    approximated = approximation.approximate_document(traced)
    print('saving')
    
    save_as_svg(approximated, output_directory, scale)
