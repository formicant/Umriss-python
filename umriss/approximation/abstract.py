from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Sequence

from umriss.contour import Contour, LineContour
from umriss.drawing import Drawing, LineDrawing
from umriss.glyph import GlyphOccurrence, GlyphInstance, GlyphReference, Glyph


TContour = TypeVar('TContour', bound=Contour)

class Approximation(ABC, Generic[TContour]):
    """
    Abstract generic base class for approximation algorithms.
    The type parameter `TContour` defines the type of approximated contours.
    In the descendants, the `DrawingType` type should inherit `Drawing[TContour]`.
    """
    
    @property
    @abstractmethod
    def DrawingType(self) -> type:
        pass
    
    
    def approximate_drawing(self, drawing: LineDrawing) -> Drawing[TContour]:
        approximated_glyphs: list[GlyphOccurrence[TContour]] = []
        for occurrence in drawing.glyph_occurrences:
            match occurrence:
                case GlyphInstance():
                    approximated_glyphs.append(GlyphInstance[TContour](
                        occurrence.position,
                        Glyph[TContour]([self.approximate_contour(c) for c in occurrence.glyph.contours])
                    ))
                case GlyphReference():
                    approximated_glyphs.append(occurrence)
                case _:
                    raise TypeError('Unsupported glyph occurrence type')
        
        approximated_referenced_glyphs = [
            Glyph[TContour]([self.approximate_contour(c) for c in glyph.contours])
            for glyph in drawing.referenced_glyphs
        ]
        approximated_drawing: Drawing[TContour] = self.DrawingType(
            drawing.width, drawing.height,
            approximated_glyphs,
            approximated_referenced_glyphs
        )
        return approximated_drawing
    
    
    @abstractmethod
    def approximate_contour(self, exact_contour: LineContour) -> TContour:
        pass
