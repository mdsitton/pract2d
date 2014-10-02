import ctypes as ct
import types
import sdl2 as sdl
import window

class EventListenerBase(object):
    def quit(self):
        pass

    def key_up(self):
        pass

    def key_down(self):
        pass

    def window_close(self):
        pass

    def window_resize(self):
        pass

class Events(object):

    def __init__(self):
        sdl.SDL_InitSubSystem(sdl.SDL_INIT_EVENTS)

        self.funcListeners = []
        self.classListeners = []

    def get_listener_list(self, obj):
        if isinstance(obj, types.InstanceType):
            return self.classListeners
        else:
            return self.funcListeners

    def add_listener(self, listenerObj):
        listenerList = self.get_listener_list(listenerObj)

        if not listenerObj in listenerList:
            listenerList.append(listenerObj)

    def remove_listener(self, listenerObj):
        listenerList = self.get_listener_list(listenerObj)

        if listenerObj in listenerList:
            listenerList.remove(listenerObj)

    def broadcast_event(self, event, args):
        for listener in self.classListeners:
            getattr(listener, event)(*args)
        for listener in self.funcListeners:
            listener(event, args)

    def process(self):
        event = sdl.SDL_Event()

        while sdl.SDL_PollEvent(ct.byref(event)):
            # Events with sub-event types
            # These sub-events can be dispatched instead of the main event.
            eventName = None
            data = None

            if event.type == sdl.SDL_QUIT:
                eventName = 'quit'
                data = tuple()

            elif event.type == sdl.SDL_KEYUP:
                eventName = 'key_up'

                data = (event.key.keysym.scancode,
                        event.key.keysym.mod)

            elif event.type == sdl.SDL_KEYDOWN:
                eventName = 'key_down'
                data = (event.key.keysym.scancode,
                        event.key.keysym.sym,
                        event.key.keysym.mod)

            elif event.type == sdl.SDL_WINDOWEVENT:
                _winEvent = event.window.event
                sdlWinID = event.window.windowID
                winID = window.WindowManager._from_sdl_id(sdlWinID)
                # Might use later on but for now its just here
                windowInstance = window.WindowManager.get_window(winID)

                if _winEvent == sdl.SDL_WINDOWEVENT_CLOSE:
                    eventName = 'window_close'
                    data = (winID,)

                elif _winEvent == sdl.SDL_WINDOWEVENT_RESIZED:
                    eventName = 'window_resize'
                    data = (winID, event.window.data1, event.window.data2)
            if eventName and data:
                self.broadcast_event(eventName, data)
