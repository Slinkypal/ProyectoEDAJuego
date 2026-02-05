import pyxel
import json
import math
import sys
import random

try:
    import graphics.city_map as cm
    from graphics.camera import Camera
    from graphics.city_map import draw_city, NODES
    from game_management.player import Player
    from game_management.save_manager import save_results
    from game_management.states import MENU, PLAYING, NODE_MENU, QUESTION, END
    from structures.graph.graph import Graph
    from structures.binary_tree import QuestionBST

except ImportError:
    # Fallback por si ejecutas desde la raíz (para facilitar pruebas)
    import city_map as cm
    from camera import Camera
    from city_map import draw_city, NODES
    from player import Player
    from save_manager import save_results
    from states import MENU, PLAYING, NODE_MENU, QUESTION, END
    from graph import Graph
    from binary_tree import QuestionBST
#IDs para el arbol
NODE_IDS = {
    "EL_EJIDO": 100, "El ARBOLITO": 200, "CASA_CULTURA": 300, 
    "MC_DONALDS": 400, "KFC": 500, "EMBAJADA FRANCESA": 600,
    "PATRIA": 700, "ESTACION_BUS": 800, "MURAL": 900,
    "PUCE": 1000, "CEC": 1100, "HOSPITAL": 1200, "EPN": 1300
}

# Cargar preguntas
def load_question_tree():
    tree = QuestionBST()
    try:
        data = json.load(open("assets/questions.json", encoding="utf8"))

        for node_group in data:
            node_name = node_group["node"]
            questions = node_group["questions"]
            
        
            base_id = NODE_IDS.get(node_name, 9900) 
            
            for q_item in questions:
                unique_id = base_id + q_item["index"]
                tree.insert(unique_id, q_item["q"], q_item["a"])
                
    except FileNotFoundError:
        print("Error: assets/questions.json no encontrado.")
    return tree

# CLASE PRINCIPAL
class Game:
    # Iniciador
    def __init__(self):
        # Título y fps
        pyxel.init(256, 192, title="Camino a la EPN", fps=60)
        
        self.state = MENU
        cm.load_resources()
       
        # Configuración de Cámara
        self.camera = Camera(
            256,
            192,
            cm.WORLD_W,
            cm.WORLD_H
        )
        
        # Posición inicial
        pos1 = NODES["EL_EJIDO"]
        pos2 = NODES["CASA_CULTURA"]
        
        self.players = [
            Player("Jugador 1", pos1[0], pos1[1]),
            Player("Jugador 2", pos2[0], pos2[1])
        ]

        # Centrar cámara inicial
        self.camera.x = self.players[0].x - 128
        self.camera.y = self.players[0].y - 96

        self.turn = 0
        self.speed = 3
        self.current_node = None
        self.previous_node = None
        
        # Cooldown para no reactivar nodos instantáneamente
        self.node_cooldown = 0
        #Grafo
        self.graph = Graph()
        # Árbol de Nodos
        self.question_tree = load_question_tree()
        self.current_question_data = None
 

        pyxel.run(self.update, self.draw)
        
    # Manejo de controles
    def update(self):
        if self.node_cooldown > 0:
            self.node_cooldown -= 1

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
                base_id = NODE_IDS.get(self.current_node, 100)
                random_index = random.randint(1, 3) 
                search_id = base_id + random_index
                
                found_node = self.question_tree.search(search_id)
                
                # Fallback si el random falla
                if not found_node:
                    found_node = self.question_tree.search(base_id + 1)
                
                self.current_question_data = found_node
                
                # Fallback de seguridad total
                if not self.current_question_data:
                    class Dummy: pass
                    self.current_question_data = Dummy()
                    self.current_question_data.question = f"¿Pregunta generica para {self.current_node}?"
                    self.current_question_data.correct_answer = True

                self.state = QUESTION

            if pyxel.btnp(pyxel.KEY_Q):
                self.previous_node = self.current_node 
                
                self.node_cooldown = 30
                self.state = PLAYING

        elif self.state == QUESTION:
            if pyxel.btnp(pyxel.KEY_Y): self.answer(True)
            if pyxel.btnp(pyxel.KEY_N): self.answer(False)

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
            
        # BOUNDARIES
        
        half_w = p.w // 2
        half_h = p.h // 2
        
        # Límite izquierdo y derecho
        nx = max(half_w, min(nx, cm.WORLD_W - half_w))
        
        # Límite superior e inferior
        ny = max(half_h, min(ny, cm.WORLD_H - half_h))

        p.x, p.y = nx, ny
        self.camera.follow(p.x, p.y)

    def detect_node(self):
        if self.node_cooldown > 0: return

        p = self.players[self.turn]
        detection_radius = 16 
        
        for node, (x, y) in NODES.items():
            if math.dist((p.x, p.y), (x, y)) < detection_radius:
                # Evitar re-detectar el mismo nodo si no nos hemos movido a otro
                if node == self.previous_node and self.state == PLAYING:
                    continue

                self.current_node = node
                self.state = NODE_MENU
                break

    def answer(self, correct):
        # Logica del Arbol
        p = self.players[self.turn]

        if self.current_question_data:
            q_text = self.current_question_data.question
            real_answer = self.current_question_data.correct_answer

            is_correct = (correct == real_answer)  
        else:
            q_text = "Error data"
            is_correct = False

        p.tree.add(q_text, is_correct)

        p.score += 10 if is_correct else -5

        # Lógica del Grafo (Mapa)
        self.graph.add_node(self.current_node)
        
        if self.previous_node and self.previous_node != self.current_node:
            cost = 1 if is_correct else 5
            self.graph.add_edge(self.previous_node, self.current_node, cost)

        self.previous_node = self.current_node

        # Verificar condición de victoria (EPN)
        if self.current_node == "EPN":
            mst, total_cost = self.graph.kruskal()
            save_results(self.players, mst, total_cost)
            self.state = END
            return

        # Cambio de turno
        self.turn = (self.turn + 1) % 2
        
        #  Mover la cámara al siguiente jugador
        next_player = self.players[self.turn]
        self.camera.x = next_player.x - 128
        self.camera.y = next_player.y - 96
        
        # Clamp (Limitar) la cámara para que no salga del mapa
        max_x = self.camera.world_w - self.camera.view_w
        max_y = self.camera.world_h - self.camera.view_h
        self.camera.x = max(0, min(self.camera.x, max_x))
        self.camera.y = max(0, min(self.camera.y, max_y))

        #  Resetear estado para seguir jugando
        self.node_cooldown = 30
        self.state = PLAYING
        
    #Dibujamos el mapa
    def draw(self):
        pyxel.cls(12) # Azul claro (cielo) 

        if self.state == MENU:
            pyxel.cls(5) # Fondo azul oscuro para menú 
            pyxel.text(90, 80, "CAMINO A LA EPN", 7)
            pyxel.text(95, 110, "ENTER - JUGAR", 7)
            pyxel.text(100, 130, "ESC - SALIR", 7)
            
        elif self.state in [PLAYING, NODE_MENU, QUESTION]:
            draw_city(self.camera)

            for i, p in enumerate(self.players):
                es_su_turno = (i == self.turn)
                p.draw(self.camera.x, self.camera.y, es_su_turno)
            
            # HUD
            pyxel.rect(0, 0, 256, 12, 0)
            p_act = self.players[self.turn]
            pyxel.text(5, 3, f"Turno: {p_act.name} | Score: {p_act.score}", 7)
   
            # UI Menús
            if self.state == NODE_MENU:
                pyxel.rect(30, 150, 196, 35, 1)
                pyxel.rectb(30, 150, 196, 35, 7)
                pyxel.text(40, 158, f"Estas en: {self.current_node}", 7)
                pyxel.text(40, 168, "E - Responder Pregunta | Q - Cancelar", 6)

            if self.state == QUESTION:
                pyxel.rect(20, 40, 216, 100, 1)
                pyxel.rectb(20, 40, 216, 100, 7)
                
                if self.current_question_data:
                    ft = self.current_question_data.question
                    # Renderizado simple del texto
                    pyxel.text(30, 50, ft[:32], 7) 
                    pyxel.text(30, 60, ft[32:64], 7)
                    pyxel.text(30, 70, ft[64:], 7)
                
                pyxel.text(80, 110, "Y = VERDADERO  |  N = FALSO", 10)

        elif self.state == END:
            pyxel.cls(0)
            pyxel.text(90, 80, "LLEGASTE A LA EPN", 10)
            pyxel.text(80, 100, "RESULTADOS GUARDADOS EN CSV", 7)
            pyxel.text(100, 140, "ESC - SALIR", 7)

if __name__ == "__main__":
    Game()
