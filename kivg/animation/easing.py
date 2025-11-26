"""
Animation easing functions for Kivg.
Pure Python implementation without Kivy dependency.
"""

from math import sqrt, cos, sin, pi


class AnimationTransition:
    """
    Collection of animation easing functions.

    These functions take a progress value (0-1) and return an eased value (0-1).
    Can be used with any animation system.
    """

    @staticmethod
    def linear(progress: float) -> float:
        """Linear transition (no easing)."""
        return progress

    @staticmethod
    def in_quad(progress: float) -> float:
        """Quadratic ease-in."""
        return progress * progress

    @staticmethod
    def out_quad(progress: float) -> float:
        """Quadratic ease-out."""
        return -1.0 * progress * (progress - 2.0)

    @staticmethod
    def in_out_quad(progress: float) -> float:
        """Quadratic ease-in-out."""
        p = progress * 2
        if p < 1:
            return 0.5 * p * p
        p -= 1.0
        return -0.5 * (p * (p - 2.0) - 1.0)

    @staticmethod
    def in_cubic(progress: float) -> float:
        """Cubic ease-in."""
        return progress * progress * progress

    @staticmethod
    def out_cubic(progress: float) -> float:
        """Cubic ease-out."""
        p = progress - 1.0
        return p * p * p + 1.0

    @staticmethod
    def in_out_cubic(progress: float) -> float:
        """Cubic ease-in-out."""
        p = progress * 2
        if p < 1:
            return 0.5 * p * p * p
        p -= 2
        return 0.5 * (p * p * p + 2.0)

    @staticmethod
    def in_quart(progress: float) -> float:
        """Quartic ease-in."""
        return progress * progress * progress * progress

    @staticmethod
    def out_quart(progress: float) -> float:
        """Quartic ease-out."""
        p = progress - 1.0
        return -1.0 * (p * p * p * p - 1.0)

    @staticmethod
    def in_out_quart(progress: float) -> float:
        """Quartic ease-in-out."""
        p = progress * 2
        if p < 1:
            return 0.5 * p * p * p * p
        p -= 2
        return -0.5 * (p * p * p * p - 2.0)

    @staticmethod
    def in_quint(progress: float) -> float:
        """Quintic ease-in."""
        return progress * progress * progress * progress * progress

    @staticmethod
    def out_quint(progress: float) -> float:
        """Quintic ease-out."""
        p = progress - 1.0
        return p * p * p * p * p + 1.0

    @staticmethod
    def in_out_quint(progress: float) -> float:
        """Quintic ease-in-out."""
        p = progress * 2
        if p < 1:
            return 0.5 * p * p * p * p * p
        p -= 2.0
        return 0.5 * (p * p * p * p * p + 2.0)

    @staticmethod
    def in_sine(progress: float) -> float:
        """Sinusoidal ease-in."""
        return -1.0 * cos(progress * (pi / 2.0)) + 1.0

    @staticmethod
    def out_sine(progress: float) -> float:
        """Sinusoidal ease-out."""
        return sin(progress * (pi / 2.0))

    @staticmethod
    def in_out_sine(progress: float) -> float:
        """Sinusoidal ease-in-out."""
        return -0.5 * (cos(pi * progress) - 1.0)

    @staticmethod
    def in_expo(progress: float) -> float:
        """Exponential ease-in."""
        if progress == 0:
            return 0.0
        return pow(2, 10 * (progress - 1.0))

    @staticmethod
    def out_expo(progress: float) -> float:
        """Exponential ease-out."""
        if progress == 1.0:
            return 1.0
        return -pow(2, -10 * progress) + 1.0

    @staticmethod
    def in_out_expo(progress: float) -> float:
        """Exponential ease-in-out."""
        if progress == 0:
            return 0.0
        if progress == 1.0:
            return 1.0
        p = progress * 2
        if p < 1:
            return 0.5 * pow(2, 10 * (p - 1.0))
        p -= 1.0
        return 0.5 * (-pow(2, -10 * p) + 2.0)

    @staticmethod
    def in_circ(progress: float) -> float:
        """Circular ease-in."""
        return -1.0 * (sqrt(1.0 - progress * progress) - 1.0)

    @staticmethod
    def out_circ(progress: float) -> float:
        """Circular ease-out."""
        p = progress - 1.0
        return sqrt(1.0 - p * p)

    @staticmethod
    def in_out_circ(progress: float) -> float:
        """Circular ease-in-out."""
        p = progress * 2
        if p < 1:
            return -0.5 * (sqrt(1.0 - p * p) - 1.0)
        p -= 2.0
        return 0.5 * (sqrt(1.0 - p * p) + 1.0)

    @staticmethod
    def in_elastic(progress: float) -> float:
        """Elastic ease-in."""
        p = 0.3
        s = p / 4.0
        q = progress
        if q == 1:
            return 1.0
        q -= 1.0
        return -(pow(2, 10 * q) * sin((q - s) * (2 * pi) / p))

    @staticmethod
    def out_elastic(progress: float) -> float:
        """Elastic ease-out."""
        p = 0.3
        s = p / 4.0
        q = progress
        if q == 1:
            return 1.0
        return pow(2, -10 * q) * sin((q - s) * (2 * pi) / p) + 1.0

    @staticmethod
    def in_out_elastic(progress: float) -> float:
        """Elastic ease-in-out."""
        p = 0.3 * 1.5
        s = p / 4.0
        q = progress * 2
        if q == 2:
            return 1.0
        if q < 1:
            q -= 1.0
            return -0.5 * (pow(2, 10 * q) * sin((q - s) * (2.0 * pi) / p))
        else:
            q -= 1.0
            return pow(2, -10 * q) * sin((q - s) * (2.0 * pi) / p) * 0.5 + 1.0

    @staticmethod
    def in_back(progress: float) -> float:
        """Back ease-in (overshoot)."""
        return progress * progress * ((1.70158 + 1.0) * progress - 1.70158)

    @staticmethod
    def out_back(progress: float) -> float:
        """Back ease-out (overshoot)."""
        p = progress - 1.0
        return p * p * ((1.70158 + 1) * p + 1.70158) + 1.0

    @staticmethod
    def in_out_back(progress: float) -> float:
        """Back ease-in-out (overshoot)."""
        p = progress * 2.0
        s = 1.70158 * 1.525
        if p < 1:
            return 0.5 * (p * p * ((s + 1.0) * p - s))
        p -= 2.0
        return 0.5 * (p * p * ((s + 1.0) * p + s) + 2.0)

    @staticmethod
    def _out_bounce_internal(t: float, d: float) -> float:
        """Internal helper for bounce calculations."""
        p = t / d
        if p < (1.0 / 2.75):
            return 7.5625 * p * p
        elif p < (2.0 / 2.75):
            p -= 1.5 / 2.75
            return 7.5625 * p * p + 0.75
        elif p < (2.5 / 2.75):
            p -= 2.25 / 2.75
            return 7.5625 * p * p + 0.9375
        else:
            p -= 2.625 / 2.75
            return 7.5625 * p * p + 0.984375

    @staticmethod
    def _in_bounce_internal(t: float, d: float) -> float:
        """Internal helper for bounce calculations."""
        return 1.0 - AnimationTransition._out_bounce_internal(d - t, d)

    @staticmethod
    def in_bounce(progress: float) -> float:
        """Bounce ease-in."""
        return AnimationTransition._in_bounce_internal(progress, 1.0)

    @staticmethod
    def out_bounce(progress: float) -> float:
        """Bounce ease-out."""
        return AnimationTransition._out_bounce_internal(progress, 1.0)

    @staticmethod
    def in_out_bounce(progress: float) -> float:
        """Bounce ease-in-out."""
        p = progress * 2.0
        if p < 1.0:
            return AnimationTransition._in_bounce_internal(p, 1.0) * 0.5
        return AnimationTransition._out_bounce_internal(p - 1.0, 1.0) * 0.5 + 0.5

    @classmethod
    def get_transition(cls, name: str):
        """
        Get an easing function by name.

        Args:
            name: Name of the easing function (e.g., 'out_quad', 'in_bounce')

        Returns:
            The easing function, or linear if not found
        """
        return getattr(cls, name, cls.linear)
