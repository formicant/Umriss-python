from typing import TypeVar
import numpy.typing as npt
import numpy as np

from umriss.types import Contour


T = TypeVar('T', bound=np.generic)

def roll_prev(contour: npt.NDArray[T], steps: int=1) -> npt.NDArray[T]:
    return np.roll(contour, steps, axis=0)

def roll_next(contour: npt.NDArray[T], steps: int=1) -> npt.NDArray[T]:
    return np.roll(contour, -steps, axis=0)


def normalize(points: Contour) -> Contour:
    """
    Normalizes every point in a point array using the Euclidean norm.
    If a point is zero, returns zero.
    """
    norms: npt.NDArray[np.float64] = np.linalg.norm(points, axis=1)
    norms = np.where(norms != 0, norms, 1)
    return points / norms[:, np.newaxis]
