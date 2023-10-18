from abc import ABC
from dataclasses import dataclass, field
from typing import Generic, TypeVar, Sequence

from .contour import Contour, LineContour, CubicContour
from .glyph import GlyphOccurrence, Glyph


TContour = TypeVar('TContour', bound=Contour)

@dataclass
class Drawing(ABC, Generic[TContour]):
    """
    Represents a vector image consisting of `glyphs`.
    `glyph_occurrences` are actual glyphs or references to glyphs.
    `referenced_glyphs` are glyphs occurring multiple times in the image.
    """
    width: float
    height: float
    glyph_occurrences: Sequence[GlyphOccurrence[TContour]]
    referenced_glyphs: list[Glyph[TContour]] = field(default_factory=lambda: [])


@dataclass
class LineDrawing(Drawing[LineContour]):
    """
    Vector image consisting of polygons.
    """
    pass


@dataclass
class CubicDrawing(Drawing[CubicContour]):
    """
    Vector image consisting of cubic Bézier splines.
    """
    pass
