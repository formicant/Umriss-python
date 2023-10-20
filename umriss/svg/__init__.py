from typing import TypeVar
from os import path

from umriss.document import Document, LineDocument, CubicDocument
from umriss.drawing import Drawing, LineDrawing, CubicDrawing
from umriss.contour import Contour
from .svg_document import SvgDocument


TContour = TypeVar('TContour', bound=Contour)

def save_as_svg(document: Document[TContour], output_directory: str, scale: float=1.0) -> None:
    if len(document.shared_glyphs) > 0:
        shared_svg = SvgDocument(is_shared=True)
        shared = Drawing[TContour](0, 0, [], document.shared_glyphs)
        _add_drawing(shared_svg, document, shared, scale)
        filename = path.join(output_directory, '_.svg')
        shared_svg.save(filename)
    
    for index, page in enumerate(document.pages):
        svg = SvgDocument(page.width, page.height)
        _add_drawing(svg, document, page, scale)
        
        filename = path.join(output_directory, f'p{index}.svg')
        svg.save(filename)


def _add_drawing(svg: SvgDocument, document: Document[TContour], drawing: Drawing[TContour], scale: float) -> None:
    match document:
        case LineDocument():
            svg.add_line_drawing(drawing, scale)
        case CubicDocument():
            svg.add_cubic_drawing(drawing, scale)
        case _:
            raise TypeError('Unsupported document type.')
