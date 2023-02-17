from typing import Iterator
from nptyping import NDArray, Shape, UInt8
import cv2 as cv

from umriss.drawing import ExactDrawing, Glyph
from umriss.types import IntContour
from .exact_contour import get_exact_contour


class Image:
    """
    Represents a black-and-white (binarized) bitmap image
    defined by its dimensions (`width` and `height`)
    and a `drawing` consisting of `Glyph`s (connected black areas of the image).
    """
    def __init__(self, image_file: str):
        """
        The `image_file` will be binarized using the simplest threshold method.
        For better quality, consider binarizing the image beforehand
        using a more advanced binarization method.
        """
        image = cv.imread(image_file, cv.IMREAD_GRAYSCALE)
        
        self.height, self.width = image.shape
        self.drawing = ExactDrawing(list(_get_glyphs(image)))


def _get_glyphs(image: NDArray[Shape['*, *'], UInt8]) -> Iterator[Glyph[IntContour]]:
    cv.threshold(image, 128, 255, cv.THRESH_BINARY_INV, dst=image)
    cv_contours, [hierarchy] = cv.findContours(image, cv.RETR_CCOMP, cv.CHAIN_APPROX_NONE)
    
    index = 0
    while index >= 0:
        outer_contour = get_exact_contour(cv_contours[index])
        glyph_contours = [outer_contour]
        index, _, child, _ = hierarchy[index]
        
        while child >= 0:
            inner_contour = get_exact_contour(cv_contours[child])
            glyph_contours.append(inner_contour)
            child, _, _, _ = hierarchy[child]
        
        yield Glyph[IntContour](glyph_contours)
