## Kivg
*SVG path drawing and animation with web and video export support*

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/shashi278/kivg/.github%2Fworkflows%2Fpython-publish.yml) [![Python 3.8](https://img.shields.io/pypi/pyversions/kivymd)](https://www.python.org/downloads/release/python-380/) [![pypi](https://img.shields.io/pypi/v/kivg)](https://pypi.org/project/Kivg/) [![code size](https://img.shields.io/github/languages/code-size/shashi278/svg-anim-kivy)]() [![license](https://img.shields.io/github/license/shashi278/svg-anim-kivy)](https://github.com/shashi278/svg-anim-kivy/blob/main/LICENSE) [![downloads](https://img.shields.io/pypi/dm/kivg)](https://pypi.org/project/Kivg/) ![Pepy Total Downloads](https://img.shields.io/pepy/dt/kivg?label=Total%20Downloads)


#

## Features

- **SVG Parsing**: Parse SVG files and extract path data
- **Web Animations**: Export SVG animations as HTML with CSS or JavaScript
- **Video Export**: Convert SVG animations to video files using FFmpeg
- **Cross-Platform**: Works on any platform with Python support
- **No GUI Dependencies**: Pure Python implementation, works in headless environments

#

## Install
```bash
pip install kivg
```

### Requirements
- Python 3.8+
- FFmpeg (for video export) - [Download FFmpeg](https://ffmpeg.org/download.html)

## Usage Guide

### Basic Usage

```python
from kivg import SVGAnimator

# Create an animator
animator = SVGAnimator(width=800, height=600)

# Load an SVG file
animator.load_svg("my_drawing.svg")

# Export as web animation (HTML with CSS)
animator.export_to_web("animation.html", method="css", duration=2.0)

# Export as video (requires FFmpeg)
animator.export_to_video("animation.mp4", fps=30, duration=2.0)
```

### Web Animation Export

Kivg supports three types of web animations:

#### CSS Animation
```python
animator.export_to_web(
    "animation.html",
    method="css",        # Use CSS @keyframes
    duration=2.0,        # Animation duration in seconds
    fill=True,           # Fill paths after drawing
    stroke_color="#000", # Stroke color during animation
    stroke_width=2       # Stroke width
)
```

#### JavaScript Animation
```python
animator.export_to_web(
    "animation.html",
    method="js",         # Use requestAnimationFrame
    duration=2.0,
    fill=True,
    stroke_color="#000",
    stroke_width=2
)
```

#### SMIL Animation (Standalone SVG)
```python
animator.export_to_web(
    "animation.svg",
    method="smil",       # Use SVG SMIL animations
    duration=2.0,
    fill=True
)
```

### Video Export

Export animations as video files using FFmpeg:

```python
animator.export_to_video(
    "animation.mp4",
    fps=30,              # Frames per second
    duration=2.0,        # Animation duration
    fill=True,           # Fill paths after drawing
    stroke_color="#000", # Stroke color
    stroke_width=2,      # Stroke width
    background_color="#ffffff",  # Background color
    codec="libx264",     # Video codec
    quality=23,          # Quality (0-51, lower is better)
    on_progress=lambda current, total: print(f"{current}/{total}")
)
```

### Direct Exporter Usage

You can also use the exporters directly:

```python
from kivg import VideoExporter, WebAnimationExporter

# Web exporter
web_exporter = WebAnimationExporter(width=800, height=600)
html = web_exporter.generate_css_animation(
    svg_paths=[{"d": "M10 10 L100 100", "fill": "#ff0000"}],
    duration=2.0
)

# Video exporter
video_exporter = VideoExporter(width=800, height=600, fps=30)
video_exporter.export_svg_animation(svg_frames, "output.mp4")
```

### SVG Parsing Only

If you just need to parse SVG files:

```python
from kivg import parse_svg

# Parse an SVG file
svg_size, path_strings = parse_svg("my_drawing.svg")
# svg_size: [width, height]
# path_strings: List of (path_data, id, color) tuples
```

### Text to SVG Animation

Create handwriting-style text animations:

```python
from kivg import TextToSVG, create_text_animation

# Quick method - create animated text SVG
svg = create_text_animation(
    "Hello World!",
    duration=2.0,          # Animation duration in seconds
    font_size=40.0,        # Font size in points
    stroke_color="#000000" # Stroke color
)

# Save to file
with open("text_animation.svg", "w") as f:
    f.write(svg)

# Advanced usage with TextToSVG class
converter = TextToSVG(
    font_family="sans-serif",  # Font family
    font_size=50.0,            # Font size
    font_slant="italic",       # normal, italic, or oblique
    font_weight="bold"         # normal or bold
)

# Get text dimensions
width, height = converter.get_text_dimensions("My Text")

# Create animated SVG with more options
svg = converter.create_animated_text_svg(
    "My Text",
    duration=3.0,
    stroke_color="#ff0000",
    stroke_width=2.0,
    fill_after_draw=True,      # Fill text after animation
    fill_color="#000000",
    background_color="#ffffff"
)
```

## Project Structure

```
kivg/
├── __init__.py         # Package entry point
├── main.py             # SVGAnimator class
├── path_utils.py       # SVG path utilities
├── svg_parser.py       # SVG parsing functionality
├── text_to_svg.py      # Text to SVG conversion
├── version.py          # Version information
├── animation/          # Animation utilities
│   └── easing.py       # Easing functions
├── drawing/            # Drawing utilities
└── export/             # Export functionality
    ├── video_exporter.py   # FFmpeg video export
    └── web_exporter.py     # HTML/CSS/JS export
```

## Changelog

**v2.1**
* Added text-to-SVG conversion for handwriting-style animations
* New `TextToSVG` class for converting text to animated SVG paths
* New `create_text_animation()` convenience function
* Demo for text animation (`demo/test_text_animation.py`)

**v2.0**
* Complete rewrite - removed Kivy dependency
* Added web animation export (CSS/JavaScript/SMIL)
* Added video export using FFmpeg
* Works in headless environments
* Cross-platform support

**v1.1**
* Fixed crashing when SVG size is not int

**v1.0**
* Shape animation feature added
* Added `anim_type` in draw method

## Contributing

![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)

We welcome contributions! Here's how you can help:

1. **Bug fixes**: If you find a bug, please open an issue or submit a pull request with a fix
2. **Feature additions**: Have an idea for a new feature? Open an issue to discuss it
3. **Documentation**: Improvements to documentation are always appreciated
4. **Examples**: Add more example use cases to help others learn

Please make sure to test your changes before submitting a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/shashi278/svg-anim-kivy/blob/main/LICENSE) file for details.
