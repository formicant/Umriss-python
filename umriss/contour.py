from __future__ import annotations
from typing import Self
from abc import ABC, abstractmethod
from functools import cached_property
import numpy as np
import cv2 as cv

from .types import Points, CubicNodes, Vector
from .utils import lexicographic_argmin, are_equal
from .bounding_box import BoundingBox


class Contour(ABC):
    """
    Base class for contours.
    """
    @property
    @abstractmethod
    def bounds(self) -> BoundingBox:
        raise NotImplementedError
    
    @property
    @abstractmethod
    def hash(self) -> int:
        raise NotImplementedError
    
    @abstractmethod
    def standardize(self) -> Self:
        raise NotImplementedError
    
    @abstractmethod
    def is_equal_to(self, other: Self) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def offset(self, vector: Vector) -> Self:
        raise NotImplementedError


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
    
    @cached_property
    def hash(self) -> int:
        return hash(self.points.data)
    
    def standardize(self) -> LineContour:
        """
        Returns an equivalent contour whose start point is lexicographically minimal.
        Should be used before hashing and comparison.
        """
        start_insex = lexicographic_argmin(self.points)
        points = np.roll(self.points, -start_insex, axis=0)
        return LineContour(points)
    
    def is_equal_to(self, other: LineContour) -> bool:
        return are_equal(self.points, other.points)
    
    def offset(self, offset: Vector) -> LineContour:
        return LineContour(self.points + offset)
    


class CubicContour(Contour):
    """
    A closed cubic Bézier spline.
    """
    def __init__(self, nodes: CubicNodes):
        self.nodes = nodes
