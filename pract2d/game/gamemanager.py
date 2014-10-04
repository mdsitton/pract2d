from pract2d.core import events
from pract2d.core import window
from pract2d.core import context

from pract2d.core import glmath
from pract2d.core import files

import OpenGL.GL as gl
from PIL import Image

class GameManager(object):
    def __init__(self):

        self.width = 800
        self.height = 600

        self.events = events.Events()
        self.window = window.Window('Hello World!', self.width, self.height, False)
        self.context = context.Context(3, 3)
        self.context.window = self.window
        self.running = False

        self.events.add_listener(self.event_handler)

        print ('test')
        # Get opengl version number
        glVersionMajor = gl.glGetIntegerv(gl.GL_MAJOR_VERSION)
        glVersionMinor = gl.glGetIntegerv(gl.GL_MINOR_VERSION)
        print (gl.glGetString(gl.GL_VERSION))
        print(glVersionMajor, glVersionMinor)

        #images
        tmpChar = Image.open('./data/character.png')
        if ''.join(tmpChar.getbands()) != 'RGBA':
            tmpChar = tmpChar.convert('RGBA')

        self.character = list(tmpChar.getdata())

        print files.get_path()

        # shaders
        vsPath = files.resolve_path("data", "shaders", "main.vs")
        fsPath = files.resolve_path("data", "shaders", "main.fs")

        vsStrData = files.read_file(vsPath)
        fsStrData = files.read_file(fsPath)

        self.vertexShader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        gl.glShaderSource(self.vertexShader, vsStrData)
        gl.glCompileShader(self.vertexShader)
        
        status = gl.glGetShaderiv(self.vertexShader, gl.GL_COMPILE_STATUS)

        if not status:
            print ("Error Vertex Shader")


        self.fragmentShader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
        gl.glShaderSource(self.fragmentShader, fsStrData)
        gl.glCompileShader(self.fragmentShader)

        status = gl.glGetShaderiv(self.fragmentShader, gl.GL_COMPILE_STATUS)

        if not status:
            print ("Error Fragment Shader")

        self.program = gl.glCreateProgram()
        gl.glAttachShader(self.program, self.vertexShader)
        gl.glAttachShader(self.program, self.fragmentShader)
        gl.glLinkProgram(self.program)

        status = gl.glGetProgramiv(self.program, gl.GL_LINK_STATUS)

        if status:
            print ("Program linked successfully.")
        else:
            print ("Linking error: ")

        test = gl.glGetProgramInfoLog(self.program)
        print (test)
        gl.glUseProgram(self.program)

        self.orthoLoc = gl.glGetUniformLocation(self.program, "ortho")
        self.modelLoc = gl.glGetUniformLocation(self.program, "model")


        self.vao = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vao)

        self.vertLoc = gl.glGetAttribLocation(self.program, b'position')

        # Math
        self.ortho = glmath.ortho(0.0, self.height, self.width, 0.0, -1.0, 1.0)
        self.model = glmath.Matrix(4)

        self.quad = [0.0, 0.0,  10.0, 0.0,  0.0, 10.0,  10.0, 10.0]
        typedQuad = (gl.GLfloat * len(self.quad))

        self.quadBuffer = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.quadBuffer)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, typedQuad(*self.quad), gl.GL_STATIC_DRAW)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, 0)

        gl.glEnableVertexAttribArray(self.vertLoc)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.quadBuffer)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)

        gl.glDisableVertexAttribArray(self.vertLoc)

        gl.glUniformMatrix4fv(self.orthoLoc, 1, gl.GL_FALSE, self.ortho.matrix)
        gl.glUniformMatrix4fv(self.modelLoc, 1, gl.GL_FALSE, self.model.matrix)

    def render(self):
        gl.glClearColor(0.5, 0.5, 0.5, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.quadBuffer)
        gl.glEnableVertexAttribArray(self.vertLoc)
        gl.glVertexAttribPointer(self.vertLoc, 2, gl.GL_FLOAT, gl.GL_FALSE, 0, 0)

        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 4)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
        gl.glDisableVertexAttribArray(self.vertLoc)

    def update(self):
        pass#gl.glUniformMatrix4fv(self.modelLoc, 1, GL_FALSE, self.model)

    def event_handler(self, event, data):
        if event == 'quit':
            self.running = False
        elif event == 'window_close':
            print ('Window {} needs to be closed.'.format(data[0]))
            winInstance= window.WindowManager.get_window(data[0])
            winInstance.destroy()
            if len(window.WindowManager.windows) < 1:
                self.running = False

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
