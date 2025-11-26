"""
Kivg - SVG drawing and animation
Core class and main API (Kivy-free implementation)
"""

from collections import OrderedDict
from typing import List, Tuple, Dict, Any, Callable, Optional

from .svg_parser import parse_svg
from .path_utils import get_all_points, bezier_points, line_points
from .export import VideoExporter, WebAnimationExporter

from svg.path import parse_path
from svg.path.path import Line, CubicBezier, Close, Move


class SVGAnimator:
    """
    Main class for processing and animating SVG files.

    This class provides methods to parse SVG files and export them
    as web animations or video files.
    """

    # Default stroke dash length for animations (should be larger than any path length)
    DEFAULT_DASH_LENGTH = 10000

    def __init__(self, width: int = 800, height: int = 600):
        """
        Initialize the SVG animator.

        Args:
            width: Output width in pixels
            height: Output height in pixels
        """
        self.width = width
        self.height = height
        self._fill = True
        self._line_width = 2
        self._line_color = "#000000"
        self._animation_duration = 2.0

        # Parsed data
        self.svg_size = []
        self.closed_shapes = OrderedDict()
        self.path = []
        self.current_svg_file = ""

        # Exporters
        self._video_exporter = None
        self._web_exporter = None

    @property
    def video_exporter(self) -> VideoExporter:
        """Get or create the video exporter."""
        if self._video_exporter is None:
            self._video_exporter = VideoExporter(self.width, self.height)
        return self._video_exporter

    @property
    def web_exporter(self) -> WebAnimationExporter:
        """Get or create the web animation exporter."""
        if self._web_exporter is None:
            self._web_exporter = WebAnimationExporter(self.width, self.height)
        return self._web_exporter

    def load_svg(self, svg_file: str) -> Dict[str, Any]:
        """
        Load and parse an SVG file.

        Args:
            svg_file: Path to the SVG file

        Returns:
            Dictionary with parsed SVG data
        """
        self.current_svg_file = svg_file
        self.svg_size, path_strings = parse_svg(svg_file)

        self.path = []
        self.closed_shapes = OrderedDict()

        for path_string, id_, clr in path_strings:
            move_found = False
            tmp = []
            self.closed_shapes[id_] = dict()
            self.closed_shapes[id_][id_ + "paths"] = []
            self.closed_shapes[id_][id_ + "shapes"] = []
            self.closed_shapes[id_]["color"] = clr
            self.closed_shapes[id_]["d"] = path_string

            _path = parse_path(path_string)
            for e in _path:
                self.path.append(e)

                if isinstance(e, Close) or (isinstance(e, Move) and move_found):
                    self.closed_shapes[id_][id_ + "paths"].append(tmp)
                    move_found = False

                if isinstance(e, Move):
                    tmp = []
                    move_found = True

                if not isinstance(e, Move) and move_found:
                    tmp.append(e)

        return {
            "svg_size": self.svg_size,
            "shapes": self.closed_shapes,
            "path_count": len(self.path),
        }

    def get_paths(self) -> List[Dict[str, Any]]:
        """
        Get all paths from the loaded SVG.

        Returns:
            List of path dictionaries with 'd' and 'fill' keys
        """
        paths = []
        for id_, shape_data in self.closed_shapes.items():
            color = shape_data.get("color", [1, 1, 1, 1])
            # Convert RGBA list to hex color
            r, g, b = int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)
            hex_color = f"#{r:02x}{g:02x}{b:02x}"

            paths.append({"id": id_, "d": shape_data.get("d", ""), "fill": hex_color})
        return paths

    def export_to_web(
        self,
        output_file: str,
        method: str = "css",
        duration: float = 2.0,
        fill: bool = True,
        stroke_color: str = "#000000",
        stroke_width: int = 2,
    ) -> str:
        """
        Export the loaded SVG as a web animation.

        Args:
            output_file: Path to output HTML file
            method: Animation method ('css', 'js', or 'smil')
            duration: Animation duration in seconds
            fill: Whether to fill paths after drawing
            stroke_color: Color of the stroke during animation
            stroke_width: Width of the stroke

        Returns:
            Path to the created file
        """
        paths = self.get_paths()

        if method == "css":
            html = self.web_exporter.generate_css_animation(
                paths, duration, fill, stroke_color, stroke_width
            )
        elif method == "js":
            html = self.web_exporter.generate_js_animation(
                paths, duration, fill, stroke_color, stroke_width
            )
        elif method == "smil":
            html = self.web_exporter.generate_svg_smil(
                paths, duration, fill, stroke_color, stroke_width
            )
        else:
            raise ValueError(f"Unknown animation method: {method}")

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html)

        return output_file

    def generate_animation_frames(
        self,
        num_frames: int = 60,
        duration: float = 2.0,
        fill: bool = True,
        stroke_color: str = "#000000",
        stroke_width: int = 2,
        background_color: str = "#ffffff",
        dash_length: int = None,
    ) -> List[str]:
        """
        Generate SVG frames for animation.

        Args:
            num_frames: Number of frames to generate
            duration: Total animation duration in seconds
            fill: Whether to fill paths after drawing
            stroke_color: Color of the stroke during animation
            stroke_width: Width of the stroke
            background_color: Background color
            dash_length: Length of dash array for animation (should be >= path length)

        Returns:
            List of SVG content strings (one per frame)
        """
        paths = self.get_paths()
        frames = []
        dash_len = dash_length or self.DEFAULT_DASH_LENGTH

        for frame_idx in range(num_frames):
            progress = frame_idx / max(num_frames - 1, 1)

            # Generate SVG for this frame
            path_elements = []
            for path_data in paths:
                d = path_data.get("d", "")
                path_fill = path_data.get("fill", "#ffffff") if fill else "none"

                # Simple dash animation simulation
                dash_offset = dash_len * (1 - progress)

                path_elements.append(
                    f'  <path d="{d}" fill="{path_fill}" '
                    f'stroke="{stroke_color}" stroke-width="{stroke_width}" '
                    f'stroke-dasharray="{dash_len}" stroke-dashoffset="{dash_offset:.2f}" />'
                )

            paths_str = "\n".join(path_elements)

            svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" 
     width="{self.width}" height="{self.height}" 
     viewBox="0 0 {self.svg_size[0]} {self.svg_size[1]}">
  <rect width="100%" height="100%" fill="{background_color}"/>
{paths_str}
</svg>"""

            frames.append(svg)

        return frames

    def export_to_video(
        self,
        output_file: str,
        fps: int = 30,
        duration: float = 2.0,
        fill: bool = True,
        stroke_color: str = "#000000",
        stroke_width: int = 2,
        background_color: str = "#ffffff",
        codec: str = "libx264",
        quality: int = 23,
        on_progress: Optional[Callable[[int, int], None]] = None,
    ) -> str:
        """
        Export the loaded SVG animation as a video file.

        Args:
            output_file: Path to output video file (e.g., 'animation.mp4')
            fps: Frames per second
            duration: Animation duration in seconds
            fill: Whether to fill paths after drawing
            stroke_color: Color of the stroke during animation
            stroke_width: Width of the stroke
            background_color: Background color
            codec: Video codec to use
            quality: Video quality (0-51, lower is better)
            on_progress: Optional callback(current_frame, total_frames)

        Returns:
            Path to the created video file
        """
        num_frames = int(fps * duration)

        frames = self.generate_animation_frames(
            num_frames=num_frames,
            duration=duration,
            fill=fill,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            background_color=background_color,
        )

        # Update video exporter settings
        self.video_exporter.fps = fps
        self.video_exporter.width = self.width
        self.video_exporter.height = self.height

        return self.video_exporter.export_svg_animation(
            frames, output_file, codec, quality, on_progress
        )


# Alias for backward compatibility
Kivg = SVGAnimator
