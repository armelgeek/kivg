#!/usr/bin/env python3
"""
Kivg Demo - SVG Animation to Video Export

This script demonstrates the SVG animation capabilities of Kivg
by exporting an animated SVG as a video file.

Usage:
    python main.py [svg_file] [output_video]
    python main.py                           # Uses default kivy.svg icon
    python main.py icons/github.svg          # Animate github icon
    python main.py icons/kivy.svg output.mp4 # Custom output path
"""

import argparse
import os
import sys

# Add parent directory to path to import kivg
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kivg import SVGAnimator


def progress_callback(current: int, total: int) -> None:
    """Display progress during video generation."""
    percent = (current / total) * 100
    bar_length = 40
    filled = int(bar_length * current / total)
    bar = "=" * filled + "-" * (bar_length - filled)
    print(f"\rGenerating frames: [{bar}] {percent:.1f}% ({current}/{total})", end="")
    if current == total:
        print()  # New line when complete


def main():
    """Main function to run the SVG to video demo."""
    parser = argparse.ArgumentParser(
        description="Kivg Demo - Export SVG animation as video",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python main.py                           # Uses default kivy.svg icon
    python main.py icons/github.svg          # Animate github icon
    python main.py icons/kivy.svg output.mp4 # Custom output path
    python main.py --duration 3 --fps 60 icons/python2.svg  # Custom settings
        """,
    )
    parser.add_argument(
        "svg_file",
        nargs="?",
        default="icons/kivy.svg",
        help="Path to the SVG file (default: icons/kivy.svg)",
    )
    parser.add_argument(
        "output",
        nargs="?",
        default=None,
        help="Output video file path (default: <svg_name>_animation.mp4)",
    )
    parser.add_argument(
        "--width", type=int, default=512, help="Video width in pixels (default: 512)"
    )
    parser.add_argument(
        "--height", type=int, default=512, help="Video height in pixels (default: 512)"
    )
    parser.add_argument(
        "--fps", type=int, default=30, help="Frames per second (default: 30)"
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=2.0,
        help="Animation duration in seconds (default: 2.0)",
    )
    parser.add_argument(
        "--stroke-color",
        default="#000000",
        help="Stroke color during animation (default: #000000)",
    )
    parser.add_argument(
        "--stroke-width",
        type=int,
        default=2,
        help="Stroke width (default: 2)",
    )
    parser.add_argument(
        "--background",
        default="#ffffff",
        help="Background color (default: #ffffff)",
    )
    parser.add_argument(
        "--no-fill",
        action="store_true",
        help="Don't fill paths after drawing",
    )
    parser.add_argument(
        "--quality",
        type=int,
        default=23,
        help="Video quality (0-51, lower is better, default: 23)",
    )

    args = parser.parse_args()

    # Resolve SVG file path relative to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    svg_path = args.svg_file
    if not os.path.isabs(svg_path):
        svg_path = os.path.join(script_dir, svg_path)

    # Check if SVG file exists
    if not os.path.exists(svg_path):
        print(f"Error: SVG file not found: {svg_path}")
        print("\nAvailable icons in demo/icons/:")
        icons_dir = os.path.join(script_dir, "icons")
        if os.path.exists(icons_dir):
            for icon in sorted(os.listdir(icons_dir)):
                if icon.endswith(".svg"):
                    print(f"  - icons/{icon}")
        sys.exit(1)

    # Determine output path
    if args.output:
        output_path = args.output
    else:
        svg_name = os.path.splitext(os.path.basename(args.svg_file))[0]
        output_path = f"{svg_name}_animation.mp4"

    print(f"Kivg Demo - SVG Animation to Video Export")
    print(f"=" * 50)
    print(f"Input SVG:    {svg_path}")
    print(f"Output video: {output_path}")
    print(f"Resolution:   {args.width}x{args.height}")
    print(f"Duration:     {args.duration}s at {args.fps} FPS")
    print(f"Fill paths:   {not args.no_fill}")
    print(f"=" * 50)

    # Create animator and load SVG
    animator = SVGAnimator(width=args.width, height=args.height)

    print(f"\nLoading SVG...")
    info = animator.load_svg(svg_path)
    print(f"  SVG size: {info['svg_size']}")
    print(f"  Paths found: {info['path_count']}")
    print(f"  Shapes: {len(info['shapes'])}")

    print(f"\nExporting video...")
    try:
        output_file = animator.export_to_video(
            output_file=output_path,
            fps=args.fps,
            duration=args.duration,
            fill=not args.no_fill,
            stroke_color=args.stroke_color,
            stroke_width=args.stroke_width,
            background_color=args.background,
            quality=args.quality,
            on_progress=progress_callback,
        )
        print(f"\nSuccess! Video saved to: {output_file}")
        print(f"File size: {os.path.getsize(output_file) / 1024:.1f} KB")
    except RuntimeError as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
