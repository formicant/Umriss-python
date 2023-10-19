import numpy as np
import cv2 as cv

from umriss.contour import LineContour
from umriss.document import LineDocument
from umriss.drawing import LineDrawing
from .abstract import Approximation


class DouglasPeuckerPolygon(Approximation[LineContour]):
    """
    Approximates contours with polygons using the Douglas—Peucker algorithm.
    The maximum distance between the original and the result can be specified.
    """
    DrocumentType = LineDocument
    DrawingType = LineDrawing
    
    
    def __init__(self, max_distance: float=1.0):
        if max_distance <= 0:
            raise ValueError('`max_distance` should be positive')
        self.max_distance = max_distance
    
    
    def approximate_contour(self, contour: LineContour) -> LineContour:
        points = contour.points.astype(np.float32)
        approximation = cv.approxPolyDP(points, self.max_distance, closed=True)
        return LineContour(np.reshape(approximation, (-1, 2)))
