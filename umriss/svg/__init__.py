from typing import TypeVar
from os import path

from umriss.document import Document, LineDocument, CubicDocument
from umriss.contour import Contour
from .svg_document import SvgDocument


TContour = TypeVar('TContour', bound=Contour)

def save_as_svg(document: Document[TContour], output_directory: str, scale: float=1.0) -> None:
    for index, page in enumerate(document.pages):
        svg = SvgDocument(page.width, page.height)
        
        match document:
            case LineDocument():
                svg.add_line_drawing(page, scale)
            case CubicDocument():
                svg.add_cubic_drawing(page, scale)
            case _:
                raise TypeError('Unsupported document type.')
        
        filename = path.join(output_directory, f'p{index}.svg')
        svg.save(filename)
