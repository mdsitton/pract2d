from pract2d.core import events
from pract2d.core import window
from pract2d.core import context

import OpenGL.GL as gl

class GameManager(object):
    def __init__(self):
        self.events = events.Events()
        self.window = window.Window('Hello World!', 800, 600, False)
        self.context = context.Context(3, 3)
        self.running = False

        self.events.add_listener(self.event_handler)

    def render(self):
        gl.glClearColor(1.0, 1.0, 1.0, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)


    def update(self):
        pass

    def event_handler(self, event, data):
        if event == 'quit':
            self.running = False
        elif event == 'window_close':
            print ('Window {} needs to be closed.'.format(data[0]))
            winInstance= window.WindowManager.get_window(data[0])
            winInstance.destroy()

    def do_run(self):
        self.events.process()
        self.update()
        for i in window.WindowManager.windows:
            i.make_current(self.context)
            self.render()
            i.flip()

    def run(self):
        self.running = True
        while self.running:
            self.do_run()
