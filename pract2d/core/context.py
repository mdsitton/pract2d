import sdl2 as sdl

class ContextManager(object):
    '''
    This class collects all contexts inside static variables.
    It's similar to WindowManager in purpose 
    '''
    contexts = []

    def register(self):
        if not self in ContextManager.contexts:
            conID = len(ContextManager.contexts)

            ContextManager.contexts.append(self)

            return conID

    def unregister(self):
        if self in ContextManager.contexts:
            for n, item in enumerate(ContextManager.contexts):
                if item is self:
                    # We don't want to remove the item in the list
                    # Because that would invalidate all other id's
                    ContextManager.contexts[n] = None
                    break


class Context(ContextManager):
    def __init__(self, major, minor, msaa=2):
        self.major = major
        self.minor = minor
        self.msaa = msaa

        self.context = None
        self._window = None

        self.id = self.register()

        sdl.SDL_GL_SetAttribute(sdl.SDL_GL_DOUBLEBUFFER, 1)

        sdl.SDL_GL_SetAttribute(sdl.SDL_GL_CONTEXT_MAJOR_VERSION, major)
        sdl.SDL_GL_SetAttribute(sdl.SDL_GL_CONTEXT_MINOR_VERSION, minor)

        sdl.SDL_GL_SetAttribute(sdl.SDL_GL_CONTEXT_PROFILE_MASK, sdl.SDL_GL_CONTEXT_PROFILE_CORE)

        if msaa < 0:
            sdl.SDL_GL_SetAttribute(sdl.SDL_GL_MULTISAMPLEBUFFERS, 1)
            sdl.SDL_GL_SetAttribute(sdl.SDL_GL_MULTISAMPLESAMPLES, msaa)

    def destroy(self):
        sdl.SDL_GL_DeleteContext(self.context)
        self.unregister()

    @property
    def window(self):
        return self._window

    @window.setter
    def window(self, win):
        self._window = win
        if self.context == None:
            # Create context if not already created
            self.context = sdl.SDL_GL_CreateContext(self._window.window)
