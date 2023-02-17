import numpy as np
from numpy.linalg import norm

from umriss.types import Contour
from umriss.numpy_tools import roll_prev, roll_next, normalize


_epsilon = 1e-12


def simplify_contour(contour: Contour, epsilon: float=_epsilon) -> Contour:
    """
    Removes contour segments of zero length and
    combines consecutive segments of the same direction.
    """
    contour = remove_zero_length_segments(contour, epsilon)
    contour = combine_same_direction_segments(contour, epsilon)
    return contour


def remove_zero_length_segments(contour: Contour, epsilon: float=_epsilon) -> Contour:
    len_prev = norm(contour - roll_prev(contour), axis=1)
    indices = np.nonzero(len_prev <= epsilon)
    return np.delete(contour, indices, axis=0)


def combine_same_direction_segments(contour: Contour, epsilon: float=_epsilon) -> Contour:
    dir_prev = normalize(contour - roll_prev(contour))
    dir_next = normalize(roll_next(contour) - contour)
    dir_diff = norm(dir_next - dir_prev, axis=1)
    indices = np.nonzero(dir_diff <= epsilon)
    return np.delete(contour, indices, axis=0)
