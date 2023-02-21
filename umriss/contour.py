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
        self._bounds: BoundingBox | None = None
    
    @property
    def bounds(self) -> BoundingBox:
        if self._bounds is None:
            self._bounds = BoundingBox(self.points)
        return self._bounds


class CubicContour(Contour):
    """
    A closed cubic Bézier spline.
    """
    def __init__(self, nodes: CubicNodes):
        self.nodes = nodes
