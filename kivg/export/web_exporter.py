"""
Web animation exporter for Kivg.
Generates web-compatible SVG animations using CSS or JavaScript.
"""

from typing import List, Dict, Optional, Any
import json

# Default stroke dash length for animations (should be larger than any path length)
DEFAULT_DASH_LENGTH = 10000


class WebAnimationExporter:
    """
    Export SVG animations as web-compatible HTML/CSS/JavaScript.

    Supports two animation methods:
    - CSS animations (using @keyframes and stroke-dasharray)
    - JavaScript animations (using requestAnimationFrame)
    """

    def __init__(self, width: int = 800, height: int = 600):
        """
        Initialize the web animation exporter.

        Args:
            width: SVG width in pixels
            height: SVG height in pixels
        """
        self.width = width
        self.height = height

    def generate_css_animation(
        self,
        svg_paths: List[Dict[str, Any]],
        duration: float = 2.0,
        fill: bool = True,
        stroke_color: str = "#000000",
        stroke_width: int = 2,
        dash_length: int = None,
    ) -> str:
        """
        Generate HTML with CSS-animated SVG paths.

        Uses the stroke-dasharray and stroke-dashoffset technique for
        path drawing animation.

        Args:
            svg_paths: List of path dicts with 'd' (path data) and optional 'fill' color
            duration: Animation duration in seconds
            fill: Whether to fill paths after drawing
            stroke_color: Color of the stroke during animation
            stroke_width: Width of the stroke
            dash_length: Length of dash array for animation (should be >= path length)

        Returns:
            HTML string with embedded CSS animations
        """
        # Handle empty paths list
        if not svg_paths:
            return self._generate_empty_html()

        dash_len = dash_length or DEFAULT_DASH_LENGTH

        # Generate unique IDs for each path
        path_elements = []
        css_rules = []

        for i, path_data in enumerate(svg_paths):
            path_id = f"path_{i}"
            d = path_data.get("d", "")
            path_fill = path_data.get("fill", "#ffffff") if fill else "none"

            # Path element
            path_elements.append(
                f'    <path id="{path_id}" d="{d}" '
                f'fill="{path_fill}" stroke="{stroke_color}" '
                f'stroke-width="{stroke_width}" class="animate-path" />'
            )

            # Delay each path slightly for sequential animation
            delay = i * (duration / len(svg_paths))
            css_rules.append(
                f"""
  #{path_id} {{
    animation-delay: {delay:.2f}s;
  }}"""
            )

        paths_str = "\n".join(path_elements)
        css_delays = "".join(css_rules)

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SVG Animation</title>
  <style>
    .animate-path {{
      stroke-dasharray: {dash_len};
      stroke-dashoffset: {dash_len};
      animation: draw {duration}s ease forwards;
    }}
    
    @keyframes draw {{
      to {{
        stroke-dashoffset: 0;
      }}
    }}
{css_delays}
  </style>
</head>
<body>
  <svg width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}">
{paths_str}
  </svg>
</body>
</html>"""

        return html

    def _generate_empty_html(self) -> str:
        """Generate an empty HTML document with an SVG canvas."""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SVG Animation</title>
</head>
<body>
  <svg width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}">
  </svg>
</body>
</html>"""

    def generate_js_animation(
        self,
        svg_paths: List[Dict[str, Any]],
        duration: float = 2.0,
        fill: bool = True,
        stroke_color: str = "#000000",
        stroke_width: int = 2,
        easing: str = "easeOutQuad",
    ) -> str:
        """
        Generate HTML with JavaScript-animated SVG paths.

        Uses requestAnimationFrame for smooth animations with configurable
        easing functions.

        Args:
            svg_paths: List of path dicts with 'd' (path data) and optional 'fill' color
            duration: Animation duration in seconds
            fill: Whether to fill paths after drawing
            stroke_color: Color of the stroke during animation
            stroke_width: Width of the stroke
            easing: Easing function name

        Returns:
            HTML string with embedded JavaScript animations
        """
        # Handle empty paths list
        if not svg_paths:
            return self._generate_empty_html()

        # Generate path elements
        path_elements = []
        path_configs = []

        for i, path_data in enumerate(svg_paths):
            path_id = f"path_{i}"
            d = path_data.get("d", "")
            path_fill = path_data.get("fill", "#ffffff") if fill else "none"

            path_elements.append(
                f'    <path id="{path_id}" d="{d}" '
                f'fill="none" stroke="{stroke_color}" '
                f'stroke-width="{stroke_width}" />'
            )

            path_configs.append({"id": path_id, "fill": path_fill if fill else "none"})

        paths_str = "\n".join(path_elements)
        config_json = json.dumps(path_configs)
        duration_ms = int(duration * 1000)

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SVG Animation</title>
  <style>
    body {{ margin: 20px; font-family: Arial, sans-serif; }}
    svg {{ border: 1px solid #ddd; }}
  </style>
</head>
<body>
  <svg id="svg-canvas" width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}">
{paths_str}
  </svg>
  
  <script>
    const pathConfigs = {config_json};
    const duration = {duration_ms};
    
    // Easing functions
    const easings = {{
      linear: t => t,
      easeInQuad: t => t * t,
      easeOutQuad: t => t * (2 - t),
      easeInOutQuad: t => t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t,
      easeOutBounce: t => {{
        if (t < 1/2.75) return 7.5625 * t * t;
        if (t < 2/2.75) {{ t -= 1.5/2.75; return 7.5625 * t * t + 0.75; }}
        if (t < 2.5/2.75) {{ t -= 2.25/2.75; return 7.5625 * t * t + 0.9375; }}
        t -= 2.625/2.75;
        return 7.5625 * t * t + 0.984375;
      }}
    }};
    
    const easing = easings['{easing}'] || easings.easeOutQuad;
    
    function animatePaths() {{
      const paths = pathConfigs.map(config => {{
        const path = document.getElementById(config.id);
        const length = path.getTotalLength();
        path.style.strokeDasharray = length;
        path.style.strokeDashoffset = length;
        return {{ path, length, fill: config.fill }};
      }});
      
      const startTime = performance.now();
      
      function animate(currentTime) {{
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const easedProgress = easing(progress);
        
        paths.forEach(({{ path, length, fill }}) => {{
          path.style.strokeDashoffset = length * (1 - easedProgress);
          
          if (progress >= 1 && fill !== 'none') {{
            path.style.fill = fill;
          }}
        }});
        
        if (progress < 1) {{
          requestAnimationFrame(animate);
        }}
      }}
      
      requestAnimationFrame(animate);
    }}
    
    // Start animation when page loads
    window.addEventListener('load', animatePaths);
  </script>
</body>
</html>"""

        return html

    def generate_svg_smil(
        self,
        svg_paths: List[Dict[str, Any]],
        duration: float = 2.0,
        fill: bool = True,
        stroke_color: str = "#000000",
        stroke_width: int = 2,
        dash_length: int = None,
    ) -> str:
        """
        Generate standalone SVG with SMIL animations.

        Note: SMIL animations are deprecated in some browsers (Chrome).
        Use CSS or JS animations for better compatibility.

        Args:
            svg_paths: List of path dicts with 'd' (path data) and optional 'fill' color
            duration: Animation duration in seconds
            fill: Whether to fill paths after drawing
            stroke_color: Color of the stroke during animation
            stroke_width: Width of the stroke
            dash_length: Length of dash array for animation (should be >= path length)

        Returns:
            SVG string with embedded SMIL animations
        """
        # Handle empty paths list
        if not svg_paths:
            return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" 
     width="{self.width}" height="{self.height}" 
     viewBox="0 0 {self.width} {self.height}">
</svg>"""

        dash_len = dash_length or DEFAULT_DASH_LENGTH
        path_elements = []

        for i, path_data in enumerate(svg_paths):
            d = path_data.get("d", "")
            path_fill = path_data.get("fill", "#ffffff") if fill else "none"
            delay = i * (duration / len(svg_paths))

            path_elements.append(
                f"""  <path d="{d}" 
        fill="{path_fill}" stroke="{stroke_color}" 
        stroke-width="{stroke_width}"
        stroke-dasharray="{dash_len}" stroke-dashoffset="{dash_len}">
    <animate attributeName="stroke-dashoffset" 
             from="{dash_len}" to="0" 
             dur="{duration}s" 
             begin="{delay}s" 
             fill="freeze"/>
  </path>"""
            )

        paths_str = "\n".join(path_elements)

        svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" 
     width="{self.width}" height="{self.height}" 
     viewBox="0 0 {self.width} {self.height}">
{paths_str}
</svg>"""

        return svg
