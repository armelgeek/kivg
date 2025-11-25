"""
PenTracker handles pen/stylus tracking with hand image during SVG path animation.
This creates a writing effect where a hand image follows the drawing path.
"""

from kivy.graphics import Rectangle, Color
from kivy.core.image import Image as CoreImage
from typing import Any, Optional, Tuple
import os


class PenTracker:
    """
    Tracks pen position during path drawing animation and displays a hand image.
    
    The hand image follows the current drawing position to create a realistic
    writing/drawing effect.
    """
    
    # Default hand image path (bundled with the package)
    DEFAULT_HAND_IMAGE = os.path.join(os.path.dirname(__file__), "..", "assets", "drawing-hand.png")
    
    def __init__(self, widget: Any, hand_image: Optional[str] = None, 
                 hand_size: Tuple[float, float] = (100, 100),
                 pen_offset: Tuple[float, float] = (10, 85)):
        """
        Initialize the PenTracker.
        
        Args:
            widget: The Kivy widget to draw the hand on
            hand_image: Path to the hand image file. If None, uses default.
            hand_size: Size of the hand image (width, height)
            pen_offset: Offset from pen tip to hand image position (x, y).
                       This is where the pen tip is located relative to the 
                       top-left corner of the hand image.
        """
        self.widget = widget
        self.hand_image_path = hand_image or self.DEFAULT_HAND_IMAGE
        self.hand_size = hand_size
        self.pen_offset = pen_offset
        self._hand_texture = None
        self._hand_rect = None
        self._is_active = False
        self._current_pos = (0, 0)
        
        # Load the hand image texture
        self._load_hand_texture()
    
    def _load_hand_texture(self) -> None:
        """Load the hand image texture."""
        if os.path.exists(self.hand_image_path):
            try:
                self._hand_texture = CoreImage(self.hand_image_path).texture
            except Exception:
                self._hand_texture = None
    
    def start(self) -> None:
        """Start tracking - makes the hand visible."""
        self._is_active = True
    
    def stop(self) -> None:
        """Stop tracking and hide the hand."""
        self._is_active = False
        self._hand_rect = None
    
    def update_position(self, x: float, y: float) -> None:
        """
        Update the hand position to follow the pen tip.
        
        Args:
            x: X coordinate of the current pen tip position
            y: Y coordinate of the current pen tip position
        """
        if not self._is_active or self._hand_texture is None:
            return
        
        # Calculate hand position based on pen tip and offset
        # The pen tip should appear at the pen_offset position within the hand image
        hand_x = x - self.pen_offset[0]
        hand_y = y - self.pen_offset[1]
        
        self._current_pos = (hand_x, hand_y)
    
    def draw_hand(self) -> None:
        """Draw the hand image at the current position."""
        if not self._is_active or self._hand_texture is None:
            return
        
        with self.widget.canvas.after:
            Color(1, 1, 1, 1)
            Rectangle(
                texture=self._hand_texture,
                pos=self._current_pos,
                size=self.hand_size
            )
    
    def clear_hand(self) -> None:
        """Clear the hand from the canvas."""
        self.widget.canvas.after.clear()
    
    @property
    def is_active(self) -> bool:
        """Check if pen tracking is active."""
        return self._is_active
    
    @property
    def current_position(self) -> Tuple[float, float]:
        """Get the current hand position."""
        return self._current_pos
