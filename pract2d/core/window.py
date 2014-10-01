import sdl2 as sdl

def init_video():
    sdl.SDL_Int(0)
    sdl.SDL_InitSubSystem(sdl.SDL_INT_VIDEO)

class BWinMan(object):
    '''
    This class is a bit of an odd one
    Its not required, but i thought since what im doing here is a bit differant
    It might be good to seperate it out in a base class for more clarity.

    Basically what i going on here, this base class contains static values
    that will contain various values needed for multiple window operation
    Mainly a list of all window instances, and a dict to translate from sdl window
    id's to our internal ones. (needed in the events code)
    '''
    _windows = []
    _windowMap = {}

    def register(self):
        if not instance in BWinMan._windows:
            winID = len(BWinMan._windows)
            sldID = sdl.SDL_GetWindowID(self.window)

            BWinMan._windows.append(instance)
            BWinMan._windowMap[sdlID] = winID

            return winID

    def unregister(self):
        if instance in BWinMan.windows:
            for n, item in enumerate(self.window):
                if item is instance:
                    # We don't want to remove the item in the list
                    # Because that would invalidate all other id's
                    BWinMan.windows[n] = None

    def _from_sdl_id(self, sdlWindowID):
        return BWinMan._windowMap[sdlWindowID]


class Window(BWinMan):
    def __init__(self, title, width, height, fullscreen):
        self.title = title
        self.w = width
        self.h = height
        self.x = sdl.SDL_WINDOWPOS_UNDEFINED
        self.y = sdl.SDL_WINDOWPOS_UNDEFINED
        self.fullscreen = fullscreen

        # Register with base class
        self.id = self.register()

        self.context = None

        self.flags = sdl.SDL_WINDOW_OPENGL | sdl.SDL_WINDOW_RESIZABLE

        if fullscreen:
            self.flags |= sdl.SDL_WINDOW_FULLSCREEN
        else:
            self.x = sdl.SDL_WINDOWPOS_CENTERED
            self.y = sdl.SDL_WINDOWPOS_CENTERED

        self.window = sdl.SDL_CreateWindow(self.title, self.x, self.y, self.w, self.h)


    def flip(self):
        sdl.SDL_GL_SwapWindow(self.window)

    def make_current(self, context):
        if context:
            window = self.window
            self.context = context

            context.window = self
            context = context.context
        else:
            if self.context:
                self.context.window = None

            window = None
            context = None
            self.context = None

        sdl.SDL_GL_MakeCurrent(window, context)

    def destroy(self):
        sdl.SDL_DestroyWindow(self.window)
        # Unregister from base class
        self.unregister()