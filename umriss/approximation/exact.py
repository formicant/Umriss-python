from umriss.contour import LineContour
from umriss.drawing import LineDrawing
from .abstract import Approximation


class Exact(Approximation[LineContour]):
    """
    Leaves the contour as is.
    """
    DrawingType = LineDrawing
    
    
    def approximate_contour(self, contour: LineContour) -> LineContour:
        return contour
