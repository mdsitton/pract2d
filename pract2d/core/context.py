import sdl2 as sdl

class Context(object):
    def __init__(self, major, minor, msaa=2):
        self.major = major
        self.minor = minor
        self.msaa = msaa

        self.context = None
        self._window = None

        sdl.SDL_GL_SetAttribute(sdl.SDL_GL_DOUBLEBUFFER, 1)

        sdl.SDL_GL_SetAttribute(sdl.SDL_GL_CONTEXT_MAJOR_VERSION, major)
        sdl.SDL_GL_SetAttribute(sdl.SDL_GL_CONTEXT_MINOR_VERSION, minor)

        sdl.SDL_GL_SetAttribute(sdl.SDL_GL_CONTEXT_PROFILE_MASK, sdl.SDL_GL_CONTEXT_PROFILE_CORE)

        if msaa < 0:
            sdl.SDL_GL_SetAttribute(sdl.SDL_GL_MULTISAMPLEBUFFERS, 1)
            sdl.SDL_GL_SetAttribute(sdl.SDL_GL_MULTISAMPLESAMPLES, msaa)

    def destroy(self):
        sdl.SDL_GL_DeleteContext(self.context)

    @property
    def window(self):
        return self._window

    @window.setter
    def window(self, win):
        self._window = win
        if self.context == None:
            # Create context if not already created
            self.context = sdl.SDL_GL_CreateContext(self._window.window)
