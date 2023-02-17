from timeit import default_timer

from . import trace
from .approximation import Exact, AccuratePolygon, DouglasPeuckerPolygon, SillyCubic


if __name__ == '__main__':
    # TODO: add CLI
    
    input_bitmap_file = 'images/page1/page1-bw.png'
    output_svg_file = 'images/out.svg'
    approximation = AccuratePolygon()
    scale = 1.0
    debug_mode = False
    
    start = default_timer()
    trace(input_bitmap_file, output_svg_file, approximation, scale, debug_mode)
    end = default_timer()
    
    elapsed_ms = (end - start) * 1000
    print(f'Elapsed {elapsed_ms:.3f} ms')
