import pyxel

NODES = {
    "EL_EJIDO": (6, 32),
    "CASA_CULTURA": (7, 21),
    "EMBAJADA_FRANCESA": (18, 4),
    "PATRIA": (20, 10),
    "PUCE": (70, 4),
    "EPN": (103, 5)
}

def draw_city(camera):
    pyxel.cls(0)
    pyxel.bltm(-camera.x,-camera.y,0,0,0,128,128)

def draw_nodes(camera):
    for x,y in NODES.values():
        pyxel.blt(x-camera.x,y-camera.y,0,0,0,8,8)
