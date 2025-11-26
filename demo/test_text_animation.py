#!/usr/bin/env python3
"""
Text Animation Demo - Handwriting-style text animation

This script demonstrates the text-to-SVG animation capabilities of Kivg
by creating animated text that appears as if being written by hand.

Usage:
    python test_text_animation.py                          # Default text
    python test_text_animation.py "Your custom text"       # Custom text
    python test_text_animation.py --output my_text.svg     # Custom output
"""

import argparse
import os
import sys
from pathlib import Path

# Add parent directory to path to import kivg
sys.path.insert(0, str(Path(__file__).parent.parent))

from kivg import TextToSVG, create_text_animation


def main():
    """Main function to run the text animation demo."""
    parser = argparse.ArgumentParser(
        description="Text Animation Demo - Create handwriting-style text animations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python test_text_animation.py                               # Default text
    python test_text_animation.py "Hello Kivg!"                 # Custom text
    python test_text_animation.py --font-size 60 "Big Text"     # Large text
    python test_text_animation.py --duration 5 "Slow writing"   # Slower animation
        """,
    )
    parser.add_argument(
        "text",
        nargs="?",
        default="Hello World!",
        help="Text to animate (default: 'Hello World!')",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="text_animation.svg",
        help="Output SVG file path (default: text_animation.svg)",
    )
    parser.add_argument(
        "--html-output",
        default=None,
        help="Also output HTML file with embedded animation",
    )
    parser.add_argument(
        "--font-family",
        default="sans-serif",
        help="Font family (default: sans-serif)",
    )
    parser.add_argument(
        "--font-size",
        type=float,
        default=40.0,
        help="Font size in points (default: 40)",
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
        help="Stroke color (default: #000000)",
    )
    parser.add_argument(
        "--stroke-width",
        type=float,
        default=2.0,
        help="Stroke width (default: 2.0)",
    )
    parser.add_argument(
        "--background",
        default="#ffffff",
        help="Background color (default: #ffffff)",
    )

    args = parser.parse_args()

    print("Kivg Text Animation Demo")
    print("=" * 50)
    print(f"Text:         '{args.text}'")
    print(f"Font:         {args.font_family} @ {args.font_size}pt")
    print(f"Duration:     {args.duration}s")
    print(f"Output:       {args.output}")
    print("=" * 50)

    # Create text converter
    converter = TextToSVG(
        font_family=args.font_family,
        font_size=args.font_size,
    )

    # Get text dimensions
    width, height = converter.get_text_dimensions(args.text)
    print(f"\nText dimensions: {width:.1f} x {height:.1f} pixels")

    # Create animated SVG
    print("\nGenerating animated SVG...")
    animated_svg = converter.create_animated_text_svg(
        args.text,
        duration=args.duration,
        stroke_color=args.stroke_color,
        stroke_width=args.stroke_width,
        background_color=args.background,
    )

    # Save SVG file
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(animated_svg)

    print(f"✓ SVG saved to: {args.output}")
    print(f"  File size: {os.path.getsize(args.output) / 1024:.1f} KiB")

    # Optionally create HTML wrapper
    if args.html_output:
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Text Animation - {args.text}</title>
    <style>
        body {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
            background: #f0f0f0;
            font-family: Arial, sans-serif;
        }}
        h1 {{
            color: #333;
            margin-bottom: 20px;
        }}
        .container {{
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        .reload-btn {{
            margin-top: 20px;
            padding: 10px 20px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }}
        .reload-btn:hover {{
            background: #0056b3;
        }}
    </style>
</head>
<body>
    <h1>Handwriting Animation Demo</h1>
    <div class="container">
{animated_svg}
    </div>
    <button class="reload-btn" onclick="location.reload()">
        Replay Animation
    </button>
</body>
</html>"""

        with open(args.html_output, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"✓ HTML saved to: {args.html_output}")

    print("\nTo view the animation:")
    print(f"  - Open {args.output} in a web browser")
    if args.html_output:
        print(f"  - Or open {args.html_output} for a styled demo page")

    print("\nDone!")


if __name__ == "__main__":
    main()
