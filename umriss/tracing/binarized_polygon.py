from typing import Iterator
import numpy as np

from umriss.bitmap import GrayPixels
from umriss.contour import LineContour
from umriss.drawing import Glyph
from umriss.utils import roll_prev, roll_next, simplify_polygon
from .abstract import Tracing
from .binarized_exact import BinarizedExact


class BinarizedPolygon(Tracing):
    """
    Binarizes the bitmap using a simple threshold method
    and traces it with polygon contours.
    The resulting drawing, when rasterized again into
    a black-and-white bitmap, should match the original bitmap.
    Maximum distance from the exact pixel contour is 0.5 px.
    Preserves the symmetries of the original image.
    """
    
    def __init__(self, max_slope_ratio: int=10, corner_offset: float=0.25):
        if max_slope_ratio < 1:
            raise ValueError('`max_slope_ratio` should be >= 1')
        self.max_slope_ratio = max_slope_ratio
        
        if not 0 <= corner_offset <= 0.25:
            raise ValueError('`corner_offset` should be between 0 and 0.25')
        self.corner_offset = corner_offset
        
        self.binarized_exact = BinarizedExact()
    
    
    def get_glyphs(self, pixels: GrayPixels) -> Iterator[Glyph[LineContour]]:
        exact_glyphs = self.binarized_exact.get_glyphs(pixels)
        
        for glyph in exact_glyphs:
            contours = [
                self._polygonize_contour(contour)
                for contour in glyph.contours
            ]
            yield Glyph[LineContour](contours)
    
    
    def _polygonize_contour(self, exact_contour: LineContour) -> LineContour:
        # We need 4 points and 3 segments between them
        # TODO: cad matrices or a window be used?
        pnt_cur = exact_contour.points
        pnt_prev = roll_prev(pnt_cur)
        pnt_next = roll_next(pnt_cur)
        pnt_next_next = roll_next(pnt_next)
        seg_prev = pnt_cur - pnt_prev
        seg_next = pnt_next - pnt_cur
        seg_next_next = pnt_next_next - pnt_next
        len_prev = np.abs(seg_prev).max(axis=1)
        len_next = np.abs(seg_next).max(axis=1)
        len_next_next = np.abs(seg_next_next).max(axis=1)
        dir_prev = (seg_prev / len_prev[:, np.newaxis]).astype(np.int32)
        dir_next = (seg_next / len_next[:, np.newaxis]).astype(np.int32)
        dir_next_next = (seg_next_next / len_next_next[:, np.newaxis]).astype(np.int32)
        
        # single-pixel contour is returned as is
        if len(pnt_cur) <= 4 and (len_next == 1).all():
            return LineContour(pnt_cur)
        
        # most new vertices will be at the segment centers
        seg_points = (pnt_cur + pnt_next) / 2
        
        # do both `seg_prev` and `seg_next_next` lie to the same side of `seg_next`?
        is_convex = np.abs(dir_prev + dir_next_next).max(axis=1) == 0
        
        # offset some points
        if self.corner_offset > 0:
            # semi-pins
            is_semi_prev = is_convex * (len_prev > 1) * (len_next == 1) * (len_next_next == 1)
            is_semi_next = is_convex * (len_prev == 1) * (len_next == 1) * (len_next_next > 1)
            is_semi_none = is_convex * (len_prev == 1) * (len_next == 1) * (len_next_next == 1)
            is_semi_none = is_semi_none * (1 - roll_next(is_semi_none)) * (1 - roll_prev(is_semi_none))
            is_semi = is_semi_prev + is_semi_next + is_semi_none
            semi_prev_offest = -dir_next * (is_semi_prev * (0.5 - self.corner_offset))[:, np.newaxis]
            semi_next_offest = dir_next * (is_semi_next * (0.5 - self.corner_offset))[:, np.newaxis]
            semi_none_offest = -dir_prev * (is_semi_none * self.corner_offset)[:, np.newaxis]
            semi_offest = semi_prev_offest + semi_next_offest + semi_none_offest
            seg_points += is_semi[:, np.newaxis] * semi_offest
        
        # too long segments and one pixel wide pins, instead of the center point,
        # get two points at a fixed distance from the ends
        is_seg_long = len_next > self.max_slope_ratio
        is_pin = is_convex * (len_prev > 1) * (len_next == 1) * (len_next_next > 1)
        long_offset = dir_next * (is_seg_long * (len_next - self.max_slope_ratio) / 2)[:, np.newaxis]
        pin_offest = dir_next * (is_pin * (0.5 - self.corner_offset))[:, np.newaxis]
        offset = long_offset + pin_offest
        (indices_to_add,) = np.nonzero(is_seg_long + is_pin)
        points_to_add = (seg_points - offset)[indices_to_add]
        seg_points = seg_points + offset
        
        # adding corner points
        is_corner = (len_prev > 1) * (len_next > 1)
        corners = pnt_cur + self.corner_offset * (dir_next - dir_prev)
        (corner_indices,) = np.nonzero(is_corner)
        corner_points = corners[corner_indices]
        
        # insert new points
        indices_to_add = np.concatenate((corner_indices, indices_to_add))
        points_to_add = np.concatenate((corner_points, points_to_add))
        seg_points = np.insert(seg_points, indices_to_add, points_to_add, axis=0)
        
        simplified = simplify_polygon(seg_points)
        return LineContour(simplified)
