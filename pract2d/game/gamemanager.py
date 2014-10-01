from pract2d.core import events
from pract2d.core import window
from pract2d.core import context

class GameManager(object):
    def __init__(self):
        self.events = events.Events()
        self.window = window.Window('Hello World!', 800, 600, False)
        self.window2 = window.Window('Hello World2!', 800, 600, False)
        self.window = window.Window('Hello World2w!', 800, 600, False)
        self.window2 = window.Window('Hello World22!', 800, 600, False)
        self.context = context.Context(3, 3)
        self.running = False

        self.events.add_listener(self.event_handler)

    def render(self):
        pass

    def update(self):
        pass

    def event_handler(self, event, data):
        if event == 'quit':
            self.running = False
        elif event == 'window_close':
            print ('Window {} needs to be closed.'.format(data[0]))
            winInstance= window.WindowManager.get_window(data[0])
            winInstance.destroy()


    def run(self):
        self.running = True
        while self.running:
            self.events.run()
            self.update()
            for i in window.WindowManager.windows:
                i.make_current(self.context)
                self.render()
                i.flip()
