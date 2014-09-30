import sdl2 as sdl

def init_video():
    sdl.SDL_Int(0)
    sdl.SDL_InitSubSystem(sdl.SDL_INT_VIDEO)

class Window(object):
    def __init__(self, title, width, height, fullscreen):
        self.title = title
        self.w = width
        self.h = height
        self.x = sdl.SDL_WINDOWPOS_UNDEFINED
        self.y = sdl.SDL_WINDOWPOS_UNDEFINED
        self.fullscreen = fullscreen

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