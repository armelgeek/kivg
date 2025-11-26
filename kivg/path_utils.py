"""
Path utilities for Kivg.
Contains functions for SVG path manipulation and coordinate transformation.
"""

from typing import Tuple, List, Union, Callable
import math
from svg.path.path import Line, CubicBezier


def transform_x(
    x_pos: float, target_x: float, target_width: float, svg_width: float
) -> float:
    """
    Transform an X coordinate from SVG to target coordinate system.

    Args:
        x_pos: SVG x coordinate
        target_x: Target x position
        target_width: Target width
        svg_width: SVG width

    Returns:
        Transformed x coordinate
    """
    return target_x + target_width * x_pos / svg_width


def transform_y(
    y_pos: float,
    target_y: float,
    target_height: float,
    svg_height: float,
    flip_y: bool = True,
) -> float:
    """
    Transform a Y coordinate from SVG to target coordinate system.

    Args:
        y_pos: SVG y coordinate
        target_y: Target y position
        target_height: Target height
        svg_height: SVG height
        flip_y: Whether to flip the Y axis (SVG has origin at top-left)

    Returns:
        Transformed y coordinate
    """
    if flip_y:
        return target_y + target_height * (svg_height - y_pos) / svg_height
    return target_y + target_height * y_pos / svg_height


def transform_point(
    complex_point: complex,
    target_size: Tuple[float, float],
    target_pos: Tuple[float, float],
    svg_size: Tuple[float, float],
    flip_y: bool = True,
) -> List[float]:
    """
    Transform a complex point from SVG to target coordinate system.

    Args:
        complex_point: SVG point as complex number
        target_size: (width, height) of target
        target_pos: (x, y) of target
        svg_size: (width, height) of SVG
        flip_y: Whether to flip the Y axis

    Returns:
        [x, y] transformed coordinates
    """
    w, h = target_size
    tx, ty = target_pos
    sw, sh = svg_size

    return [
        transform_x(complex_point.real, tx, w, sw),
        transform_y(complex_point.imag, ty, h, sh, flip_y),
    ]


def bezier_points(
    bezier: CubicBezier,
    target_size: Tuple[float, float],
    target_pos: Tuple[float, float],
    svg_size: Tuple[float, float],
    flip_y: bool = True,
) -> List[float]:
    """
    Convert a CubicBezier to target-compatible bezier points.

    Args:
        bezier: CubicBezier object
        target_size: (width, height) of target
        target_pos: (x, y) of target
        svg_size: (width, height) of SVG
        flip_y: Whether to flip the Y axis

    Returns:
        List of points [x1, y1, cx1, cy1, cx2, cy2, x2, y2]
    """
    return [
        *transform_point(bezier.start, target_size, target_pos, svg_size, flip_y),
        *transform_point(bezier.control1, target_size, target_pos, svg_size, flip_y),
        *transform_point(bezier.control2, target_size, target_pos, svg_size, flip_y),
        *transform_point(bezier.end, target_size, target_pos, svg_size, flip_y),
    ]


def line_points(
    line: Line,
    target_size: Tuple[float, float],
    target_pos: Tuple[float, float],
    svg_size: Tuple[float, float],
    flip_y: bool = True,
) -> List[float]:
    """
    Convert a Line to target-compatible line points.

    Args:
        line: Line object
        target_size: (width, height) of target
        target_pos: (x, y) of target
        svg_size: (width, height) of SVG
        flip_y: Whether to flip the Y axis

    Returns:
        List of points [x1, y1, x2, y2]
    """
    return [
        *transform_point(line.start, target_size, target_pos, svg_size, flip_y),
        *transform_point(line.end, target_size, target_pos, svg_size, flip_y),
    ]


# Bernstein polynomials for Bezier calculation
# https://stackoverflow.com/a/15399173/8871954
B0_t = lambda t: (1 - t) ** 3
B1_t = lambda t: 3 * t * (1 - t) ** 2
B2_t = lambda t: 3 * t**2 * (1 - t)
B3_t = lambda t: t**3


def get_all_points(
    start: Tuple[float, float],
    control1: Tuple[float, float],
    control2: Tuple[float, float],
    end: Tuple[float, float],
    segments: int = 40,
) -> List[float]:
    """
    Generate discrete points along a cubic bezier curve.

    Args:
        start: Starting point (x, y)
        control1: First control point (x, y)
        control2: Second control point (x, y)
        end: End point (x, y)
        segments: Number of segments to generate

    Returns:
        Flattened list of points [x1, y1, x2, y2, ...]
    """
    points = []
    ax, ay = start
    bx, by = control1
    cx, cy = control2
    dx, dy = end

    seg = 1 / segments
    t = 0

    while t <= 1:
        points.extend(
            [
                (B0_t(t) * ax) + (B1_t(t) * bx) + (B2_t(t) * cx) + (B3_t(t) * dx),
                (B0_t(t) * ay) + (B1_t(t) * by) + (B2_t(t) * cy) + (B3_t(t) * dy),
            ]
        )
        t += seg

    return points


def find_center(sorted_list: List[float]) -> float:
    """
    Find the center value of a sorted list.

    Args:
        sorted_list: A sorted list of numbers

    Returns:
        The center value or average of the two middle values
    """
    middle = float(len(sorted_list)) / 2
    if middle % 2 != 0:
        return sorted_list[int(middle - 0.5)]
    else:
        return (sorted_list[int(middle)] + sorted_list[int(middle - 1)]) / 2
