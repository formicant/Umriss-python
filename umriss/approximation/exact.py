from umriss.types import IntContour
from umriss.drawing import ExactDrawing
from .abstract import Approximation


class Exact(Approximation[IntContour]):
    """
    Leaves contours as is.
    """
    DrawingType = ExactDrawing
    
    def approximate_contour(self, exact_contour: IntContour) -> IntContour:
        return exact_contour
