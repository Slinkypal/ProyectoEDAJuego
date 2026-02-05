import pyxel
try:
    from binary_tree import BinaryTree
except ImportError:
    from structures.binary_tree import BinaryTree

class Player:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.img = 1  # Banco de imágenes 1
        self.u = 0
        self.v = 48
        self.w = 16
        self.h = 16
        self.score = 0
        self.tree = BinaryTree()
        
    def draw(self, camera_x, camera_y, is_turn):
        # Posición relativa a la cámara
        px = int(self.x - camera_x)
        py = int(self.y - camera_y)

        # Culling simple (solo dibujar si está en pantalla)
        if -self.w <= px <= 256 and -self.h <= py <= 192:
            draw_x = px - (self.w // 2)
            draw_y = py - (self.h // 2)

            pyxel.blt(draw_x, draw_y, self.img, self.u, self.v, self.w, self.h) 

            if is_turn:
                # Indicador de turno flotando
                text_w = pyxel.FONT_WIDTH * 2
                pyxel.text(draw_x + (self.w//2) - (text_w//2), draw_y - 8, "TU", 7)
