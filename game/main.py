import pyxel
import json
import math
import sys

# Importaciones Propias
# Asegúrate de que tienes un archivo vacío __init__.py en cada subcarpeta
try:
    import graphics.city_map as cm
    from graphics.camera import Camera
    from graphics.city_map import draw_city, NODES
    
    from game_management.player import Player
    from game_management.save_manager import save_results
    from game_management.states import MENU, PLAYING, NODE_MENU, QUESTION, END
    from structures.graph.graph import Graph

except ImportError as e:
    print(f"Error de importación: {e}")
    print("Verifica que las carpetas tengan __init__.py y la estructura sea correcta.")
    sys.exit(1)

# Cargar preguntas de forma segura
try:
    questions = json.load(open("assets/questions.json", encoding="utf8"))
except FileNotFoundError:
    print("Advertencia: assets/questions.json no encontrado. Usando preguntas dummy.")
    questions = {k: "¿Pregunta de prueba?" for k in NODES.keys()}

class Game:
    def __init__(self):
        # Título y fps
        pyxel.init(256, 192, title="Camino a la EPN", fps=60)
        
        self.state = MENU
        cm.load_resources()
       
        # Configuración de Cámara
        self.camera = Camera(
            view_w=256, view_h=192,
            world_w=cm.WORLD_W, world_h=cm.WORLD_H
        )
        
        # Posición inicial (ajustada a un nodo para que no empiece en la nada
        pos1 = NODES["EL_EJIDO"]
        pos2 = NODES["EMBAJADA FRANCESA"]
        
        self.players = [
            # Jugador 1: Sprite de 16x16 en (0,0) del Banco 0
            Player("Jugador 1", pos1[0], pos1[1]),
            
            # Jugador 2: 
            Player("Jugador 2", pos2[0], pos2[1])
        ]

        # Centrar cámara en el jugador 1 al inicio
        self.camera.x = self.players[0].x - 128
        self.camera.y = self.players[0].y - 96

        self.turn = 0
        self.speed = 3  # Aumenté un poco la velocidad para pruebas

        self.current_node = None
        self.previous_node = None
        self.graph = Graph()

        pyxel.run(self.update, self.draw)

    def update(self):
        if self.state == MENU:
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.state = PLAYING
            if pyxel.btnp(pyxel.KEY_ESCAPE):
                pyxel.quit()

        elif self.state == PLAYING:
            self.move_player()
            self.detect_node()

        elif self.state == NODE_MENU:
            if pyxel.btnp(pyxel.KEY_E):
                self.state = QUESTION
            if pyxel.btnp(pyxel.KEY_Q):
                # Pequeño empujón para salir del radio de detección y no volver a entrar instantáneamente
                p = self.players[self.turn]
                p.y += 5 
                self.state = PLAYING

        elif self.state == QUESTION:
            if pyxel.btnp(pyxel.KEY_Y):
                self.answer(True)
            if pyxel.btnp(pyxel.KEY_N):
                self.answer(False)

        elif self.state == END:
            if pyxel.btnp(pyxel.KEY_ESCAPE):
                pyxel.quit()

    def move_player(self):
        p = self.players[self.turn]
        nx, ny = p.x, p.y

        # Movimiento
        if pyxel.btn(pyxel.KEY_W): ny -= self.speed
        if pyxel.btn(pyxel.KEY_S): ny += self.speed
        if pyxel.btn(pyxel.KEY_A): nx -= self.speed
        if pyxel.btn(pyxel.KEY_D): nx += self.speed

        # Límites del mundo (Colisión simple con bordes)
        nx = max(0, min(nx, cm.WORLD_W))
        ny = max(0, min(ny, cm.WORLD_H))

        p.x, p.y = nx, ny
        self.camera.follow(p.x, p.y)

    def detect_node(self):
        p = self.players[self.turn]
        # Distancia de detección un poco más generosa (16px)
        detection_radius = 16 
        
        for node, (x, y) in NODES.items():
            # Evitar re-detectar el nodo del que acabamos de salir inmediatamente
            if node == self.previous_node and self.state == PLAYING:
                if math.dist((p.x, p.y), (x, y)) > detection_radius + 5:
                     # Si nos alejamos lo suficiente, permitimos volver a interactuar (opcional)
                     pass 
                else:
                    continue

            if math.dist((p.x, p.y), (x, y)) < detection_radius:
                self.current_node = node
                self.state = NODE_MENU

    def answer(self, correct):
        p = self.players[self.turn]
        
        # Validación de seguridad por si el nodo no tiene pregunta
        q_text = questions.get(self.current_node, "Pregunta genérica")
        p.tree.add(q_text, correct)

        p.score += 10 if correct else -5

        self.graph.add_node(self.current_node)
        
        # Lógica del grafo
        if self.previous_node and self.previous_node != self.current_node:
            cost = 1 if correct else 5
            self.graph.add_edge(self.previous_node, self.current_node, cost)

        self.previous_node = self.current_node

        if self.current_node == "EPN":
            mst, total_cost = self.graph.kruskal()
            save_results(self.players, mst, total_cost)
            self.state = END
            return

        self.turn = (self.turn + 1) % 2
        # Mover al jugador un poco para que no reactive el nodo al instante
        self.players[self.turn].y += 10 
        self.state = PLAYING
        # Si llegamos a la EPN...
        if self.current_node == "EPN":
            # ... (código de guardar y fin)
            return

        # --- CAMBIO DE TURNO ---
        self.turn = (self.turn + 1) % 2
        
        # Teletransporte de cámara ---
        next_player = self.players[self.turn]
        
     # 1. Centrar la cámara en el nuevo jugador instantáneamente
     # Restamos la mitad de la pantalla (128, 96) para que quede al centro
        self.camera.x = next_player.x - 128
        self.camera.y = next_player.y - 96
        
# 2. Corregir límites (Clamp) para que no muestre el vacío negro si está cerca del borde
# Usamos las mismas variables que tiene tu objeto camera
        max_x = self.camera.world_w - self.camera.view_w
        max_y = self.camera.world_h - self.camera.view_h
        
        self.camera.x = max(0, min(self.camera.x, max_x))
        self.camera.y = max(0, min(self.camera.y, max_y))

        self.players[self.turn].y += 10 
        self.state = PLAYING

    def draw(self):
        pyxel.cls(12) # Azul claro (cielo)

        if self.state == MENU:
            pyxel.cls(5) # Fondo azul oscuro para menú
            pyxel.text(90, 80, "CAMINO A LA EPN", 7)
            pyxel.text(95, 110, "ENTER - JUGAR", 7)
            pyxel.text(100, 130, "ESC - SALIR", 7)
            
        elif self.state in [PLAYING, NODE_MENU, QUESTION]:
            draw_city(self.camera)

            # --- Dibujar Jugadores ---
            # Usaremos la funcion escrita en player.py
            for i, p in enumerate(self.players):
                es_su_turno = (i == self.turn)# Verificamos el turno
    # Le pasamos la posición de la cámara para que él calcule dónde aparecer
                p.draw(self.camera.x, self.camera.y, es_su_turno)
            

            # --- HUD ---
            pyxel.rect(0, 0, 256, 12, 0)
            p_act = self.players[self.turn]
            pyxel.text(5, 3, f"Turno: {p_act.name} | Score: {p_act.score}", 7)
   
            # --- UI Menús ---
            if self.state == NODE_MENU:
                # Caja semi-transparente (simulada con dither o color sólido)
                pyxel.rect(30, 150, 196, 35, 1)
                pyxel.rectb(30, 150, 196, 35, 7)
                pyxel.text(40, 158, f"Estas en: {self.current_node}", 7)
                pyxel.text(40, 168, "E - Responder Pregunta | Q - Cancelar", 6)

            if self.state == QUESTION:
                pyxel.rect(20, 40, 216, 100, 1)
                pyxel.rectb(20, 40, 216, 100, 7)
                
                q_text = questions.get(self.current_node, "Pregunta no encontrada")
                # Wrap de texto muy simple (corta visualmente si es muy largo)
                pyxel.text(30, 50, q_text[:30], 7) 
                pyxel.text(30, 60, q_text[30:60], 7)
                pyxel.text(30, 70, q_text[60:], 7)
                
                pyxel.text(80, 110, "Y = VERDADERO  |  N = FALSO", 10)

        elif self.state == END:
            pyxel.cls(0)
            pyxel.text(90, 80, "LLEGASTE A LA EPN", 10)
            pyxel.text(80, 100, "RESULTADOS GUARDADOS EN CSV", 7)
            pyxel.text(100, 140, "ESC - SALIR", 7)
        #--- MODO DEBUG (Agrega esto al final) ---
        # Si presionas TAB, te muestra las coordenadas
        if pyxel.btn(pyxel.KEY_TAB):
            mx, my = pyxel.mouse_x, pyxel.mouse_y
            
            # Calculamos la posición real en el mundo (Cámara + Mouse)
            world_x = self.camera.x + mx
            world_y = self.camera.y + my
            
            # Calculamos cuál es ese pixel en el EDITOR DE PYXEL (dividiendo por el zoom)
            editor_x = int(world_x / 2) # 2 es tu DRAW_SCALE
            editor_y = int(world_y / 2)
            
            # Dibujamos el texto flotando al lado del mouse
            info = f"Editor: {editor_x},{editor_y} | World: {int(world_x)},{int(world_y)}"
            pyxel.rect(mx + 8, my, len(info)*4 + 4, 7, 0) # Fondo negro pequeño
            pyxel.text(mx + 10, my + 1, info, 11) # Texto verde
            
            # Dibuja una cruz roja donde estás apuntando
            pyxel.line(mx - 4, my, mx + 4, my, 8)
            pyxel.line(mx, my - 4, mx, my + 4, 8)

# Ejecutar
if __name__ == "__main__":
    Game()
