from typing import Iterator
import numpy as np
import skimage as si

from umriss.bitmap import GrayPixels
from umriss.contour import LineContour
from umriss.drawing import Glyph
from .abstract import Tracing


class GrayscalePolygon(Tracing):
    """
    Traces the grayscale bitmap usiing the marching squares algorithm.
    The resulting drawing, when rasterized again into a grayscale bitmap,
    should be very similar to the original bitmap.
    """
    
    def __init__(self, threshold: float=128):
        self.threshold = threshold
    
    
    def get_glyphs(self, pixels: GrayPixels) -> Iterator[Glyph[LineContour]]:
        contours = si.measure.find_contours(pixels.T, self.threshold)
        glyph = Glyph[LineContour]([LineContour(c + _half_pixel[np.newaxis, :]) for c in contours])
        yield glyph


_half_pixel = np.array([0.5, 0.5])
