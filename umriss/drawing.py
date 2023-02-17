from abc import ABC
from dataclasses import dataclass
from typing import Generic, TypeVar

from .types import IntContour, Contour, QuadraticContour, CubicContour


TContour = TypeVar('TContour')

@dataclass
class Glyph(Generic[TContour]):
    """
    Represents a connected black area in the image defined by its contours.
    The first contour of a `Glyph` is the outer contour of the area,
    the others being inner contours (holes).
    """
    contours: list[TContour]


@dataclass
class Drawing(ABC, Generic[TContour]):
    """
    Represents a vector image consisting of `Glyph`s.
    """
    glyphs: list[Glyph[TContour]]


class ExactDrawing(Drawing[IntContour]):
    """
    Exact vector representation of image pixels.
    """
    pass


class LineDrawing(Drawing[Contour]):
    """
    Vector image consisting of polygons.
    """
    pass


class QuadraticDrawing(Drawing[QuadraticContour]):
    """
    Vector image consisting of quadratic Bézier splines.
    """
    pass


class CubicDrawing(Drawing[CubicContour]):
    """
    Vector image consisting of cubic Bézier splines.
    """
    pass
