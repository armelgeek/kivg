"""
Kivg - SVG drawing and animation for Kivy
"""
from .version import __version__

# Check if Kivy is available
try:
    from kivy.logger import Logger
    KIVY_AVAILABLE = True
    _log_message = "Kivg:" + f" {__version__}" + f' (installed at "{__file__}")'
    Logger.info(_log_message)
except ImportError:
    KIVY_AVAILABLE = False

# Only import Kivg class if Kivy is available (it depends on Kivy)
if KIVY_AVAILABLE:
    from .main import Kivg
    __all__ = ["Kivg", "KIVY_AVAILABLE"]
else:
    # Provide a helpful error message for users trying to use Kivg without Kivy
    def Kivg(*args, **kwargs):
        raise ImportError(
            "Kivy is not installed. The Kivg class requires Kivy for desktop rendering. "
            "Install with: pip install kivg[kivy]"
        )
    __all__ = ["KIVY_AVAILABLE"]

# Always export svg_parser functionality (works without Kivy)
from .svg_parser import parse_svg

__all__ = ["Kivg", "KIVY_AVAILABLE", "parse_svg", "__version__"]
