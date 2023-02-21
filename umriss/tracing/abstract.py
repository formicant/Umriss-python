from abc import ABC, abstractmethod
from typing import Iterable

from umriss.bitmap import Bitmap, GrayPixels
from umriss.contour import LineContour
from umriss.drawing import Glyph, LineDrawing


class Tracing(ABC):
    """
    Abstract base class for bitmap tracing algorithms.
    """
    def trace_bitmap(self, bitmap: Bitmap) -> LineDrawing:
        return LineDrawing(
            bitmap.width,
            bitmap.height,
            list(self.get_glyphs(bitmap.pixels))
        )
    
    @abstractmethod
    def get_glyphs(self, pixels: GrayPixels) -> Iterable[Glyph[LineContour]]:
        pass
