import numpy as np
import cv2 as cv

from .types import Vector
from .contour import LineContour
from .drawing import Glyph, GlyphReference, LineDrawing


def unify_glyphs(drawing: LineDrawing, distance: float) -> LineDrawing:
    # naive approach
    n = len(drawing.glyphs)
    matrix = np.zeros((n, n, 2), dtype=np.float64)
    
    for i1, g1 in enumerate(drawing.glyphs):
        for i2 in range(i1):
            g2 = drawing.glyphs[i2]
            offset = _get_similar_glyph_offset(g1, g2, distance)
            matrix[i1, i2] = offset
            matrix[i2, i1] = -offset
    
    masked = np.ma.masked_array(matrix, np.isnan(matrix))
    counts = masked.count(axis=1)[:, 0]
    indices = np.argsort(counts)[::-1]
    indices_left = set(range(n))
    
    free_glyphs: list[Glyph[LineContour]] = []
    ref_glyphs: list[Glyph[LineContour]] = []
    references: list[GlyphReference] = []
    
    for index in indices:
        if index in indices_left:
            row = masked[index]
            base_glyph = drawing.glyphs[index]
            if counts[index] > 1:
                base_offset = -base_glyph.contours[0].bounds.origin
                offsets = []
                (ref_indices,) = np.nonzero(1 - row.mask[:, 0])
                for ref_index in ref_indices:
                    offsets.append(row.data[ref_index] - base_offset)
                
                ref_glyph_index = len(ref_glyphs)
                ref_glyphs.append(_offset_glyph(base_glyph, base_offset))
                references.extend(GlyphReference(ref_glyph_index, o) for o in offsets)
                
                indices_left.difference_update(ref_indices)
            else:
                free_glyphs.append(base_glyph)
                indices_left.remove(index)
    
    return LineDrawing(drawing.width, drawing.height, free_glyphs, ref_glyphs, references)


def _get_similar_glyph_offset(g1: Glyph[LineContour], g2: Glyph[LineContour], distance: float) -> Vector:
    if _are_scontours_similar(g1.contours[0], g2.contours[0], distance):
        return g2.contours[0].bounds.center - g1.contours[0].bounds.center
    else:
        return _nan_vector


def _are_scontours_similar(c1: LineContour, c2: LineContour, distance: float) -> bool:
    if np.max(np.abs(c1.bounds.size - c2.bounds.size)) > 2 * distance:
        return False
    
    ps = (c1.points - (c1.bounds.center - c2.bounds.center)[np.newaxis, :]).astype(np.float32)
    if any(abs(cv.pointPolygonTest(ps, p, True)) > 2 * distance for p in c2.points):
        return False
    
    return True


def _offset_glyph(glyph: Glyph[LineContour], offset: Vector) -> Glyph[LineContour]:
    return Glyph[LineContour]([
        LineContour(c.points + offset)
        for c in glyph.contours
    ])


_nan_vector: Vector = np.array([np.nan, np.nan])
