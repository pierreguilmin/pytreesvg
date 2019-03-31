"""This module implements various tool functions."""


def map_value(x: float, a: float, b: float, c: float, d: float) -> float:
    """Map linearly x in [a, b] to [c, d].

    The function used to map :math:`x` linearly is

    .. math::
        f : [a, b] & \\to     [c, d] \\\\
            x      & \\mapsto \\frac{x - a}{b - a} * (d - c) + c
    
    Args:
        x: Value to map.
        a: Lower boundary of [a, b] to which x belongs.
        b: Higher boundary of [a, b] to which x belongs.
        c: Lower boundary of [c, d] where we want to map x.
        d: Higher boundary of [c, d] where we want to map x.

    Returns:
        The value of `x` linearly mapped.

    Raises:
        ValueError: If ``a = b`` or ``c = d`` (i.e. if one of the interval is
        empty).

    Examples:
        >>> map(1, 0, 5, 0, 10)
        2.0

        >>> # convert 30 degrees in radian
        >>> import math
        >>> map(30, 0, 180, 0, math.pi)
        0.5235987755982988
    """
    if a == b or c == d:
        raise ValueError("a = b or c = d, intervals shouldn't be empty")

    return (x - a) / (b - a) * (d - c) + c
