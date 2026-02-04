import json
import math
import random

import pyxel

from game.save_manager import save_results
from game.states import END, MENU, NODE_MENU, PLAYING, QUESTION
from graphics.camera import Camera
from graphics.city_map import EDGES, NODES, draw_city
from player import Player
from structures.graph import Graph

with open("data/questions.json", encoding="utf8") as f:
    QUESTION_POOL = json.load(f)["questions"]


class Game:
    def __init__(self):
        pyxel.init(256, 256, title="Camino a la EPN")

        self.state = MENU
        self.camera = Camera(256, 256)

        self.players = [
            Player("Jugador 1", *NODES["ELEJIDO"]),
            Player("Jugador 2", *NODES["CASA_CULTURA"]),
        ]

        self.turn = 0
        self.speed = 2

        self.current_node = None
        self.previous_node = None
        self.current_question = None
        self.available_questions = QUESTION_POOL[:]

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
                self.current_question = self.get_random_question()
                self.state = QUESTION
            if pyxel.btnp(pyxel.KEY_Q):
                self.state = PLAYING

        elif self.state == QUESTION:
            if pyxel.btnp(pyxel.KEY_Y):
                self.answer(True)
            if pyxel.btnp(pyxel.KEY_N):
                self.answer(False)
            if pyxel.btnp(pyxel.KEY_T):
                self.answer(True)
            if pyxel.btnp(pyxel.KEY_F):
                self.answer(False)

        elif self.state == END:
            if pyxel.btnp(pyxel.KEY_ESCAPE):
                pyxel.quit()

    def move_player(self):
        player = self.players[self.turn]
        nx, ny = player.x, player.y

        if pyxel.btn(pyxel.KEY_W):
            ny -= self.speed
        if pyxel.btn(pyxel.KEY_S):
            ny += self.speed
        if pyxel.btn(pyxel.KEY_A):
            nx -= self.speed
        if pyxel.btn(pyxel.KEY_D):
            nx += self.speed

        player.x, player.y = nx, ny
        self.camera.follow(player.x, player.y)

    def detect_node(self):
        player = self.players[self.turn]
        for node, (x, y) in NODES.items():
            if math.dist((player.x, player.y), (x, y)) < 8:
                if self.previous_node == node:
                    return
                if self.previous_node and not self.is_connected(self.previous_node, node):
                    player.score -= 5
                    player.x, player.y = NODES[self.previous_node]
                    self.camera.follow(player.x, player.y)
                    return

                self.current_node = node
                self.state = NODE_MENU

    def answer(self, correct):
        player = self.players[self.turn]
        question = self.current_question

        player.tree.add(question, correct)

        player.score += 10 if correct else -5

        self.graph.add_node(self.current_node)
        if self.previous_node:
            self.graph.add_node(self.previous_node)
            cost = 1 if correct else 5
            self.graph.add_edge(self.previous_node, self.current_node, cost)

        self.previous_node = self.current_node
        self.current_question = None

        if self.current_node == "EPN":
            mst, total_cost = self.graph.kruskal()
            save_results(self.players, mst, total_cost)
            self.state = END
            return

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

            player = self.players[self.turn]
            pyxel.rect(
                player.x - self.camera.x,
                player.y - self.camera.y,
                6,
                6,
                0,
            )
            pyxel.text(5, 5, f"{player.name} Puntaje: {player.score}", 7)

            if self.state == NODE_MENU:
                pyxel.rect(40, 190, 180, 40, 1)
                pyxel.text(50, 200, "E - Ver pregunta", 7)
                pyxel.text(50, 215, "Q - Cancelar", 7)

            if self.state == QUESTION:
                pyxel.rect(10, 180, 236, 60, 1)
                pyxel.text(20, 190, self.current_question, 7)
                pyxel.text(20, 210, "Y/T = SI | N/F = NO", 7)

        elif self.state == END:
            pyxel.cls(0)
            pyxel.text(70, 100, "LLEGASTE A LA EPN", 7)
            pyxel.text(40, 130, "RESULTADO GUARDADO", 7)
            pyxel.text(50, 160, "ESC - SALIR", 7)

    def get_random_question(self):
        if not self.available_questions:
            self.available_questions = QUESTION_POOL[:]
        self.current_question = random.choice(self.available_questions)
        self.available_questions.remove(self.current_question)
        return self.current_question

    @staticmethod
    def is_connected(a, b):
        return (a, b) in EDGES or (b, a) in EDGES


Game()