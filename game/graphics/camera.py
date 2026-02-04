class Camera:
    def __init__(self, w, h):
        self.x = 0
        self.y = 0
        self.w = w
        self.h = h

    def follow(self, x, y):
        self.x = max(0, x - self.w // 2)
        self.y = max(0, y - self.h // 2)