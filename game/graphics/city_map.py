import pyxel

NODES = {
    "ELEJIDO": (40, 60),
    "CASA_CULTURA": (90, 60),
    "HOSPITAL": (140, 90),
    "PATRIA": (110, 140),
    "EPN": (170, 180),
}

EDGES = [
    ("ELEJIDO", "CASA_CULTURA"),
    ("CASA_CULTURA", "HOSPITAL"),
    ("HOSPITAL", "PATRIA"),
    ("PATRIA", "EPN"),
    ("CASA_CULTURA", "PATRIA"),
]


def draw_city(camera):
    pyxel.cls(11)

    for a, b in EDGES:
        ax, ay = NODES[a]
        bx, by = NODES[b]
        pyxel.line(
            ax - camera.x,
            ay - camera.y,
            bx - camera.x,
            by - camera.y,
            6,
        )

    for name, (x, y) in NODES.items():
        pyxel.circ(x - camera.x, y - camera.y, 4, 2)
        pyxel.text(x - camera.x - 8, y - camera.y - 10, name[:3], 7)

