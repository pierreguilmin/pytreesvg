"""This module implements various tool functions."""


def map_value(x: float, a: float, b: float, c: float, d: float) -> float:
    """Map linearly :math:`x` from math:`[a, b]` to math:`[c, d]`.

    The function used is:

    .. math::
        f : [a, b] & \\to     [c, d] \\\\
            x      & \\mapsto \\frac{x - a}{b - a} * (d - c) + c
    
    Args:
        x: Value to map.
        a: Origin interval lower boundary.
        b: Origin interval higher boundary.
        c: Destination interval lower boundary
        d: Destination interval higher boundary.

    Returns:
        The linearly mapped new value.

    Raises:
        ValueError: If ``a = b`` (i.e. the origin interval is empty).

    Examples:
        >>> map(1, 0, 5, 0, 10)
        2.0

        >>> # convert 30 degrees in radian
        >>> import math
        >>> map(30, 0, 360, 0, 2 * math.pi)
        0.5235987755982988
    """
    if a == b:
        raise ValueError('the origin interval is empty')

    return (x - a) / (b - a) * (d - c) + c
