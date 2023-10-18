# from math import sqrt
# import numpy as np
# from scipy.optimize import minimize, Bounds
# import cv2 as cv

# from .types import Points, Vector
# from .contour import LineContour
# from .drawing import Glyph, GlyphReference, LineDrawing


# def unify_glyphs(drawing: LineDrawing, distance: float) -> LineDrawing:
#     # naive approach. too slow
    
#     n = len(drawing.glyphs)
#     print(n)
#     matrix = np.zeros((n, n, 2), dtype=np.float64)
    
#     for i1, g1 in enumerate(drawing.glyphs):
#         for i2 in range(i1):
#             g2 = drawing.glyphs[i2]
#             offset = _get_similar_glyph_offset(g1, g2, distance)
#             matrix[i1, i2] = offset
#             matrix[i2, i1] = -offset
    
#     masked = np.ma.masked_array(matrix, np.isnan(matrix))
#     counts = masked.count(axis=1)[:, 0]
#     indices = np.argsort(counts)[::-1]
#     indices_left = set(range(n))
    
#     free_glyphs: list[Glyph[LineContour]] = []
#     ref_glyphs: list[Glyph[LineContour]] = []
#     references: list[GlyphReference] = []
    
#     for index in indices:
#         if index in indices_left:
#             row = masked[index]
#             base_glyph = drawing.glyphs[index]
#             if counts[index] > 1:
#                 base_offset = -base_glyph.contours[0].bounds.origin
#                 offsets = []
#                 (ref_indices,) = np.nonzero(1 - row.mask[:, 0])
#                 for ref_index in indices_left.intersection(ref_indices):
#                     offsets.append(row.data[ref_index] - base_offset)
                
#                 ref_glyph_index = len(ref_glyphs)
#                 ref_glyphs.append(_offset_glyph(base_glyph, base_offset))
#                 references.extend(GlyphReference(ref_glyph_index, o) for o in offsets)
                
#                 indices_left.difference_update(ref_indices)
#             else:
#                 free_glyphs.append(base_glyph)
#                 indices_left.remove(index)
    
#     return LineDrawing(drawing.width, drawing.height, free_glyphs, ref_glyphs, references)


# def _get_similar_glyph_offset(g1: Glyph[LineContour], g2: Glyph[LineContour], distance: float) -> Vector:
#     outer1, outer2 = g1.contours[0], g2.contours[0]
    
#     # if sizes aren't close, glyphs are different
#     if np.max(np.abs(outer1.bounds.size - outer2.bounds.size)) > 2 * distance:
#         return _nan_vector
    
#     rough_offset = (outer2.bounds.center - outer1.bounds.center).astype(np.float32)
#     rough_distance = distance * (sqrt(2) + 1)
    
#     # determine matching glyph contours by their bounds (small holes are ignored)
#     matching_contours = [(outer1.points.astype(np.float32), outer2.points.astype(np.float32))]
#     contours2 = set(g2.contours[1:])
#     for c1 in g1.contours[1:]:
#         if np.max(c1.bounds.size) <= distance:
#             continue
#         for c2 in contours2:
#             bound_diff = c2.bounds.points - c1.bounds.points - rough_offset
#             if np.max(np.abs(bound_diff)) < rough_distance:
#                 matching_contours.append((c1.points.astype(np.float32), c2.points.astype(np.float32)))
#                 contours2.remove(c2)
#                 break
#         else:  # no matching contour
#             return _nan_vector
#     if any(np.max(c2.bounds.size) > distance for c2 in contours2):
#         return _nan_vector
    
#     # if matching contours aren't close, glyphs are different
#     for ps1, ps2 in matching_contours:
#         ps = ps2 - rough_offset
#         for p in ps1:
#             if abs(cv.pointPolygonTest(ps, p, measureDist=True)) >= rough_distance:
#                 return _nan_vector
    
#     return rough_offset
    
#     # fine tune the offset
#     def get_distance(offset: Vector) -> float:
#         return max(
#             _get_max_contour_distance(c1, (c2 - offset).astype(np.float32))
#             for c1, c2 in matching_contours
#         )
    
#     bounds = (
#         (rough_offset[0] - distance, rough_offset[0] + distance),
#         (rough_offset[1] - distance, rough_offset[1] + distance)
#     )
#     result = minimize(get_distance, rough_offset, bounds=bounds, method='Nelder-Mead', options={ 'maxiter': 4 })
#     offset: Vector = result.x
#     print(result)
    
#     if result.fun <= distance:
#         return offset
#     else:
#         return _nan_vector


# def _get_max_contour_distance(c1: Points, c2: Points) -> float:
#     d1: float = max(abs(cv.pointPolygonTest(c2, p, measureDist=True)) for p in c1)
#     d2: float = max(abs(cv.pointPolygonTest(c1, p, measureDist=True)) for p in c2)
#     return max(d1, d2)


# def _offset_glyph(glyph: Glyph[LineContour], offset: Vector) -> Glyph[LineContour]:
#     return Glyph[LineContour]([
#         LineContour(c.points + offset)
#         for c in glyph.contours
#     ])


# _nan_vector: Vector = np.array([np.nan, np.nan])

# _fine_tuning_iterations = 4
