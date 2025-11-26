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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
