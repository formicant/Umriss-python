from typing import Iterator
from nptyping import NDArray, Shape, Int
import numpy as np
import cv2 as cv

from umriss.types import IntPoint, IntVectors
from umriss.bitmap import GrayPixels
from umriss.contour import LineContour
from umriss.drawing import Glyph
from umriss.utils import roll_prev, roll_next
from .abstract import Tracing


class BinarizedExact(Tracing):
    """
    Binarizes the bitmap using a simple threshold method
    and draws an exact contour around the black pixels of the image.
    """
    def get_glyphs(self, pixels: GrayPixels) -> Iterator[Glyph[LineContour]]:
        _, inv_pixels = cv.threshold(pixels, 128, 255, cv.THRESH_BINARY_INV)
        cv_contours, [hierarchy] = cv.findContours(inv_pixels, cv.RETR_CCOMP, cv.CHAIN_APPROX_NONE)
        
        index = 0
        while index >= 0:
            outer_contour = _get_exact_contour(cv_contours[index])
            glyph_contours = [outer_contour]
            index, _, child, _ = hierarchy[index]
            
            while child >= 0:
                inner_contour = _get_exact_contour(cv_contours[child])
                glyph_contours.append(inner_contour)
                child, _, _, _ = hierarchy[child]
            
            yield Glyph[LineContour](glyph_contours)


def _get_exact_contour(cv_contour: NDArray[Shape['*, 1, [x, y]'], Int]) -> LineContour:
    """
    An OpenCV's contour is an array of the coordinates of the area's outer pixels.
    This function converts it into the edge line around the area's pixels.
    """
    contour = cv_contour.reshape(-1, 2)
    relative = contour - roll_prev(contour)
    
    indices_from = _get_indices(relative, to=False)
    indices_to = _get_indices(roll_next(relative), to=True)
    indices_to = (indices_to - indices_from) % 4 + indices_from + 1
    
    exact_contour = np.concatenate([
        _directions[index_from:index_to]
        for index_from, index_to in zip(indices_from, indices_to)
    ])
    exact_contour, start_offset = _simplify_relative(exact_contour)
    
    start_offset += (_directions[indices_from[0]] @ _offset_transform + 0.5).astype(np.int32)
    absolute = contour[0] + start_offset + exact_contour.cumsum(axis=0)
    
    return LineContour(absolute)


def _simplify_relative(relative_contour: IntVectors) -> tuple[IntVectors, IntPoint]:
    """
    Combines consecutive contour segments of the same direction.
    """
    difference = relative_contour - roll_prev(relative_contour)
    
    (segment_indices,) = np.nonzero(difference.any(axis=1))
    start_offset = relative_contour[0] * segment_indices[0]
    
    last_index = len(relative_contour) + segment_indices[0]
    segment_sizes = np.append(segment_indices[1:], last_index) - segment_indices
    simplified_contour = relative_contour[segment_indices] * segment_sizes[:, np.newaxis]
    
    return (simplified_contour, start_offset)


_IndexArray = NDArray[Shape['*'], Int]

def _get_indices(directions: IntVectors, to: bool) -> _IndexArray:
    index_by_direction = _index_by_to_direction if to else _index_by_from_direction
    indices: _IndexArray = index_by_direction[tuple(directions.T + 1)]
    return indices


_directions = np.array([
    [ 0,  1], # 0 down
    [ 1,  0], # 1 right
    [ 0, -1], # 2 up
    [-1,  0], # 3 left
    [ 0,  1], # 4 down again
    [ 1,  0], # 5 right again
    [ 0, -1], # 6 up again
])

_index_by_from_direction = np.array([
# y -1  0  1      x
    [2, 3, 3], # -1
    [2, 0, 0], #  0
    [1, 1, 0], #  1
])

_index_by_to_direction = np.array([
# y -1  0  1      x
    [3, 3, 0], # -1
    [2, 3, 0], #  0
    [2, 1, 1], #  1
])

_offset_transform = np.array([
    [-0.5,  0.5],
    [-0.5, -0.5],
])
