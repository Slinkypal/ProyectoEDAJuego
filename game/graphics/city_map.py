import pyxel

# Configuración de Pantalla
SCREEN_W, SCREEN_H = 256, 192
NATIVE_TILE = 8         # Tamaño real de un tile en el editor de Pyxel (8x8)
DRAW_SCALE = 1.0        # Factor de Zoom (2x)
TILE_SCREEN = NATIVE_TILE * DRAW_SCALE   # 16px visuales en pantalla

TM_GROUND = 0  # Índice del Tilemap

# Puntos de interés (Coordenadas ajustadas al mundo escalado)
# Nota: Ajusté las posiciones multiplicando por TILE_SCREEN para que sea más fácil leer
NODES = {
    "EL_EJIDO":         (6 * TILE_SCREEN, 32 * TILE_SCREEN),
    "El ARBOLITO":      (37 * TILE_SCREEN, 39 * TILE_SCREEN),
    "CASA_CULTURA":     (14 * TILE_SCREEN, 21 * TILE_SCREEN),
    "MC_DONALDS":       (15 * TILE_SCREEN, 5 * TILE_SCREEN),
    "KFC":              (7 * TILE_SCREEN, 5 * TILE_SCREEN),
    "EMBAJADA FRANCESA":(22 * TILE_SCREEN, 5 * TILE_SCREEN),
    "PATRIA":           (7 * TILE_SCREEN, 11 * TILE_SCREEN),
    "ESTACION_BUS":     (44 * TILE_SCREEN, 4 * TILE_SCREEN),
    "MURAL":            (49 * TILE_SCREEN, 5 * TILE_SCREEN),
    "PUCE":             (75 * TILE_SCREEN, 4 * TILE_SCREEN),
    "CEC":              (88 * TILE_SCREEN, 8 * TILE_SCREEN),
    "HOSPITAL":         (79 * TILE_SCREEN, 29 * TILE_SCREEN),
    "EPN":              (106 * TILE_SCREEN, 4 * TILE_SCREEN),
}

# Variables globales para el tamaño del mundo
WORLD_W = 0
WORLD_H = 0

def load_resources():
    
    #Carga el .pyxres y define los límites del mundo.
    
    # Asegúrate de que la ruta sea correcta según tu estructura de carpetas
    pyxel.load("graphics/resources.pyxres")
    
    # Obtenemos el tamaño del mapa 0 directamente de Pyxel
    tm = pyxel.tilemap(TM_GROUND)
    # El ancho en píxeles escalados = (ancho en tiles * 8) * 2
    global WORLD_W, WORLD_H
    WORLD_W = tm.width * NATIVE_TILE * DRAW_SCALE
    WORLD_H = tm.height * NATIVE_TILE * DRAW_SCALE

def draw_city(camera):
    """
    Dibuja el mapa con el cálculo correcto de paralaje/zoom.
    """
    # 1. Convertir la posición de la cámara (Mundo Escalado) a (Mundo Nativo)
    #    Si la cámara está en x=16 (escalado), en el tilemap original es x=8.
    native_cam_x = camera.x / DRAW_SCALE
    native_cam_y = camera.y / DRAW_SCALE

    # 2. Calcular 'u' y 'v' (Tile inicial superior izquierdo en el tilemap)
    #    Simplemente dividimos la posición nativa entre 8 (NATIVE_TILE)
    u = native_cam_x // NATIVE_TILE
    v = native_cam_y // NATIVE_TILE

    # 3. Calcular el Offset (Desplazamiento fino en píxeles)
    #    Es el residuo de la división, multiplicado por el ZOOM para pantalla.
    #    Esto suaviza el movimiento pixel a pixel.
    ox = -(native_cam_x % NATIVE_TILE) * DRAW_SCALE
    oy = -(native_cam_y % NATIVE_TILE) * DRAW_SCALE

    # 4. Calcular cuántos tiles necesitamos dibujar para llenar la pantalla
    #    Sumamos 2 extra para evitar bordes vacíos al hacer scroll
    w_tiles = (SCREEN_W // NATIVE_TILE) + 2
    h_tiles = (SCREEN_H // NATIVE_TILE) + 2

    # 5. Dibujar el mapa usando bltm con escala
    pyxel.bltm(
        ox, oy,         # Posición en pantalla (con offset negativo)
        TM_GROUND,      # Número de Tilemap
        u * NATIVE_TILE, # Coordenada X origen en el tilemap (en píxeles nativos)
        v * NATIVE_TILE, # Coordenada Y origen en el tilemap
        w_tiles * NATIVE_TILE, # Ancho a copiar
        h_tiles * NATIVE_TILE, # Alto a copiar
        scale=DRAW_SCALE # ¡El truco mágico!
    )

    # --- Dibujar Nodos (POIs) ---
    cx, cy = camera.x, camera.y
    for name, (nx, ny) in NODES.items():
        # Culling: Solo dibujar si está dentro de la vista de la cámara
        if (cx - 20 <= nx <= cx + camera.view_w + 20) and \
           (cy - 20 <= ny <= cy + camera.view_h + 20):
            
            # Convertir coordenadas de mundo a coordenadas de pantalla
            screen_x = nx - cx
            screen_y = ny - cy
            
            # Dibujar un círculo y el nombre
            pyxel.circ(screen_x, screen_y, 4, 10) # Círculo amarillo
            pyxel.circb(screen_x, screen_y, 4, 0) # Borde negro
            
            # Texto centrado
            text_w = len(name) * 4
            pyxel.text(screen_x - text_w//2, screen_y - 8, name, 0) # Sombra
            pyxel.text(screen_x - text_w//2, screen_y - 9, name, 7) # Texto blanco

