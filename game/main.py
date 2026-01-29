import pyxel
# Si ejecutan este archivo como ejecutable les mandara una pantalla
# Que dice hola mundo :)
# Tambien si pueden vean un tuto de pyxel
# Claro si no quieren usar otra cosa para la visualidad.
class App:
	def __init__(self):
		pyxel.init(160, 120, title="Hello World")
		pyxel.run(self.update, self.draw)

	def update(self):
		if pyxel.btnp(pyxel.KEY_Q):
			pyxel.quit()

	def draw(self):
		pyxel.cls(0)
		pyxel.text(55, 41, "Hello World!", 5)
if __name__ == "__main__":
	App()
