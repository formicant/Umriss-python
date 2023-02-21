from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from umriss.contour import Contour, LineContour
from umriss.drawing import Drawing, LineDrawing, Glyph


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
        approximated_glyphs = [
            Glyph[TContour]([self.approximate_contour(c) for c in glyph.contours])
            for glyph in drawing.glyphs
        ]
        approximated_drawing: Drawing[TContour] = self.DrawingType(
            drawing.width, drawing.height,
            approximated_glyphs
        )
        return approximated_drawing
    
    
    @abstractmethod
    def approximate_contour(self, exact_contour: LineContour) -> TContour:
        pass
