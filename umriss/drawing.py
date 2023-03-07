from abc import ABC
from dataclasses import dataclass, field
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
class GlyphReference:
    """
    Represents a reference to a glyph.
    """
    index: int
    offset: Vector


@dataclass
class Drawing(ABC, Generic[TContour]):
    """
    Represents a vector image consisting of `glyphs`.
    `referenced_glyphs` are glyphs occurring multiple times in the image.
    `references` define positions of each occurrence.
    """
    width: float
    height: float
    glyphs: list[Glyph[TContour]]
    referenced_glyphs: list[Glyph[TContour]] = field(default_factory=lambda: [])
    references: list[GlyphReference] = field(default_factory=lambda: [])


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
