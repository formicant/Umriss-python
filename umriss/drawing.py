from abc import ABC
from dataclasses import dataclass
from typing import Generic, TypeVar

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
class Drawing(ABC, Generic[TContour]):
    """
    Represents a vector image consisting of `Glyph`s.
    """
    width: float
    height: float
    glyphs: list[Glyph[TContour]]


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
