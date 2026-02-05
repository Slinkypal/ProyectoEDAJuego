import pyxel

SCREEN_W, SCREEN_H = 256, 192
TILE_SIZE = 8
TM_GROUND = 0 

# Variables globales para el tamaño del mundo
WORLD_W = 0
WORLD_H = 0

# Coordenadas de los nodos (en píxeles reales del mapa)
NODES = {
    "EL_EJIDO":         (48, 256),
    "El ARBOLITO":      (296, 312),
    "CASA_CULTURA":     (112, 168),
    "MC_DONALDS":       (120, 40),
    "KFC":              (56, 40),
    "EMBAJADA FRANCESA":(176, 40),
    "PATRIA":           (56, 88),
    "ESTACION_BUS":     (295, 40),
    "MURAL":            (392, 40),
    "PUCE":             (600, 32),
    "CEC":              (704, 64),
    "HOSPITAL":         (632, 232),
    "EPN":              (848, 32),
}


def load_resources():
    pyxel.load("graphics/resources.pyxres")
    
    tm = pyxel.tilemap(TM_GROUND)
    global WORLD_W, WORLD_H
    WORLD_W = tm.width * TILE_SIZE
    WORLD_H = tm.height * TILE_SIZE

def draw_city(camera):
    # Dibujar Tilemap
    # bltm(x, y, tm, u, v, w, h)
    # x,y: dónde dibujar en pantalla
    # tm: índice del tilemap
    # u,v: coordenadas origen en el tilemap (en píxeles, por eso /TILE_SIZE * TILE_SIZE es redundante si no hay zoom)
    
    pyxel.bltm(
        -camera.x, -camera.y, 
        TM_GROUND, 
        0, 0, 
        WORLD_W, WORLD_H, 
    )

    # Dibujar Nodos (POIs)
    cx, cy = camera.x, camera.y
    for name, (nx, ny) in NODES.items():
        # Culling visual
        if (cx - 20 <= nx <= cx + 276) and (cy - 20 <= ny <= cy + 212):
            screen_x = nx - cx
            screen_y = ny - cy
            
            pyxel.circ(screen_x, screen_y, 4, 10)
            pyxel.circb(screen_x, screen_y, 4, 0)
            
            # Nombre del nodo
            text_w = len(name) * 4
            pyxel.text(screen_x - text_w//2, screen_y - 10, name, 0)
            pyxel.text(screen_x - text_w//2, screen_y - 11, name, 7)
