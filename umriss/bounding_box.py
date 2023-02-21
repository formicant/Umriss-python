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
        
        self.center: Point = np.array([(self.left + self.right) / 2, (self.top - self.bottom) / 2])
        self.size: Vector = np.array([self.right - self.left, self.bottom - self.top])
