from timeit import default_timer

from . import trace
from .tracing import BinarizedExact, BinarizedPolygon, GrayscalePolygon
from .approximation import Exact, DouglasPeuckerPolygon, SillyCubic


if __name__ == '__main__':
    # TODO: add CLI
    
    input_bitmap_file = 'tmp/gray150.png'
    output_svg_file = 'tmp/out.svg'
    tracing = GrayscalePolygon(200)
    approximation = Exact()
    scale = 1.0
    debug_mode = False
    
    start = default_timer()
    trace(input_bitmap_file, output_svg_file, tracing, approximation, scale, debug_mode)
    end = default_timer()
    
    elapsed_ms = (end - start) * 1000
    print(f'Elapsed {elapsed_ms:.3f} ms')
