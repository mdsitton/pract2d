from pract2d.core import events
from pract2d.core import window
from pract2d.core import context

from pract2d.core import glmath
from pract2d.core import files

import OpenGL.GL as gl
from PIL import Image

class ShaderBase(object):
    def create(self):
        self.shader = gl.glCreateShader(self.shaderType)
        gl.glShaderSource(self.shader, self.shaderData)
        gl.glCompileShader(self.shader)

        status = gl.glGetShaderiv(self.shader, gl.GL_COMPILE_STATUS)

        if not status:
            print (self.shaderErrorMessage)
            print (gl.glGetShaderInfoLog(self.shader))
        else:
            print (self.shaderSuccessMessage)


class VertexShader(ShaderBase):
    def __init__(self, path):
        self.shaderData = files.read_file(path)
        self.shaderErrorMessage = "Vertex Shader Compilation Error."
        self.shaderSuccessMessage = "Vertex Shader Compiled successfully."
        self.shaderType = gl.GL_VERTEX_SHADER


class FragmentShader(ShaderBase):
    def __init__(self, path):
        self.shaderData = files.read_file(path)
        self.shaderErrorMessage = "Fragment Shader Compilation Error."
        self.shaderSuccessMessage = "Fragment Shader Compiled successfully."
        self.shaderType = gl.GL_FRAGMENT_SHADER


class ShaderProgram(object):
    def __init__(self, vertex, fragment):

        self.uniforms = {}

        self.vertex = vertex
        self.fragment = fragment

        self.vertex.create()
        self.fragment.create()
        
        self.program = gl.glCreateProgram()

        gl.glAttachShader(self.program, self.vertex.shader)
        gl.glAttachShader(self.program, self.fragment.shader)

        gl.glLinkProgram(self.program)

        status = gl.glGetProgramiv(self.program, gl.GL_LINK_STATUS)

        if not status:
            print ("Linking error: ")
            print (gl.glGetProgramInfoLog(self.program))
        else:
            print ("Program linked successfully.")

    def use(self, using=True):
        if using is False:
            prog = 0
        else:
            prog = self.program
        gl.glUseProgram(prog)

    def get_attribute(self, name):
        return gl.glGetAttribLocation(self.program, name)

    def new_uniform(self, name):

        self.uniforms[name] = gl.glGetUniformLocation(self.program, name)

    def set_uniform(self, name, value):

        uniform = self.uniforms[name]

        if isinstance(value, glmath.Vector):
            value = value.vector

        if isinstance(value, glmath.Matrix):
            size = value.size
            data = value.c_matrix

            if size == 4:
                gl.glUniformMatrix4fv(uniform, 1, gl.GL_FALSE, data)
            elif size == 3:
                gl.glUniformMatrix3fv(uniform, 1, gl.GL_FALSE, data)
            elif size == 2:
                gl.glUniformMatrix2fv(uniform, 1, gl.GL_FALSE, data)

        elif isinstance(name, list) or isinstance(value, tuple):
            size = len(value)

            if isinstance(value[0], int):
                if size == 4:
                    gl.glUniform4i(uniform, *value)
                elif size == 3:
                    gl.glUniform3i(uniform, *value)
                elif size == 2:
                    gl.glUniform2i(uniform, *value)

            elif isinstance(value[0], float):
                if size == 4:
                    gl.glUniform4f(uniform, *value)
                elif size == 3:
                    gl.glUniform3f(uniform, *value)
                elif size == 2:
                    gl.glUniform2f(uniform, *value)

        elif isinstance(value, int):
            gl.glUniform1i(uniform, value)

        elif isinstance(value, float):
            gl.glUniform1f(uniform, value)


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

        vsPath = files.resolve_path("data", "shaders", "main.vs")
        fsPath = files.resolve_path("data", "shaders", "main.fs")

        vertex = VertexShader(vsPath)
        fragment = FragmentShader(fsPath)
        self.program = ShaderProgram(vertex, fragment)

        self.program.use()

        self.program.new_uniform('ortho')
        self.program.new_uniform('model')

        self.vao = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vao)

        self.vertLoc = self.program.get_attribute('position')

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

        self.program.set_uniform('ortho', self.ortho)
        self.program.set_uniform('model', self.model)

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
