from nptyping import NDArray, Shape, Number
import numpy as np

from .types import Point, Vector


class BoundingBox:
    def __init__(self, points: NDArray[Shape['*, [x, y]'], Number]):
        
        # `cv.boundingRect` rounds floats. Using numpy instead
        self.left   = np.min(points[:, 0])
        self.right  = np.max(points[:, 0])
        self.top    = np.min(points[:, 1])
        self.bottom = np.max(points[:, 1])
        
        self.origin: Point = np.array([self.left, self.top])
        self.size: Vector = np.array([self.right - self.left, self.bottom - self.top])
        self.center: Point = self.origin + self.size / 2
