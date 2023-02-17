from abc import ABC, abstractproperty
from dataclasses import dataclass
from nptyping import NDArray, Shape, Int, Number


IntPoint         = NDArray[Shape['[x, y]'], Int]
Point            = NDArray[Shape['[x, y]'], Number]

QuadraticNode    = NDArray[Shape['[ctrl, point], [x, y]'], Number]
CubicNode        = NDArray[Shape['[ctrl1, ctrl2, point], [x, y]'], Number]

IntContour       = NDArray[Shape['*, [x, y]'], Int]
Contour          = NDArray[Shape['*, [x, y]'], Number]

QuadraticContour = NDArray[Shape['*, [ctrl, point], [x, y]'], Number]
CubicContour     = NDArray[Shape['*, [ctrl1, ctrl2, point], [x, y]'], Number]
