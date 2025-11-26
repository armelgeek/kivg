"""
Kivg - SVG drawing and animation with video export support

This library provides:
- SVG path parsing and manipulation
- Web-compatible SVG animations (CSS/JavaScript)
- Video export using FFmpeg
- Text to SVG path conversion for handwriting animations
"""

from .version import __version__
from .svg_parser import parse_svg
from .main import SVGAnimator
from .export import VideoExporter, WebAnimationExporter
from .text_to_svg import TextToSVG, text_to_svg, create_text_animation

__all__ = [
    "SVGAnimator",
    "parse_svg",
    "VideoExporter",
    "WebAnimationExporter",
    "TextToSVG",
    "text_to_svg",
    "create_text_animation",
    "__version__",
]
