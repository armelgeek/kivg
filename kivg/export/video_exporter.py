"""
Video exporter for Kivg.
Uses FFmpeg to export SVG animations as video files.
"""

import subprocess
import shutil
import os
import tempfile
from typing import List, Optional, Callable
from PIL import Image
import io

try:
    import cairosvg

    CAIROSVG_AVAILABLE = True
except ImportError:
    CAIROSVG_AVAILABLE = False


class VideoExporter:
    """
    Export SVG animations as video files using FFmpeg.

    This class generates frames from SVG path animations and combines them
    into a video file using FFmpeg.
    """

    def __init__(self, width: int = 800, height: int = 600, fps: int = 30):
        """
        Initialize the video exporter.

        Args:
            width: Video width in pixels
            height: Video height in pixels
            fps: Frames per second
        """
        self.width = width
        self.height = height
        self.fps = fps
        self._check_ffmpeg()

    def _check_ffmpeg(self) -> bool:
        """Check if FFmpeg is available on the system."""
        self.ffmpeg_path = shutil.which("ffmpeg")
        if not self.ffmpeg_path:
            raise RuntimeError(
                "FFmpeg not found. Please install FFmpeg to use video export. "
                "Visit https://ffmpeg.org/download.html for installation instructions."
            )
        return True

    def svg_to_frame(self, svg_content: str) -> Image.Image:
        """
        Convert SVG content to a PIL Image frame.

        Args:
            svg_content: SVG markup string

        Returns:
            PIL Image object
        """
        if not CAIROSVG_AVAILABLE:
            raise ImportError(
                "CairoSVG is required for video export. "
                "Install with: pip install cairosvg"
            )

        # Convert SVG to PNG bytes
        png_data = cairosvg.svg2png(
            bytestring=svg_content.encode("utf-8"),
            output_width=self.width,
            output_height=self.height,
        )

        # Load as PIL Image
        return Image.open(io.BytesIO(png_data))

    def export_frames_to_video(
        self,
        frames: List[Image.Image],
        output_path: str,
        codec: str = "libx264",
        quality: int = 23,
    ) -> str:
        """
        Export a list of PIL Image frames to a video file.

        Args:
            frames: List of PIL Image frames
            output_path: Path to output video file
            codec: Video codec to use (default: libx264)
            quality: Video quality (0-51, lower is better, default: 23)

        Returns:
            Path to the created video file
        """
        if not frames:
            raise ValueError("No frames provided for video export")

        # Create temporary directory for frames
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save frames as PNG images
            for i, frame in enumerate(frames):
                frame_path = os.path.join(temp_dir, f"frame_{i:06d}.png")
                frame.save(frame_path, "PNG")

            # Build FFmpeg command
            input_pattern = os.path.join(temp_dir, "frame_%06d.png")

            cmd = [
                self.ffmpeg_path,
                "-y",  # Overwrite output file
                "-framerate",
                str(self.fps),
                "-i",
                input_pattern,
                "-c:v",
                codec,
                "-crf",
                str(quality),
                "-pix_fmt",
                "yuv420p",  # Compatibility
                output_path,
            ]

            # Run FFmpeg
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode != 0:
                raise RuntimeError(f"FFmpeg error: {result.stderr}")

        return output_path

    def export_svg_animation(
        self,
        svg_frames: List[str],
        output_path: str,
        codec: str = "libx264",
        quality: int = 23,
        on_progress: Optional[Callable[[int, int], None]] = None,
    ) -> str:
        """
        Export SVG animation frames to a video file.

        Args:
            svg_frames: List of SVG content strings (one per frame)
            output_path: Path to output video file
            codec: Video codec to use
            quality: Video quality (0-51, lower is better)
            on_progress: Optional callback(current_frame, total_frames)

        Returns:
            Path to the created video file
        """
        frames = []
        total = len(svg_frames)

        for i, svg_content in enumerate(svg_frames):
            frame = self.svg_to_frame(svg_content)
            frames.append(frame)

            if on_progress:
                on_progress(i + 1, total)

        return self.export_frames_to_video(frames, output_path, codec, quality)
