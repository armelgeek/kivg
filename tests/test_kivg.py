"""
Unit tests for Kivg library.
"""

import pytest
import tempfile
import os


class TestSVGParser:
    """Tests for SVG parsing functionality."""

    @pytest.fixture
    def sample_svg_content(self):
        """Create sample SVG content."""
        return """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path id="circle" d="M50 10 A40 40 0 1 1 49.99 10 Z" fill="#ff0000"/>
  <path id="line" d="M10 50 L90 50" fill="#00ff00"/>
</svg>"""

    @pytest.fixture
    def sample_svg_file(self, sample_svg_content):
        """Create a temporary SVG file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".svg", delete=False) as f:
            f.write(sample_svg_content)
            return f.name

    def test_parse_svg(self, sample_svg_file):
        """Test parsing an SVG file."""
        from kivg import parse_svg

        svg_size, paths = parse_svg(sample_svg_file)

        assert svg_size == [100.0, 100.0]
        assert len(paths) == 2

        # Clean up
        os.unlink(sample_svg_file)

    def test_parse_svg_colors(self, sample_svg_file):
        """Test that colors are parsed correctly."""
        from kivg import parse_svg

        svg_size, paths = parse_svg(sample_svg_file)

        # First path should be red (#ff0000)
        circle_color = paths[0][2]
        assert circle_color[0] == 1.0  # Red
        assert circle_color[1] == 0.0  # Green
        assert circle_color[2] == 0.0  # Blue

        # Second path should be green (#00ff00)
        line_color = paths[1][2]
        assert line_color[0] == 0.0  # Red
        assert line_color[1] == 1.0  # Green
        assert line_color[2] == 0.0  # Blue

        # Clean up
        os.unlink(sample_svg_file)


class TestColorConversion:
    """Tests for hex color conversion."""

    def test_hex_color_6_digits(self):
        """Test converting 6-digit hex colors."""
        from kivg.svg_parser import get_color_from_hex

        color = get_color_from_hex("#ff0000")
        assert color == [1.0, 0.0, 0.0, 1.0]

        color = get_color_from_hex("#00ff00")
        assert color == [0.0, 1.0, 0.0, 1.0]

        color = get_color_from_hex("#0000ff")
        assert color == [0.0, 0.0, 1.0, 1.0]

    def test_hex_color_3_digits(self):
        """Test converting 3-digit shorthand hex colors."""
        from kivg.svg_parser import get_color_from_hex

        color = get_color_from_hex("#f00")
        assert color == [1.0, 0.0, 0.0, 1.0]

        color = get_color_from_hex("#0f0")
        assert color == [0.0, 1.0, 0.0, 1.0]

    def test_hex_color_8_digits(self):
        """Test converting 8-digit hex colors with alpha."""
        from kivg.svg_parser import get_color_from_hex

        color = get_color_from_hex("#ff000080")
        assert color[0] == 1.0
        assert color[1] == 0.0
        assert color[2] == 0.0
        assert abs(color[3] - 0.502) < 0.01  # ~50% alpha

    def test_hex_color_without_hash(self):
        """Test converting hex colors without # prefix."""
        from kivg.svg_parser import get_color_from_hex

        color = get_color_from_hex("ff0000")
        assert color == [1.0, 0.0, 0.0, 1.0]


class TestSVGAnimator:
    """Tests for SVGAnimator class."""

    @pytest.fixture
    def sample_svg_file(self):
        """Create a temporary SVG file."""
        content = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <path id="test" d="M10 10 L90 90" fill="#ff0000"/>
</svg>"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".svg", delete=False) as f:
            f.write(content)
            return f.name

    def test_create_animator(self):
        """Test creating an SVGAnimator instance."""
        from kivg import SVGAnimator

        animator = SVGAnimator(width=800, height=600)
        assert animator.width == 800
        assert animator.height == 600

    def test_load_svg(self, sample_svg_file):
        """Test loading an SVG file."""
        from kivg import SVGAnimator

        animator = SVGAnimator()
        info = animator.load_svg(sample_svg_file)

        assert "svg_size" in info
        assert "shapes" in info
        assert "path_count" in info

        # Clean up
        os.unlink(sample_svg_file)

    def test_get_paths(self, sample_svg_file):
        """Test getting paths from loaded SVG."""
        from kivg import SVGAnimator

        animator = SVGAnimator()
        animator.load_svg(sample_svg_file)

        paths = animator.get_paths()
        assert len(paths) == 1
        assert paths[0]["id"] == "test"
        assert "d" in paths[0]
        assert "fill" in paths[0]

        # Clean up
        os.unlink(sample_svg_file)


class TestWebExporter:
    """Tests for WebAnimationExporter class."""

    def test_generate_css_animation(self):
        """Test generating CSS animation HTML."""
        from kivg import WebAnimationExporter

        exporter = WebAnimationExporter(width=400, height=400)
        paths = [{"d": "M10 10 L90 90", "fill": "#ff0000"}]

        html = exporter.generate_css_animation(paths, duration=2.0)

        assert "<!DOCTYPE html>" in html
        assert "@keyframes draw" in html
        assert "stroke-dasharray" in html

    def test_generate_js_animation(self):
        """Test generating JavaScript animation HTML."""
        from kivg import WebAnimationExporter

        exporter = WebAnimationExporter(width=400, height=400)
        paths = [{"d": "M10 10 L90 90", "fill": "#ff0000"}]

        html = exporter.generate_js_animation(paths, duration=2.0)

        assert "<!DOCTYPE html>" in html
        assert "requestAnimationFrame" in html
        assert "animatePaths" in html

    def test_generate_svg_smil(self):
        """Test generating SMIL animation SVG."""
        from kivg import WebAnimationExporter

        exporter = WebAnimationExporter(width=400, height=400)
        paths = [{"d": "M10 10 L90 90", "fill": "#ff0000"}]

        svg = exporter.generate_svg_smil(paths, duration=2.0)

        assert '<?xml version="1.0"' in svg
        assert "<animate" in svg
        assert "stroke-dashoffset" in svg


class TestAnimationEasing:
    """Tests for animation easing functions."""

    def test_linear(self):
        """Test linear easing."""
        from kivg.animation import AnimationTransition

        assert AnimationTransition.linear(0.0) == 0.0
        assert AnimationTransition.linear(0.5) == 0.5
        assert AnimationTransition.linear(1.0) == 1.0

    def test_out_quad(self):
        """Test quadratic ease-out."""
        from kivg.animation import AnimationTransition

        assert AnimationTransition.out_quad(0.0) == 0.0
        assert AnimationTransition.out_quad(1.0) == 1.0
        # out_quad should be faster at the start
        assert AnimationTransition.out_quad(0.5) > 0.5

    def test_in_bounce(self):
        """Test bounce ease-in."""
        from kivg.animation import AnimationTransition

        assert AnimationTransition.in_bounce(0.0) == 0.0
        assert AnimationTransition.in_bounce(1.0) == 1.0

    def test_get_transition(self):
        """Test getting transition by name."""
        from kivg.animation import AnimationTransition

        func = AnimationTransition.get_transition("out_bounce")
        assert func == AnimationTransition.out_bounce

        # Non-existent should return linear
        func = AnimationTransition.get_transition("non_existent")
        assert func == AnimationTransition.linear


class TestTextToSVG:
    """Tests for text-to-SVG conversion functionality."""

    def test_create_text_to_svg(self):
        """Test creating a TextToSVG instance."""
        from kivg import TextToSVG

        converter = TextToSVG(
            font_family="sans-serif", font_size=40.0, font_weight="bold"
        )
        assert converter.font_family == "sans-serif"
        assert converter.font_size == 40.0
        assert converter.font_weight == "bold"

    def test_get_text_dimensions(self):
        """Test getting text dimensions."""
        from kivg import TextToSVG

        converter = TextToSVG(font_size=40.0)
        width, height = converter.get_text_dimensions("Hello")

        assert width > 0
        assert height > 0
        assert width > height  # Text should be wider than tall

    def test_text_to_path_data(self):
        """Test converting text to path data."""
        from kivg import TextToSVG

        converter = TextToSVG(font_size=40.0)
        svg_size, paths = converter.text_to_path_data("Test")

        assert len(svg_size) == 2
        assert svg_size[0] > 0  # width
        assert svg_size[1] > 0  # height
        assert len(paths) >= 1  # At least one path should be created

    def test_text_to_svg_paths(self):
        """Test generating SVG content from text."""
        from kivg import TextToSVG

        converter = TextToSVG(font_size=40.0)
        svg_content = converter.text_to_svg_paths("Hello")

        assert "<?xml" in svg_content
        assert "<svg" in svg_content
        assert "<path" in svg_content
        assert 'd="' in svg_content

    def test_create_animated_text_svg(self):
        """Test creating animated text SVG."""
        from kivg import TextToSVG

        converter = TextToSVG(font_size=40.0)
        svg = converter.create_animated_text_svg(
            "Hello",
            duration=2.0,
            stroke_color="#ff0000",
            stroke_width=2.0,
        )

        assert "<?xml" in svg
        assert "<svg" in svg
        assert "@keyframes draw-text" in svg
        assert "stroke-dasharray" in svg
        assert "stroke-dashoffset" in svg
        assert "animation" in svg

    def test_create_text_animation_function(self):
        """Test the create_text_animation convenience function."""
        from kivg import create_text_animation

        svg = create_text_animation(
            "Hello World", duration=3.0, font_size=50.0, stroke_color="#000000"
        )

        assert "<?xml" in svg
        assert "<svg" in svg
        assert "@keyframes" in svg
        assert "3.0s" in svg  # Duration should be in the animation

    def test_text_to_svg_function(self):
        """Test the text_to_svg convenience function."""
        from kivg import text_to_svg

        svg = text_to_svg("Test", font_size=30.0, font_weight="bold")

        assert "<svg" in svg
        assert "<path" in svg


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
