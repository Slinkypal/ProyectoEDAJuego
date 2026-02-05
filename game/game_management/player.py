from structures.binary_tree import BinaryTree
import pyxel

class Player:
    def __init__(self, name, x, y):
        self.name = name # Nombre
        self.x = x # Ubicaciones (x,y)
        self.y = y
        # Guardamos la info del sprite
        self.img = 1
        self.u = 0
        self.v = 48
        self.w = 16  # Ancho estándar
        self.h = 16  # Alto estándar
        self.score = 0
        self.tree = BinaryTree()
        
    def draw(self, camera_x, camera_y, is_turn):
        px = int(self.x - camera_x)
        py = int(self.y - camera_y)

        # Margen de seguridad para dibujar (usamos self.w para ser genéricos)
        if -self.w <= px <= 256 and -self.h <= py <= 192:
            
            # --- CORRECCIÓN DE CENTRADO ---
            # En lugar de restar 4 fijos, restamos la mitad del ancho/alto real
            draw_x = px - (self.w // 2)
            draw_y = py - (self.h // 2)

            # Dibujamos usando las dimensiones correctas
            pyxel.blt(draw_x, draw_y, self.img, self.u, self.v, self.w, self.h)

            if is_turn:
# Ajustamos el texto para que flote sobre la cabeza, sea cual sea la altura
                pyxel.text(draw_x, draw_y - 6, "TU", 7)
