from timeit import default_timer

from . import trace
from .tracing import BinarizedExact, BinarizedPolygon, GrayscalePolygon
from .approximation import Exact, DouglasPeuckerPolygon, SillyCubic


if __name__ == '__main__':
    # TODO: add CLI
    
    input_bitmap_files = [
        'tmp/input_ku/173.tif',
        'tmp/input_ku/174.tif',
        'tmp/input_ku/175.tif',
    ]
    output_directory = 'tmp/out'
    tracing = BinarizedPolygon()
    approximation = Exact() # DouglasPeuckerPolygon(0.5)
    scale = 1.0
    
    start = default_timer()
    trace(input_bitmap_files, output_directory, tracing, approximation, scale)
    end = default_timer()
    
    elapsed_ms = (end - start) * 1000
    print(f'Elapsed {elapsed_ms:.3f} ms')
