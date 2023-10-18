from typing import TypeVar
import numpy.typing as npt
import numpy as np

from .types import Points, Vectors


T = TypeVar('T', bound=np.generic)

def lexicographic_argmin(points: Points) -> int:
    xs = points[:, 0]
    min_by_x = xs.min()
    indices = np.where(xs == min_by_x)[0]
    argmin: int = indices[np.argmin(points[indices, 1])]
    return argmin


def roll_prev(points: npt.NDArray[T], steps: int=1) -> npt.NDArray[T]:
    return np.roll(points, steps, axis=0)

def roll_next(points: npt.NDArray[T], steps: int=1) -> npt.NDArray[T]:
    return np.roll(points, -steps, axis=0)


def normalize(vectors: Vectors) -> Vectors:
    """
    Normalizes every vector in a vector array using the Euclidean norm.
    If a vector is zero, returns zero.
    """
    norms: npt.NDArray[np.float64] = np.linalg.norm(vectors, axis=1)
    norms = np.where(norms != 0, norms, 1)
    return vectors / norms[:, np.newaxis]


_epsilon = 1e-12

def are_equal(points1: Points, points2: Points, epsilon: float=_epsilon) -> bool:
    if points1.shape != points2.shape:
        return False;
    max_abs_difference: float = np.max(np.absolute(points1 - points2))
    return max_abs_difference <= epsilon


def simplify_polygon(polygon: Points, epsilon: float=_epsilon) -> Points:
    """
    Removes polygon segments of zero length and
    combines consecutive segments of the same direction.
    """
    polygon = remove_zero_length_segments(polygon, epsilon)
    polygon = combine_same_direction_segments(polygon, epsilon)
    return polygon


def remove_zero_length_segments(polygon: Points, epsilon: float=_epsilon) -> Points:
    len_prev = np.linalg.norm(polygon - roll_prev(polygon), axis=1)
    indices = np.nonzero(len_prev <= epsilon)
    return np.delete(polygon, indices, axis=0)


def combine_same_direction_segments(polygon: Points, epsilon: float=_epsilon) -> Points:
    dir_prev = normalize(polygon - roll_prev(polygon))
    dir_next = normalize(roll_next(polygon) - polygon)
    dir_diff = np.linalg.norm(dir_next - dir_prev, axis=1)
    indices = np.nonzero(dir_diff <= epsilon)
    return np.delete(polygon, indices, axis=0)
