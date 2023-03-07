from math import atan, floor, sqrt, pi


_debug_colors = dict()


def get_debug_color(index: int) -> str:
    """
    Gets unique color for every index.
    For debugging purposes only.
    """
    if not index in _debug_colors:
        hue = 0.23 + _phi * index
        hue -= floor(hue)
        r, g, b = _hsl_to_rgb(hue, 1, 0.5)
        y = r * 0.299 + g * 0.587 + b * 0.114
        l = 0.5 + atan(2 * (0.333 - y)) / pi
        r, g, b = _hsl_to_rgb(hue, 1, 0.9 - (0.9 - l / 1.5) / (1 + (index - 1) / 18))
        color = f'#{round(255 * r):02X}{round(255 * g):02X}{round(255 * b):02X}'
        _debug_colors[index] = color
    
    return _debug_colors[index]


def _hsl_to_rgb(h: float, s: float, l: float) -> tuple[float, float, float]:
    q = l * (1 + s) if l < 0.5 else l + s - l * s
    p = 2 * l - q
    r = sqrt(_hue_to_rgb(p, q, h + 1/3))
    g = sqrt(_hue_to_rgb(p, q, h))
    b = sqrt(_hue_to_rgb(p, q, h - 1/3))
    return (r, g, b)


def _hue_to_rgb(p: float, q: float, t: float) -> float:
    if t < 0: t += 1
    if t > 1: t -= 1
    if t < 1/6: return p + (q - p) * 6 * t
    if t < 1/2: return q
    if t < 2/3: return p + (q - p) * 6 * (2/3 - t)
    return p


_phi = 0.38196601125;
