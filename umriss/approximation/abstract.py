from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from umriss.types import IntContour
from umriss.drawing import Drawing, ExactDrawing, Glyph


TContour = TypeVar('TContour')

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
    
    
    def approximate_drawing(self, exact_drawing: ExactDrawing) -> Drawing[TContour]:
        drawing: Drawing[TContour] = self.DrawingType([
            Glyph[TContour]([self.approximate_contour(c) for c in glyph.contours])
            for glyph in exact_drawing.glyphs
        ])
        return drawing
    
    
    @abstractmethod
    def approximate_contour(self, exact_contour: IntContour) -> TContour:
        pass
