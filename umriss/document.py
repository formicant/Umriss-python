from abc import ABC
from dataclasses import dataclass, field
from typing import Generic, TypeVar

from .contour import Contour, LineContour, CubicContour
from .drawing import Drawing
from .glyph import Glyph


TContour = TypeVar('TContour', bound=Contour)

@dataclass
class Document(ABC, Generic[TContour]):
    """
    Represents a multi-page document.
    """
    pages: list[Drawing[TContour]]
    shared_glyphs: list[Glyph[TContour]] = field(default_factory=lambda: [])


@dataclass
class LineDocument(Document[LineContour]):
    pass


@dataclass
class CubicDocument(Document[CubicContour]):
    pass
