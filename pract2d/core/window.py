import sdl2 as sdl

class Window(object):
	def __init__(self, title, width, height):
		self.titile = title
		self.width = width
		self.height = height

	def flip(self):
		pass

	def make_current(self, context):
		pass

	def destroy(self):
		pass