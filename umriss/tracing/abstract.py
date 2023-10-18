from abc import ABC, abstractmethod
from typing import Iterable

from umriss.bitmap import Bitmap, GrayPixels
from umriss.contour import LineContour
from umriss.drawing import LineDrawing
from umriss.glyph import Glyph, GlyphInstance


class Tracing(ABC):
    """
    Abstract base class for bitmap tracing algorithms.
    """
    def trace_bitmap(self, bitmap: Bitmap) -> LineDrawing:
        glyphs = self.get_glyphs(bitmap.pixels)
        return LineDrawing(
            bitmap.width,
            bitmap.height,
            [GlyphInstance.from_glyph(g) for g in glyphs]
        )
    
    @abstractmethod
    def get_glyphs(self, pixels: GrayPixels) -> Iterable[Glyph[LineContour]]:
        pass
