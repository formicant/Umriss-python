from abc import ABC
from dataclasses import dataclass
from typing import Generic, TypeVar

from .types import Vector
from .contour import Contour, LineContour, CubicContour


TContour = TypeVar('TContour', bound=Contour)

@dataclass
class Glyph(Generic[TContour]):
    """
    Represents a connected black area in the image defined by its contours.
    The first contour of a `Glyph` is the outer contour of the area,
    the others being inner contours (holes).
    """
    contours: list[TContour]
    
    @property
    def outer_contour(self) -> TContour:
        return self.contours[0]


@dataclass
class Font(Generic[TContour]):
    """
    Represents a set of glyphs which can be referenced
    multiple times in drawings.
    """
    glyphs: list[Glyph[TContour]]


@dataclass
class GlyphReference(Generic[TContour]):
    """
    Represents a reference to a glyph in a font.
    """
    font: Font[TContour]
    index: int
    offset: Vector


@dataclass
class Drawing(ABC, Generic[TContour]):
    """
    Represents a vector image consisting of `Glyph`s.
    """
    width: float
    height: float
    glyphs: list[Glyph[TContour]]
    glyph_references: list[GlyphReference[TContour]] | None = None


class LineDrawing(Drawing[LineContour]):
    """
    Vector image consisting of polygons.
    """
    pass


class CubicDrawing(Drawing[CubicContour]):
    """
    Vector image consisting of cubic Bézier splines.
    """
    pass
