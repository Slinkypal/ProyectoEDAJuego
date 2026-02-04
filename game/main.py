import pyxel, json, math
from player import Player
from graphics.camera import Camera
from graphics.city_map import draw_city, NODES
from structures.graph import Graph
from game.states import MENU, PLAYING, NODE_MENU, QUESTION, END
from game.save_manager import save_results

questions = json.load(open("assets/questions.json", encoding="utf8"))

class Game:
    def __init__(self):
        pyxel.init(256, 256, title="Camino a la EPN")

        self.state = MENU
        self.camera = Camera(256, 256)

        self.players = [
            Player("Jugador 1", *NODES["EL_EJIDO"]),
            Player("Jugador 2", *NODES["CASA_CULTURA"])
        ]

        self.turn = 0
        self.speed = 2

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

        if pyxel.btn(pyxel.KEY_W): ny -= self.speed
        if pyxel.btn(pyxel.KEY_S): ny += self.speed
        if pyxel.btn(pyxel.KEY_A): nx -= self.speed
        if pyxel.btn(pyxel.KEY_D): nx += self.speed

        p.x, p.y = nx, ny
        self.camera.follow(p.x, p.y)

    def detect_node(self):
        p = self.players[self.turn]
        for node, (x, y) in NODES.items():
            if math.dist((p.x, p.y), (x, y)) < 8:
                self.current_node = node
                self.state = NODE_MENU

    def answer(self, correct):
        p = self.players[self.turn]
        question = questions[self.current_node]

        # 🌳 Árbol binario
        p.tree.add(question, correct)

        # 🎯 Puntaje
        p.score += 10 if correct else -5

        # 🧠 Grafo dinámico
        self.graph.add_node(self.current_node)
        if self.previous_node:
            cost = 1 if correct else 5
            self.graph.add_edge(self.previous_node, self.current_node, cost)

        self.previous_node = self.current_node

        # 🏁 Llegó a la EPN
        if self.current_node == "EPN":
            mst, total_cost = self.graph.kruskal()
            save_results(self.players, mst, total_cost)
            self.state = END
            return

        # 🔄 Cambio de turno
        self.turn = (self.turn + 1) % 2
        self.state = PLAYING

    def draw(self):
        pyxel.cls(11)

        if self.state == MENU:
            pyxel.text(70, 100, "CAMINO A LA EPN", 7)
            pyxel.text(60, 130, "ENTER - JUGAR", 7)
            pyxel.text(60, 150, "ESC - SALIR", 7)

        elif self.state in [PLAYING, NODE_MENU, QUESTION]:
            draw_city(self.camera)

            p = self.players[self.turn]
            pyxel.rect(p.x - self.camera.x, p.y - self.camera.y, 6, 6, 0)
            pyxel.text(5, 5, f"{p.name} Puntaje: {p.score}", 7)

            if self.state == NODE_MENU:
                pyxel.rect(40, 190, 180, 40, 1)
                pyxel.text(50, 200, "E - Ver pregunta", 7)
                pyxel.text(50, 215, "Q - Cancelar", 7)

            if self.state == QUESTION:
                pyxel.rect(10, 180, 236, 60, 1)
                pyxel.text(20, 190, questions[self.current_node], 7)
                pyxel.text(20, 210, "Y = SI | N = NO", 7)

        elif self.state == END:
            pyxel.cls(0)
            pyxel.text(70, 100, "LLEGASTE A LA EPN", 7)
            pyxel.text(40, 130, "RESULTADO GUARDADO", 7)
            pyxel.text(50, 160, "ESC - SALIR", 7)

Game()
