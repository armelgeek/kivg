"""
Unit tests for the PenTracker class.

These tests use mock objects to test the slide_out logic without requiring
a Kivy display/graphics context. The MockPenTracker class replicates the
essential slide_out logic to enable testing in headless environments.

Note: The mock implementation mirrors the real PenTracker's slide_out logic.
If the real implementation changes, these tests should be updated accordingly.
"""
import pytest
from unittest.mock import MagicMock


class TestPenTrackerSlideOut:
    """Tests for the PenTracker slide_out functionality."""

    @pytest.fixture
    def mock_widget(self):
        """Create a mock widget for testing."""
        widget = MagicMock()
        widget.pos = [100, 100]
        widget.size = [400, 400]
        # Mock canvas.after
        widget.canvas = MagicMock()
        widget.canvas.after = MagicMock()
        return widget

    @pytest.fixture
    def mock_pen_tracker(self, mock_widget):
        """
        Create a mock PenTracker for unit testing without graphics.
        
        This mock replicates the slide_out logic from the real PenTracker
        to enable testing without a Kivy display. The logic is intentionally
        duplicated to test the algorithm independently of Kivy's graphics
        context requirements.
        """
        class MockPenTracker:
            def __init__(self, widget, hand_size=(100, 100), pen_offset=(10, 85)):
                self.widget = widget
                self.hand_size = hand_size
                self.pen_offset = pen_offset
                self._hand_texture = MagicMock()  # Mock texture
                self._hand_group = None
                self._hand_rect = None
                self._hand_color = None
                self._is_active = False
                self._current_pos = (0, 0)
                self._slide_out_event = None
                self._slide_out_callback = None
            
            def start(self):
                if self._hand_texture is None:
                    return
                self._is_active = True
                self._hand_group = MagicMock()
                self._hand_rect = MagicMock()
                self._hand_color = MagicMock()
            
            def stop(self):
                if self._slide_out_event:
                    self._slide_out_event.cancel()
                    self._slide_out_event = None
                self._slide_out_callback = None
                self._is_active = False
                self._hand_group = None
                self._hand_rect = None
                self._hand_color = None
            
            def update_position(self, x, y):
                if not self._is_active or self._hand_texture is None:
                    return
                hand_x = x - self.pen_offset[0]
                hand_y = y - (self.hand_size[1] - self.pen_offset[1])
                self._current_pos = (hand_x, hand_y)
                if self._hand_rect:
                    self._hand_rect.pos = self._current_pos
            
            def clear_hand(self):
                self._hand_group = None
                self._hand_rect = None
                self._hand_color = None
            
            def slide_out(self, on_complete=None, duration=0.5, step=0.016):
                if not self._is_active or self._hand_texture is None:
                    if on_complete:
                        on_complete()
                    return
                
                self._slide_out_callback = on_complete
                
                # Calculate target position - slide downward off the widget
                widget_bottom = self.widget.pos[1] - self.hand_size[1]
                
                start_x, start_y = self._current_pos
                target_x = start_x  # Keep same x position - slide straight down
                target_y = widget_bottom
                
                self._slide_start_pos = (start_x, start_y)
                self._slide_target_pos = (target_x, target_y)
                self._slide_progress = 0.0
                self._slide_duration = duration
                self._slide_step = step
                self._slide_start_opacity = 1.0  # Start fully visible
                # Fallback RGB value for fade effect (mock doesn't track actual color)
                self._slide_original_rgb = (1, 1, 1)
                
                # Store mock event for testing
                self._slide_out_event = MagicMock()
            
            def _update_slide_out(self, dt):
                self._slide_progress += dt / self._slide_duration
                
                if self._slide_progress >= 1.0:
                    self._slide_progress = 1.0
                    self._finish_slide_out()
                    return False
                
                t = self._slide_progress
                ease = -1.0 * t * (t - 2.0)
                
                start_x, start_y = self._slide_start_pos
                target_x, target_y = self._slide_target_pos
                
                current_x = start_x + (target_x - start_x) * ease
                current_y = start_y + (target_y - start_y) * ease
                
                self._current_pos = (current_x, current_y)
                
                if self._hand_rect:
                    self._hand_rect.pos = self._current_pos
                
                # Update opacity with fade effect
                if self._hand_color:
                    current_opacity = self._slide_start_opacity * (1.0 - ease)
                    r, g, b = self._slide_original_rgb
                    self._hand_color.rgba = (r, g, b, current_opacity)
                
                return True
            
            def _finish_slide_out(self):
                if self._slide_out_event:
                    self._slide_out_event.cancel()
                    self._slide_out_event = None
                
                self._is_active = False
                self.clear_hand()
                
                if self._slide_out_callback:
                    callback = self._slide_out_callback
                    self._slide_out_callback = None
                    callback()
            
            @property
            def is_active(self):
                return self._is_active
            
            @property
            def current_position(self):
                return self._current_pos
        
        return MockPenTracker(mock_widget)

    def test_slide_out_calculates_correct_target(self, mock_pen_tracker, mock_widget):
        """Test that slide_out calculates the correct target position."""
        # Start tracking and set initial position
        mock_pen_tracker.start()
        mock_pen_tracker.update_position(200, 200)
        
        mock_pen_tracker.slide_out()
        
        # Check that the target position is calculated correctly
        # Now slides straight down: x stays the same, y goes to widget bottom
        # start_x = 200 - pen_offset[0] = 200 - 10 = 190
        expected_target_x = mock_pen_tracker._slide_start_pos[0]  # Same as start x
        # widget_bottom = widget.pos[1] - hand_size[1]
        # = 100 - 100 = 0
        expected_target_y = 0
        
        assert mock_pen_tracker._slide_target_pos == (expected_target_x, expected_target_y)

    def test_slide_out_calls_callback_on_complete(self, mock_pen_tracker):
        """Test that slide_out calls the callback when animation completes."""
        callback = MagicMock()
        
        mock_pen_tracker.start()
        mock_pen_tracker.update_position(200, 200)
        
        mock_pen_tracker.slide_out(on_complete=callback)
        
        # Simulate animation completion
        mock_pen_tracker._slide_progress = 1.0
        mock_pen_tracker._finish_slide_out()
        
        callback.assert_called_once()

    def test_slide_out_clears_hand_on_complete(self, mock_pen_tracker):
        """Test that slide_out clears the hand when animation completes."""
        mock_pen_tracker.start()
        mock_pen_tracker.update_position(200, 200)
        
        mock_pen_tracker.slide_out()
        
        # Simulate animation completion
        mock_pen_tracker._finish_slide_out()
        
        # Hand should no longer be active
        assert mock_pen_tracker._is_active is False
        assert mock_pen_tracker._hand_group is None

    def test_slide_out_with_no_texture_calls_callback_immediately(self, mock_widget):
        """Test that slide_out calls callback immediately if no texture."""
        class MockPenTrackerNoTexture:
            def __init__(self):
                self._hand_texture = None
                self._is_active = False
            
            def slide_out(self, on_complete=None, duration=0.3, step=0.016):
                if not self._is_active or self._hand_texture is None:
                    if on_complete:
                        on_complete()
                    return
        
        tracker = MockPenTrackerNoTexture()
        callback = MagicMock()
        tracker.slide_out(on_complete=callback)
        
        callback.assert_called_once()

    def test_slide_out_with_inactive_tracker_calls_callback_immediately(
        self, mock_pen_tracker
    ):
        """Test that slide_out calls callback if tracker is not active."""
        # Don't start the tracker
        callback = MagicMock()
        mock_pen_tracker.slide_out(on_complete=callback)
        
        callback.assert_called_once()

    def test_update_slide_out_progress(self, mock_pen_tracker):
        """Test that _update_slide_out correctly updates position."""
        mock_pen_tracker.start()
        mock_pen_tracker.update_position(200, 200)
        
        mock_pen_tracker.slide_out()
        
        # Store initial values
        start_pos = mock_pen_tracker._slide_start_pos
        target_pos = mock_pen_tracker._slide_target_pos
        
        # Simulate a progress update (dt = 0.1 seconds)
        mock_pen_tracker._update_slide_out(0.1)
        
        # Check that progress was updated
        assert mock_pen_tracker._slide_progress > 0
        
        # Check that position was updated (should be between start and target)
        current_x, current_y = mock_pen_tracker._current_pos
        start_x, start_y = start_pos
        target_x, target_y = target_pos
        
        # Position should be moving toward target
        if target_x > start_x:
            assert current_x > start_x
        if target_y < start_y:
            assert current_y < start_y

    def test_slide_out_fades_opacity(self, mock_pen_tracker):
        """Test that slide_out gradually reduces opacity during animation."""
        mock_pen_tracker.start()
        mock_pen_tracker.update_position(200, 200)
        
        mock_pen_tracker.slide_out()
        
        # Simulate a progress update (dt = 0.1 seconds)
        mock_pen_tracker._update_slide_out(0.1)
        
        # Check that opacity was reduced
        assert mock_pen_tracker._hand_color.rgba[3] < 1.0
        
        # Simulate more progress
        mock_pen_tracker._update_slide_out(0.1)
        
        # Opacity should be further reduced
        assert mock_pen_tracker._hand_color.rgba[3] < 0.8

    def test_stop_cancels_slide_out_animation(self, mock_pen_tracker):
        """Test that stop() cancels any ongoing slide-out animation."""
        mock_pen_tracker.start()
        mock_pen_tracker.update_position(200, 200)
        
        mock_pen_tracker.slide_out()
        
        # Now call stop
        mock_pen_tracker.stop()
        
        # Event should have been cancelled
        assert mock_pen_tracker._slide_out_event is None
        assert mock_pen_tracker._slide_out_callback is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

