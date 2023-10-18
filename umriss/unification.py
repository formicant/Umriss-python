from collections import defaultdict

from .types import Points, Vector
from .contour import LineContour
from .drawing import  LineDrawing
from .glyph import Glyph, GlyphOccurrence, GlyphInstance, GlyphReference


def unify_identical_glyphs(drawing: LineDrawing) -> LineDrawing:
    glyph_instances = _get_glyph_instances(drawing)
    
    glyph_dict: dict[Glyph[LineContour], list[GlyphInstance[LineContour]]] = dict()
    referenced_glyphs: list[Glyph[LineContour]] = []
    index_dict: dict[Glyph[LineContour], int] = dict()
    
    for glyph, instance in glyph_instances:
        if glyph in glyph_dict:
            if len(glyph_dict[glyph]) == 1:
                index_dict[glyph] = len(referenced_glyphs)
                referenced_glyphs.append(glyph)
            glyph_dict[glyph].append(instance)
        else:
            glyph_dict[glyph] = [instance]
    
    occurrences: list[GlyphOccurrence[LineContour]] = []
    
    for glyph, instance in glyph_instances:
        index = index_dict.get(glyph)
        if index is None:
            occurrences.append(instance)
        else:
            occurrences.append(GlyphReference[LineContour](instance.position, index, is_shared=False))
    
    return LineDrawing(drawing.width, drawing.height, occurrences, referenced_glyphs)


def _get_glyph_instances(drawing: LineDrawing) -> list[tuple[Glyph[LineContour], GlyphInstance[LineContour]]]:
    glyph_instances = []
    
    for occurrence in drawing.glyph_occurrences:
        match occurrence:
            case GlyphInstance():
                glyph = occurrence.glyph
                instance = occurrence
            case GlyphReference():
                glyph = drawing.referenced_glyphs[occurrence.index]
                instance = GlyphInstance[LineContour](occurrence.position, glyph)
            case _:
                raise TypeError('Unsupported glyph occurrence type')
        glyph_instances.append((glyph, instance))
    
    return glyph_instances
