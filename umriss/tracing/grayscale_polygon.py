from dataclasses import dataclass
from enum import Enum, auto
from functools import cached_property
from typing import Iterable, Iterator
import numpy as np
import cv2 as cv
import skimage as si

from umriss.bitmap import GrayPixels
from umriss.contour import LineContour
from umriss.drawing import Glyph
from umriss.types import Point, Points
from umriss.utils import simplify_polygon
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
        height, width = pixels.shape
        contours = [
            LineContour(simplify_polygon(c))
            for c in _get_contours(pixels, self.threshold, width, height)
        ]
        outer_contours = (c for c in contours if c.signed_area > 0)
        inner_contours = set(c for c in contours if c.signed_area < 0)
        
        for outer_contour in sorted(outer_contours, key=lambda c: c.signed_area):
            outer_points = outer_contour.points.astype(np.float32)
            glyph_contours = [
                c for c in inner_contours
                if cv.pointPolygonTest(outer_points, c.points[0], False) >= 0
            ]
            inner_contours.difference_update(glyph_contours)
            glyph_contours.insert(0, outer_contour)
            yield Glyph[LineContour](glyph_contours)
        
        if len(inner_contours) > 0:
            canvas = LineContour(_get_corners(width, height))
            glyph_contours = [canvas]
            glyph_contours.extend(inner_contours)
            yield Glyph[LineContour](glyph_contours)
            


def _get_contours(pixels: GrayPixels, threshold: float, width: int, height: int) -> list[Points]:
        contours = si.measure.find_contours(pixels.T, threshold, positive_orientation='high')
        contours = (c + 0.5 for c in contours)
        return _connect_open_contours(contours, width, height)


def _connect_open_contours(contours: Iterable[Points], width: int, height: int) -> list[Points]:
    """
    Connects the edge points of the open contours in the correct order.
    
    From `skimage.measure.find_contours` docs:
    > Output contours are not guaranteed to be closed: contours which intersect
    > the array edge [...] will be left open. All other contours will be closed.
    > (The closed-ness of a contours can be tested by checking whether
    > the beginning point is the same as the end point.)
    
    TODO: refactor
    """
    center = np.array([width / 2, height / 2])
    
    @dataclass
    class EdgePoint:
        point: Point
        contour: Points | None = None
        is_start: bool = False
        
        @cached_property
        def angle(self) -> float:
            angle: float = np.arctan2(*(self.point - center))
            return angle
    
    edge_points = [EdgePoint(corner) for corner in _get_corners(width, height)]
    closed_contours: list[Points] = []
    open_contour_starts = set()
    
    for contour in contours:
        start = contour[0]
        end = contour[-1]
        if np.all(start == end):
            closed_contours.append(contour[:-1])
        else:
            open_contour_starts.add(tuple(start))
            edge_points.append(EdgePoint(start, contour, is_start=True))
            edge_points.append(EdgePoint(end, contour, is_start=False))
    
    edge_points.sort(key=lambda ep: ep.angle)
    
    def to_edge(point: Point) -> Points:
        x, y = point
        if x < 1: x = 0
        elif x > width - 1: x = width
        if y < 1: y = 0
        elif y > height - 1: y = height
        return np.array([[x, y]])
    
    class State(Enum):
        FIND_FIRST = auto()
        FIND_NEXT = auto()
        FIND_END = auto()
        STOP = auto()
    
    current_contour = []
    state = State.FIND_FIRST if len(open_contour_starts) > 0 else State.STOP
    
    while state != State.STOP:
        for ep in edge_points:
            match state, ep:
                case State.FIND_FIRST | State.FIND_NEXT, EdgePoint(p, c, True) if c is not None and tuple(p) in open_contour_starts:
                    current_contour.append(to_edge(p))
                    current_contour.append(c)
                    open_contour_starts.remove(tuple(p))
                    state = State.FIND_END
                case State.FIND_NEXT, EdgePoint(p, None):
                    current_contour.append(np.array([p]))
                case State.FIND_NEXT, EdgePoint(p, c, True) if np.array_equal(p, current_contour[1][0]):
                    closed_contours.append(np.concatenate(current_contour))
                    current_contour = []
                    state = State.FIND_FIRST if len(open_contour_starts) > 0 else State.STOP
                case State.FIND_END, EdgePoint(p, c, False) if np.array_equal(p, current_contour[-1][-1]):
                    current_contour.append(to_edge(p))
                    state = State.FIND_NEXT
    
    return closed_contours


def _get_corners(width: int, height: int) -> Points:
    return np.array([
        [0, 0],
        [0, height],
        [width, height],
        [width, 0]
    ])
