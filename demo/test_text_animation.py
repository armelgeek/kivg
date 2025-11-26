"""
Demo for text animation functionality in Kivg.

This demo shows how to:
1. Draw text with handwriting animation effect
2. Animate text with shape animation (each character appears separately)
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock

from kivg import Kivg

kv = """
BoxLayout:
    orientation: "vertical"
    canvas:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size

    AnchorLayout:
        BoxLayout:
            id: text_area
            size_hint: None, None
            size: 800, 200

    GridLayout:
        size_hint_y: None
        height: dp(80)
        rows: 1
        padding: dp(10)
        spacing: dp(10)

        Button:
            text: "Draw Text\\n(Handwriting)"
            on_release: app.animate_handwriting()

        Button:
            text: "Text Animate\\n(Bounce)"
            on_release: app.animate_text_bounce()

        Button:
            text: "Text Animate\\n(Drop from Top)"
            on_release: app.animate_text_drop()

        Button:
            text: "Text Animate\\n(Rise from Bottom)"
            on_release: app.animate_text_rise()

        Button:
            text: "Clear"
            on_release: app.clear_canvas()
"""


class TextAnimDemo(App):
    def build(self):
        self.root = Builder.load_string(kv)
        self.kivg = Kivg(self.root.ids.text_area)
        return self.root

    def clear_canvas(self):
        """Clear the canvas."""
        self.root.ids.text_area.canvas.clear()

    def animate_handwriting(self):
        """Animate text like handwriting with pen/hand tracking."""
        self.clear_canvas()
        self.kivg.draw_text(
            "Hello",
            animate=True,
            font_size=120,
            fill_color="#2196F3",
            fill=True,
            line_width=2,
            line_color=[0, 0, 0, 1],
            dur=0.01,
            show_hand=True,
            hand_size=(100, 100),
        )

    def animate_text_bounce(self):
        """Animate each character with bounce effect."""
        self.clear_canvas()
        self.kivg.text_animate(
            "Kivy",
            font_size=150,
            fill_color="#4CAF50",
            animation_type="from_center_y",
            duration_per_char=0.3,
            transition="out_bounce",
        )

    def animate_text_drop(self):
        """Animate characters dropping from top."""
        self.clear_canvas()
        self.kivg.text_animate(
            "Drop",
            font_size=150,
            fill_color="#FF5722",
            animation_type="from_top",
            duration_per_char=0.25,
            transition="out_back",
        )

    def animate_text_rise(self):
        """Animate characters rising from bottom."""
        self.clear_canvas()
        self.kivg.text_animate(
            "Rise",
            font_size=150,
            fill_color="#9C27B0",
            animation_type="from_bottom",
            duration_per_char=0.25,
            transition="out_elastic",
        )


if __name__ == "__main__":
    TextAnimDemo().run()
