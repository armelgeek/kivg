"""
Kivg - SVG drawing and animation with video export support

This library provides:
- SVG path parsing and manipulation
- Web-compatible SVG animations (CSS/JavaScript)
- Video export using FFmpeg
"""

from .version import __version__
from .svg_parser import parse_svg
from .main import SVGAnimator
from .export import VideoExporter, WebAnimationExporter

__all__ = [
    "SVGAnimator",
    "parse_svg",
    "VideoExporter",
    "WebAnimationExporter",
    "__version__",
]
