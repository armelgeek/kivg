"""
Text to SVG conversion for Kivg.
Converts text to SVG paths for handwriting-style animation.
"""

import io
import re
from typing import List, Tuple, Dict, Any, Optional
from xml.dom import minidom

try:
    import cairocffi as cairo
except ImportError:
    cairo = None


class TextToSVG:
    """
    Convert text to SVG paths for animation.

    Uses Cairo to render text as paths, enabling handwriting-style
    animations of text content.
    """

    # Font style constants
    FONT_SLANT_NORMAL = "normal"
    FONT_SLANT_ITALIC = "italic"
    FONT_SLANT_OBLIQUE = "oblique"

    FONT_WEIGHT_NORMAL = "normal"
    FONT_WEIGHT_BOLD = "bold"

    def __init__(
        self,
        font_family: str = "sans-serif",
        font_size: float = 40.0,
        font_slant: str = "normal",
        font_weight: str = "normal",
    ):
        """
        Initialize the text-to-SVG converter.

        Args:
            font_family: Font family name (e.g., "sans-serif", "serif", "monospace")
            font_size: Font size in points
            font_slant: Font slant ("normal", "italic", or "oblique")
            font_weight: Font weight ("normal" or "bold")
        """
        if cairo is None:
            raise ImportError(
                "cairocffi is required for text-to-SVG conversion. "
                "Install it with: pip install cairocffi"
            )

        self.font_family = font_family
        self.font_size = font_size
        self.font_slant = font_slant
        self.font_weight = font_weight

    def _get_cairo_font_slant(self) -> int:
        """Get the Cairo font slant constant."""
        slant_map = {
            "normal": cairo.FONT_SLANT_NORMAL,
            "italic": cairo.FONT_SLANT_ITALIC,
            "oblique": cairo.FONT_SLANT_OBLIQUE,
        }
        return slant_map.get(self.font_slant, cairo.FONT_SLANT_NORMAL)

    def _get_cairo_font_weight(self) -> int:
        """Get the Cairo font weight constant."""
        weight_map = {
            "normal": cairo.FONT_WEIGHT_NORMAL,
            "bold": cairo.FONT_WEIGHT_BOLD,
        }
        return weight_map.get(self.font_weight, cairo.FONT_WEIGHT_NORMAL)

    def get_text_dimensions(self, text: str) -> Tuple[float, float]:
        """
        Calculate the dimensions needed to render the text.

        Args:
            text: The text to measure

        Returns:
            Tuple of (width, height) in pixels
        """
        # Create a temporary surface to measure text
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1, 1)
        ctx = cairo.Context(surface)

        ctx.select_font_face(
            self.font_family,
            self._get_cairo_font_slant(),
            self._get_cairo_font_weight(),
        )
        ctx.set_font_size(self.font_size)

        # text_extents returns (x_bearing, y_bearing, width, height, x_advance, y_advance)
        extents = ctx.text_extents(text)
        x_advance = extents[4]  # x_advance is the 5th element

        # Add some padding
        width = x_advance + 20
        height = self.font_size * 1.5 + 20

        surface.finish()
        return (width, height)

    def text_to_svg_paths(
        self,
        text: str,
        x: float = 10.0,
        y: float = None,
        stroke_color: str = "#000000",
        stroke_width: float = 2.0,
        fill_color: str = "none",
    ) -> str:
        """
        Convert text to SVG path data.

        Args:
            text: The text to convert
            x: X position for the text
            y: Y position for the text baseline (if None, calculated automatically)
            stroke_color: Stroke color for the paths
            stroke_width: Stroke width for the paths
            fill_color: Fill color for the paths (use "none" for outline only)

        Returns:
            SVG content string with path elements
        """
        # Calculate dimensions
        width, height = self.get_text_dimensions(text)

        if y is None:
            y = height - 10  # Position baseline near bottom with padding

        # Create SVG surface
        svg_io = io.BytesIO()
        surface = cairo.SVGSurface(svg_io, width, height)
        ctx = cairo.Context(surface)

        # Set font
        ctx.select_font_face(
            self.font_family,
            self._get_cairo_font_slant(),
            self._get_cairo_font_weight(),
        )
        ctx.set_font_size(self.font_size)

        # Convert text to path
        ctx.move_to(x, y)
        ctx.text_path(text)

        # Set stroke properties
        ctx.set_line_width(stroke_width)
        ctx.stroke()

        surface.finish()

        # Get SVG content
        svg_content = svg_io.getvalue().decode("utf-8")

        return svg_content

    def extract_paths_from_svg(self, svg_content: str) -> List[Dict[str, Any]]:
        """
        Extract path data from SVG content.

        Args:
            svg_content: SVG content string

        Returns:
            List of path dictionaries with 'd', 'fill', and 'stroke' keys
        """
        paths = []

        try:
            doc = minidom.parseString(svg_content)

            for path in doc.getElementsByTagName("path"):
                d = path.getAttribute("d")
                fill = path.getAttribute("fill") or "none"
                stroke = path.getAttribute("stroke") or "#000000"

                if d:  # Only include paths with path data
                    paths.append({"d": d, "fill": fill, "stroke": stroke})

            doc.unlink()
        except Exception:
            pass

        return paths

    def text_to_path_data(
        self,
        text: str,
        x: float = 10.0,
        y: float = None,
    ) -> Tuple[List[float], List[Dict[str, Any]]]:
        """
        Convert text to path data for animation.

        Args:
            text: The text to convert
            x: X position for the text
            y: Y position for the text baseline (if None, calculated automatically)

        Returns:
            Tuple of (svg_size, paths) where:
                - svg_size: [width, height] of the SVG
                - paths: List of path dictionaries
        """
        svg_content = self.text_to_svg_paths(text, x, y)
        paths = self.extract_paths_from_svg(svg_content)

        # Extract viewBox dimensions
        width, height = self.get_text_dimensions(text)

        return [width, height], paths

    def create_animated_text_svg(
        self,
        text: str,
        duration: float = 2.0,
        stroke_color: str = "#000000",
        stroke_width: float = 2.0,
        fill_after_draw: bool = False,
        fill_color: str = "#000000",
        background_color: str = "#ffffff",
    ) -> str:
        """
        Create an SVG with animated text (handwriting effect).

        Args:
            text: The text to animate
            duration: Animation duration in seconds
            stroke_color: Stroke color during animation
            stroke_width: Stroke width
            fill_after_draw: Whether to fill the text after animation
            fill_color: Fill color after animation
            background_color: Background color

        Returns:
            Complete SVG string with CSS animation
        """
        svg_size, paths = self.text_to_path_data(text)

        if not paths:
            # Return empty SVG if no paths
            return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="{svg_size[0]}" height="{svg_size[1]}"
     viewBox="0 0 {svg_size[0]} {svg_size[1]}">
  <rect width="100%" height="100%" fill="{background_color}"/>
</svg>"""

        # Build path elements
        path_elements = []
        dash_length = 10000  # Should be larger than any path length

        for i, path_data in enumerate(paths):
            d = path_data.get("d", "")
            fill = fill_color if fill_after_draw else "none"

            path_elements.append(
                f'    <path id="text-path-{i}" d="{d}" '
                f'fill="{fill}" stroke="{stroke_color}" '
                f'stroke-width="{stroke_width}" class="animate-text"/>'
            )

        paths_str = "\n".join(path_elements)

        svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="{svg_size[0]}" height="{svg_size[1]}"
     viewBox="0 0 {svg_size[0]} {svg_size[1]}">
  <style>
    .animate-text {{
      stroke-dasharray: {dash_length};
      stroke-dashoffset: {dash_length};
      animation: draw-text {duration}s ease forwards;
    }}

    @keyframes draw-text {{
      to {{
        stroke-dashoffset: 0;
      }}
    }}
  </style>
  <rect width="100%" height="100%" fill="{background_color}"/>
{paths_str}
</svg>"""

        return svg


def text_to_svg(
    text: str,
    font_family: str = "sans-serif",
    font_size: float = 40.0,
    font_slant: str = "normal",
    font_weight: str = "normal",
) -> str:
    """
    Convenience function to convert text to SVG paths.

    Args:
        text: The text to convert
        font_family: Font family name
        font_size: Font size in points
        font_slant: Font slant ("normal", "italic", or "oblique")
        font_weight: Font weight ("normal" or "bold")

    Returns:
        SVG content string
    """
    converter = TextToSVG(
        font_family=font_family,
        font_size=font_size,
        font_slant=font_slant,
        font_weight=font_weight,
    )
    return converter.text_to_svg_paths(text)


def create_text_animation(
    text: str,
    duration: float = 2.0,
    font_family: str = "sans-serif",
    font_size: float = 40.0,
    stroke_color: str = "#000000",
    stroke_width: float = 2.0,
    background_color: str = "#ffffff",
) -> str:
    """
    Convenience function to create animated text SVG.

    Args:
        text: The text to animate
        duration: Animation duration in seconds
        font_family: Font family name
        font_size: Font size in points
        stroke_color: Stroke color
        stroke_width: Stroke width
        background_color: Background color

    Returns:
        SVG content string with animation
    """
    converter = TextToSVG(font_family=font_family, font_size=font_size)
    return converter.create_animated_text_svg(
        text,
        duration=duration,
        stroke_color=stroke_color,
        stroke_width=stroke_width,
        background_color=background_color,
    )
