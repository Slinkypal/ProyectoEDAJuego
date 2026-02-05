import json, math, random, pyxel
from graphics.camera import Camera
from graphics.city_map import draw_city, draw_nodes, NODES
from graphics.loader import load_resources
from game_management.player import Player
from structures.graph import Graph
from game_management.states import *

with open("assets/questions.json", encoding="utf8") as f:
    QUESTION_POOL = json.load(f)["questions"]

class Game:
    def __init__(self):
        pyxel.init(256,256,title="Camino a la EPN")
        load_resources()

        self.state = MENU
        self.camera = Camera(256,256)

        self.players = [
            Player("Jugador 1", *NODES["EL_EJIDO"]),
            Player("Jugador 2", *NODES["CASA_CULTURA"])
        ]

        self.turn = 0
        self.graph = Graph()
        self.current_node = None
        self.previous_node = None
        self.available_questions = QUESTION_POOL[:]

        pyxel.run(self.update, self.draw)

    def update(self):
        if self.state == MENU and pyxel.btnp(pyxel.KEY_RETURN):
            self.state = PLAYING
        elif self.state == PLAYING:
            self.move()
            self.check_node()

    def move(self):
        p = self.players[self.turn]
        if pyxel.btn(pyxel.KEY_W): p.y -= 2
        if pyxel.btn(pyxel.KEY_S): p.y += 2
        if pyxel.btn(pyxel.KEY_A): p.x -= 2
        if pyxel.btn(pyxel.KEY_D): p.x += 2
        self.camera.follow(p.x, p.y)

    def check_node(self):
        p = self.players[self.turn]
        for n,(x,y) in NODES.items():
            if math.dist((p.x,p.y),(x,y)) < 8:
                self.current_node = n
                self.state = QUESTION

    def draw(self):
        draw_city(self.camera)
        draw_nodes(self.camera)
        p = self.players[self.turn]
        pyxel.blt(p.x-self.camera.x,p.y-self.camera.y,0,8,0,8,8)

Game()