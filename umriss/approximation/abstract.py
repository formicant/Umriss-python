from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from umriss.contour import Contour, LineContour
from umriss.document import Document, LineDocument
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
    def DocumentType(self) -> type:
        pass
    
    @property
    @abstractmethod
    def DrawingType(self) -> type:
        pass
    
    
    def approximate_document(self, document: LineDocument) -> Document[TContour]:
        approximated_shared_glyphs = [
            Glyph[TContour]([self.approximate_contour(c) for c in glyph.contours])
            for glyph in document.shared_glyphs
        ]
        approximated_pages = [self.approximate_drawing(page) for page in document.pages]
        
        return self.DocumentType(approximated_pages, approximated_shared_glyphs)
    
    
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
        approximated_drawing = self.DrawingType(
            drawing.width, drawing.height,
            approximated_glyphs,
            approximated_referenced_glyphs
        )
        return approximated_drawing
    
    
    @abstractmethod
    def approximate_contour(self, exact_contour: LineContour) -> TContour:
        pass
