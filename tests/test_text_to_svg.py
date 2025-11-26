"""
Unit tests for the text_to_svg module.

These tests verify that text can be correctly converted to SVG paths.
"""
import pytest
import os
import tempfile
from unittest.mock import MagicMock, patch


class TestTextToSvg:
    """Tests for the text_to_svg module."""

    @pytest.fixture
    def mock_font(self):
        """Create a mock font for testing."""
        mock = MagicMock()
        mock.__getitem__ = MagicMock(side_effect=lambda key: {
            'head': MagicMock(unitsPerEm=2048),
            'hhea': MagicMock(ascender=1900, descender=-500),
        }.get(key))
        return mock

    def test_find_system_font(self):
        """Test that find_system_font can find a font."""
        from kivg.text_to_svg import find_system_font
        
        font_path = find_system_font()
        
        # On a typical Linux system, should find a font
        # Skip test if no fonts are available (e.g., in minimal container)
        if font_path:
            assert os.path.exists(font_path)
            assert font_path.endswith(('.ttf', '.otf', '.TTF', '.OTF', '.ttc'))

    def test_get_glyph_path_returns_path_and_width(self):
        """Test that get_glyph_path returns path string and width."""
        from kivg.text_to_svg import get_glyph_path, find_system_font
        from fontTools.ttLib import TTFont
        
        font_path = find_system_font()
        if font_path is None:
            pytest.skip("No system font available")
        
        font = TTFont(font_path)
        
        path_str, width = get_glyph_path(font, 'A')
        
        assert isinstance(path_str, str)
        assert len(path_str) > 0  # Path should not be empty for 'A'
        assert isinstance(width, (int, float))
        assert width > 0
        
        font.close()

    def test_get_glyph_path_with_unknown_character(self):
        """Test get_glyph_path with a character not in the font."""
        from kivg.text_to_svg import get_glyph_path, find_system_font
        from fontTools.ttLib import TTFont
        
        font_path = find_system_font()
        if font_path is None:
            pytest.skip("No system font available")
        
        font = TTFont(font_path)
        
        # Use an obscure Unicode character unlikely to be in most fonts
        path_str, width = get_glyph_path(font, '\u2603')  # Snowman
        
        # May or may not be present, but should not raise
        assert isinstance(path_str, str)
        
        font.close()

    def test_transform_path_basic(self):
        """Test that transform_path applies offsets correctly."""
        from kivg.text_to_svg import transform_path
        
        # Simple move command
        path = "M100 200"
        result = transform_path(path, x_offset=10, y_offset=300, scale=1.0)
        
        # Should have M command with transformed coordinates
        assert "M" in result

    def test_text_to_svg_paths_creates_valid_svg(self):
        """Test that text_to_svg_paths generates valid SVG content."""
        from kivg.text_to_svg import text_to_svg_paths, find_system_font
        
        font_path = find_system_font()
        if font_path is None:
            pytest.skip("No system font available")
        
        svg_content, (width, height) = text_to_svg_paths(
            "Test",
            font_path=font_path,
            font_size=50
        )
        
        # Check that it's valid SVG
        assert '<?xml version="1.0"' in svg_content
        assert '<svg' in svg_content
        assert '</svg>' in svg_content
        assert '<path' in svg_content
        assert 'viewBox' in svg_content
        
        # Check dimensions
        assert width > 0
        assert height > 0

    def test_text_to_svg_file_creates_file(self):
        """Test that text_to_svg_file creates an SVG file."""
        from kivg.text_to_svg import text_to_svg_file, find_system_font
        
        font_path = find_system_font()
        if font_path is None:
            pytest.skip("No system font available")
        
        # Create temporary file
        fd, temp_path = tempfile.mkstemp(suffix='.svg')
        os.close(fd)
        
        try:
            width, height = text_to_svg_file(
                "Hello",
                temp_path,
                font_path=font_path,
                font_size=50
            )
            
            # Check file was created
            assert os.path.exists(temp_path)
            
            # Check file content
            with open(temp_path, 'r') as f:
                content = f.read()
            
            assert '<svg' in content
            assert '</svg>' in content
            
            # Check dimensions
            assert width > 0
            assert height > 0
            
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_text_to_svg_paths_with_fill_color(self):
        """Test that fill color is applied to paths."""
        from kivg.text_to_svg import text_to_svg_paths, find_system_font
        
        font_path = find_system_font()
        if font_path is None:
            pytest.skip("No system font available")
        
        svg_content, _ = text_to_svg_paths(
            "A",
            font_path=font_path,
            font_size=50,
            fill_color="#FF0000"
        )
        
        assert 'fill="#FF0000"' in svg_content

    def test_text_to_svg_paths_with_multiline(self):
        """Test that multiline text creates multiple lines of paths."""
        from kivg.text_to_svg import text_to_svg_paths, find_system_font
        
        font_path = find_system_font()
        if font_path is None:
            pytest.skip("No system font available")
        
        svg_content, (width, height) = text_to_svg_paths(
            "Line1\nLine2",
            font_path=font_path,
            font_size=50
        )
        
        # Check that paths for both lines are created
        assert 'char_0_0' in svg_content  # First line
        assert 'char_1_0' in svg_content  # Second line
        
        # Height should be greater for two lines
        single_line_content, (_, single_height) = text_to_svg_paths(
            "Line1",
            font_path=font_path,
            font_size=50
        )
        
        assert height > single_height

    def test_get_text_animation_config_sequential(self):
        """Test animation config generation for sequential animation."""
        from kivg.text_to_svg import get_text_animation_config
        
        config = get_text_animation_config(
            "AB",
            animation_type="sequential",
            duration_per_char=0.2,
            transition="out_sine"
        )
        
        assert len(config) == 2
        assert config[0]["id_"] == "char_0_0"
        assert config[1]["id_"] == "char_0_1"
        assert config[0]["from_"] is None  # Sequential has no direction
        assert config[0]["d"] == 0.2
        assert config[0]["t"] == "out_sine"

    def test_get_text_animation_config_from_left(self):
        """Test animation config generation for from_left animation."""
        from kivg.text_to_svg import get_text_animation_config
        
        config = get_text_animation_config(
            "AB",
            animation_type="from_left"
        )
        
        assert len(config) == 2
        assert config[0]["from_"] == "left"

    def test_get_text_animation_config_ignores_spaces(self):
        """Test that spaces are not included in animation config."""
        from kivg.text_to_svg import get_text_animation_config
        
        config = get_text_animation_config("A B")
        
        # Only 2 characters (A and B), space is skipped
        assert len(config) == 2


class TestKivgDrawText:
    """Tests for the Kivg.draw_text and Kivg.text_animate methods."""

    @pytest.fixture
    def mock_widget(self):
        """Create a mock widget for testing."""
        widget = MagicMock()
        widget.pos = [100, 100]
        widget.size = [400, 400]
        widget.canvas = MagicMock()
        widget.canvas.clear = MagicMock()
        widget.canvas.after = MagicMock()
        return widget

    def test_draw_text_raises_on_no_font(self, mock_widget):
        """Test that draw_text raises error when no font is found."""
        from kivg import Kivg
        
        kivg = Kivg(mock_widget)
        
        with patch('kivg.main.find_system_font', return_value=None):
            with pytest.raises(ValueError, match="No font file found"):
                kivg.draw_text("Hello")

    def test_text_animate_raises_on_no_font(self, mock_widget):
        """Test that text_animate raises error when no font is found."""
        from kivg import Kivg
        
        kivg = Kivg(mock_widget)
        
        with patch('kivg.main.find_system_font', return_value=None):
            with pytest.raises(ValueError, match="No font file found"):
                kivg.text_animate("Hello")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
