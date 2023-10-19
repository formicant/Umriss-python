import numpy as np

from umriss.contour import LineContour, CubicContour
from umriss.document import CubicDocument
from umriss.drawing import CubicDrawing
from umriss.utils import roll_prev, roll_next, normalize
from umriss.types import CubicNodes, Points
from .abstract import Approximation


class SillyCubic(Approximation[CubicContour]):
    """
    Applies a given `polygonal_approximation` first.
    Then, draws a smooth cubic spline between the even points of the polygon.
    The odd ones are used for tangents in a not-so-clever way.
    For tests only. The results can be terrible.
    """
    DocumentType = CubicDocument
    DrawingType = CubicDrawing
    
    
    def approximate_contour(self, contour: LineContour) -> CubicContour:
        polygon = contour.points
        
        # the number of points should be even
        if len(polygon) % 2 != 0:
            polygon = _insert_additional_point(polygon)
        
        # segment points
        p_middle = polygon[::2]
        p_end = polygon[1::2]
        p_start = roll_prev(p_end)
        
        # tangent directions
        dir_start = normalize(p_middle - roll_prev(p_middle))
        dir_end = normalize(p_middle - roll_next(p_middle))
        print(polygon)
        
        # tangent kengths
        len_start = np.abs(np.sum(dir_start * (p_middle - p_start), axis=1))
        len_end = np.abs(np.sum(dir_end * (p_middle - p_end), axis=1))
        
        # control points
        ctrl_start = p_start + dir_start * len_start[:, np.newaxis]
        ctrl_end = p_end + dir_end * len_end[:, np.newaxis]
        
        nodes: CubicNodes = np.stack((ctrl_start, ctrl_end, p_end), axis=1)
        return CubicContour(nodes)
    
    
def _insert_additional_point(polygon: Points) -> Points:
    prev_points = roll_prev(polygon)
    longest_segment_index = np.argmax(np.linalg.norm(polygon - prev_points, axis=1))
    new_point = (polygon[longest_segment_index] + prev_points[longest_segment_index]) / 2
    return np.insert(polygon, [longest_segment_index], [new_point], axis=0)
