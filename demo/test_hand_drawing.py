from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.clock import Clock
from kivg import Kivg

kv = """
BoxLayout:
    orientation: "vertical"
    canvas:
        Color:
            rgba: 0.95, 0.95, 0.95, 1
        Rectangle:
            pos: self.pos
            size: self.size
    
    Label:
        size_hint_y: 0.15
        text: "Démo de la main qui dessine - Regardez la main suivre le tracé!"
        color: 0.2, 0.2, 0.2, 1
        font_size: 20
        bold: True
    
    Widget:
        id: svg_container
        size_hint: 1, 0.85
        canvas:
            Color:
                rgba: 1, 1, 1, 1
            Rectangle:
                pos: self.pos
                size: self.size
"""

class HandDrawingDemo(App):
    def build(self):
        self.root = Builder.load_string(kv)
        return self.root
    
    def on_start(self):
        # Attendre un peu pour que la fenêtre soit complètement initialisée
        Clock.schedule_once(self.start_drawing, 0.5)
    
    def start_drawing(self, dt):
        # Créer le widget Kivg sur le conteneur
        container = self.root.ids.svg_container
        print(f"Container size: {container.size}")
        print(f"Container pos: {container.pos}")
        
        self.kivg = Kivg(container)
        
        # Dessiner avec la main qui suit le tracé
        print("Démarrage du dessin avec la main...")
        self.kivg.draw(
            "icons/github.svg",      # GitHub a un bon tracé pour la démo
            animate=True,
            fill=False,
            show_hand=True,          # Activer la main
            hand_size=(150, 150),    # Taille de la main plus grande
            dur=0.015,               # Plus rapide pour voir l'effet
            line_width=4,            # Trait plus épais
            line_color=[0.2, 0.4, 0.8, 1],  # Couleur bleue
            pen_offset=(15, 100)     # Ajuster la position du stylo
        )
        print("Commande draw() exécutée!")

if __name__ == "__main__":
    HandDrawingDemo().run()
