from typing import Iterable
from collections import defaultdict
from itertools import groupby

from .contour import LineContour
from .drawing import  LineDrawing
from .glyph import Glyph, GlyphOccurrence, GlyphInstance, GlyphReference
from .document import LineDocument


def unify_identical_glyphs(document: LineDocument, use_shared: bool) -> LineDocument:
    glyph_instances = list(_get_glyph_instances(document))
    
    shared_by_glyph: dict[Glyph[LineContour], list[tuple[int, GlyphInstance[LineContour]]]] = defaultdict(list)
    
    if use_shared:
        for page_number, instance in glyph_instances:
            shared_by_glyph[instance.glyph].append((page_number, instance))
    
    multipage_glyphs = (
        (glyph, instances) for glyph, instances in shared_by_glyph.items()
        if len(set(p for p, _ in instances)) > 1
    )
    shared_glyphs = [glyph for glyph, _ in sorted(multipage_glyphs, key=lambda i: -len(i[1]))]
    shared_indices = { glyph: index for index, glyph in enumerate(shared_glyphs) }
    
    unified_pages: list[LineDrawing] = []
    
    instances_by_page = (
        (document.pages[page_number], list(instance for _, instance in instances))
        for page_number, instances in groupby(glyph_instances, lambda i: i[0])
    )
    for page, instances in instances_by_page:
        by_glyph: dict[Glyph[LineContour], list[GlyphInstance[LineContour]]] = defaultdict(list)
        for instance in instances:
            if not instance.glyph in shared_indices:
                by_glyph[instance.glyph].append(instance)
        
        repeating_glyphs = (
            (glyph, instances) for glyph, instances in by_glyph.items()
            if len(instances) > 1
        )
        referenced_glyphs = [glyph for glyph, _ in repeating_glyphs]
        # referenced_glyphs = [glyph for glyph, _ in sorted(repeating_glyphs, key=lambda i: -len(i[1]))]
        refernced_indices = { glyph: index for index, glyph in enumerate(referenced_glyphs) }
        
        occurrences: list[GlyphOccurrence[LineContour]] = []
        for instance in instances:
            shared_index = shared_indices.get(instance.glyph)
            if shared_index is None:
                page_index = refernced_indices.get(instance.glyph)
                if page_index is None:
                    occurrences.append(instance)
                else:
                    occurrences.append(GlyphReference[LineContour](instance.position, page_index, is_shared=False))
            else:
                occurrences.append(GlyphReference[LineContour](instance.position, shared_index, is_shared=True))
        
        unified_pages.append(LineDrawing(page.width, page.height, occurrences, referenced_glyphs))
    
    return LineDocument(unified_pages, shared_glyphs)


def _get_glyph_instances(document: LineDocument) -> Iterable[tuple[int, GlyphInstance[LineContour]]]:
    for page_number, page in enumerate(document.pages):
        for occurrence in page.glyph_occurrences:
            match occurrence:
                case GlyphInstance():
                    instance = occurrence
                case GlyphReference():
                    if occurrence.is_shared:
                        glyph = document.shared_glyphs[occurrence.index]
                    else:
                        glyph = page.referenced_glyphs[occurrence.index]
                    instance = GlyphInstance[LineContour](occurrence.position, glyph)
                case _:
                    raise TypeError('Unsupported glyph occurrence type')
            
            yield (page_number, instance)
