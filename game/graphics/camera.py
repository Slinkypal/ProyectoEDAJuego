class Camera:
    def __init__(self, view_w, view_h, world_w, world_h):
        self.x = 0
        self.y = 0
        self.view_w = view_w
        self.view_h = view_h
        self.world_w = world_w
        self.world_h = world_h

        # Dead zone (porcentaje del viewport)
        self.dead_w = int(view_w * 0.35)
        self.dead_h = int(view_h * 0.35)

        # Objetivo para lerp
        self.target_x = 0
        self.target_y = 0

        # Suavizado (0=no sigue, 1=sigue al instante). 0.15–0.25 funciona bien.
        self.smooth = 0.18

        # Shake
        self.shake_frames = 0
        self.shake_intensity = 0

    def follow(self, px, py):
        # Determina rectángulo dead-zone centrado en cámara
        dz_left   = self.x + (self.view_w - self.dead_w) // 2
        dz_right  = dz_left + self.dead_w
        dz_top    = self.y + (self.view_h - self.dead_h) // 2
        dz_bottom = dz_top + self.dead_h

        # Solo ajusta objetivo cuando el jugador sale de la dead-zone
        tx, ty = self.x, self.y
        if px < dz_left:
            tx = px - (self.view_w - self.dead_w) // 2
        elif px > dz_right:
            tx = px - (self.view_w + self.dead_w) // 2
        if py < dz_top:
            ty = py - (self.view_h - self.dead_h) // 2
        elif py > dz_bottom:
            ty = py - (self.view_h + self.dead_h) // 2

        # Lerp hacia el objetivo
        self.target_x = max(0, min(self.world_w - self.view_w, tx))
        self.target_y = max(0, min(self.world_h - self.view_h, ty))

        self.x += (self.target_x - self.x) * self.smooth
        self.y += (self.target_y - self.y) * self.smooth

        # Shake opcional
        if self.shake_frames > 0:
            import random
            self.x += random.uniform(-self.shake_intensity, self.shake_intensity)
            self.y += random.uniform(-self.shake_intensity, self.shake_intensity)
            self.shake_frames -= 1

        # Clamp final (por si shake empuja fuera)
        self.x = max(0, min(self.world_w - self.view_w, self.x))
        self.y = max(0, min(self.world_h - self.view_h, self.y))

    def start_shake(self, frames=10, intensity=1.5):
        self.shake_frames = frames
        self.shake_intensity = intensity
