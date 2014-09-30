from pract2d.core import events
from pract2d.core import window
from pract2d.core import context

class GameManager(object):
	def __init__(self):
		self.events = events.Events()
		self.window = window.Window('Hello World!', 800, 600)
		self.context = context.Context(3, 3)

	def render(self):
		pass

	def update(self):
		pass

	def run():
		while self.event.run():
			self.update()
			self.render()
