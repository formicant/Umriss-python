import numpy as np

from .types import Point, Points, Vector


class BoundingBox:
    def __init__(self, points: Points):
        
        # `cv.boundingRect` rounds floats. Using numpy instead
        left   = np.min(points[:, 0])
        right  = np.max(points[:, 0])
        top    = np.min(points[:, 1])
        bottom = np.max(points[:, 1])
        
        self.points: Points = np.array([[left, top], [right, bottom]])
        
        self.origin: Point = self.points[0]
        self.size: Vector = self.points[1] - self.points[0]
        self.center: Point = self.origin + self.size / 2
