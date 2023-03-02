from functools import cached_property
import numpy as np
import cv2 as cv

from umriss.types import Points, CubicNodes
from .bounding_box import BoundingBox


class Contour:
    """
    Base class for contours.
    """
    pass


class LineContour(Contour):
    """
    A contour consisting of line segments, i.e. a polygon.
    """
    def __init__(self, points: Points):
        self.points = points
    
    @cached_property
    def bounds(self) -> BoundingBox:
        return BoundingBox(self.points)
    
    @cached_property
    def signed_area(self) -> float:
        area: float = cv.contourArea(self.points.astype(np.float32), oriented=True)
        return -area


class CubicContour(Contour):
    """
    A closed cubic Bézier spline.
    """
    def __init__(self, nodes: CubicNodes):
        self.nodes = nodes
