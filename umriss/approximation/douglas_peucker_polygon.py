import numpy as np
import cv2 as cv

from umriss.types import IntContour, Contour
from umriss.drawing import LineDrawing
from .abstract import Approximation


class DouglasPeuckerPolygon(Approximation[Contour]):
    """
    Approximates contours with polygons using the Douglas—Peucker algorithm.
    The maximum distance between the original and the result can be specified.
    """
    DrawingType = LineDrawing
    
    
    def __init__(self, max_distance: float=1.0, preliminary_approximation: Approximation[Contour]|None=None):
        if max_distance <= 0:
            raise ValueError('`max_distance` should be positive')
        self.max_distance = max_distance
        
        self.preliminary_approximation = preliminary_approximation
    
    
    def approximate_contour(self, exact_contour: IntContour) -> Contour:
        contour: Contour
        if self.preliminary_approximation is not None:
            contour = self.preliminary_approximation.approximate_contour(exact_contour).astype(np.float32)
        else:
            contour = exact_contour
        
        approximation = cv.approxPolyDP(contour, self.max_distance, closed=True)
        return np.reshape(approximation, (-1, 2))
