from __future__ import annotations
from typing import Self
from abc import ABC
from dataclasses import dataclass
from typing import Generic, TypeVar

from .types import Vector
from .contour import Contour


TContour = TypeVar('TContour', bound=Contour)

@dataclass
class Glyph(Generic[TContour]):
    """
    Represents a connected black area in the image defined by its contours.
    The first contour of a `Glyph` is the outer contour of the area,
    the others being inner contours (holes).
    """
    contours: list[TContour]
    hash: int|None = None
    
    @property
    def outer_contour(self) -> TContour:
        return self.contours[0]
    
    def __hash__(self) -> int:
        if self.hash is None:
            self.hash = 0
            for contour in self.contours:
                self.hash ^= hash(contour)
        return self.hash
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Glyph) or len(self.contours) != len(other.contours):
            return False;
        self_contours = sorted(self.contours, key=lambda c: hash(c))
        other_contours = sorted(self.contours, key=lambda c: hash(c))
        return all(s == o for s, o in zip(self_contours, other_contours))
    
    def offset(self, offset: Vector) -> Glyph[TContour]:
        return Glyph[TContour]([c.offset(offset) for c in self.contours])


@dataclass
class GlyphOccurrence(ABC, Generic[TContour]):
    position: Vector


@dataclass
class GlyphInstance(GlyphOccurrence[TContour], Generic[TContour]):
    """
    Represents a glyph occurring only once in the image
    """
    glyph: Glyph[TContour]
    
    @classmethod
    def from_glyph(cls, glyph: Glyph[TContour]) -> Self:
        position = glyph.outer_contour.bounds.center
        glyph = glyph.offset(-position)
        return cls(position, glyph)


@dataclass
class GlyphReference(GlyphOccurrence[TContour]):
    """
    Represents a reference to a glyph.
    """
    index: int
    is_shared: bool
