from nptyping import NDArray, Shape, Int, Number


IntPoint = NDArray[Shape['[x, y]'], Int]
IntPoints = NDArray[Shape['*, [x, y]'], Int]

IntVector = NDArray[Shape['[x, y]'], Int]
IntVectors = NDArray[Shape['*, [x, y]'], Int]

Point = NDArray[Shape['[x, y]'], Number]
Points = NDArray[Shape['*, [x, y]'], Number]

Vector = NDArray[Shape['[x, y]'], Number]
Vectors = NDArray[Shape['*, [x, y]'], Number]

QuadraticNode = NDArray[Shape['[ctrl1, ctrl2, point], [x, y]'], Number]
QuadraticNodes = NDArray[Shape['*, [ctrl1, ctrl2, point], [x, y]'], Number]

CubicNode = NDArray[Shape['[ctrl1, ctrl2, point], [x, y]'], Number]
CubicNodes = NDArray[Shape['*, [ctrl1, ctrl2, point], [x, y]'], Number]
