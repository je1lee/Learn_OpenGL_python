import sys
import glfw
import OpenGL.GL as gl
import glm
from PIL import Image
from pathlib import Path
from ctypes import c_uint, c_float, sizeof, c_void_p

CURDIR = Path(__file__).parent.absolute()
RESDIR = CURDIR.joinpath("resources")
sys.path.append(str(CURDIR))

from shader import Shader


def Tex(fn):
    return RESDIR.joinpath("textures", fn)


def main():
    glfw.init()
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(800, 600, "LearnOpenGL", None, None)
    if not window:
        print("Window Creation failed!")
        glfw.terminate()

    glfw.make_context_current(window)
    glfw.set_window_size_callback(window, on_resize)

    shader = Shader(CURDIR / 'shaders/model.vs', CURDIR / 'shaders/model.fs')
   
    
    vertices = [
     # positions      tex_coords
    -0.5, -0.5, -0.5,  0.0, 0.0,
     0.5, -0.5, -0.5,  1.0, 0.0,
     0.5,  0.5, -0.5,  1.0, 1.0,
     0.5,  0.5, -0.5,  1.0, 1.0,
    -0.5,  0.5, -0.5,  0.0, 1.0,
    -0.5, -0.5, -0.5,  0.0, 0.0,

    -0.5, -0.5,  0.5,  0.0, 0.0,
     0.5, -0.5,  0.5,  1.0, 0.0,
     0.5,  0.5,  0.5,  1.0, 1.0,
     0.5,  0.5,  0.5,  1.0, 1.0,
    -0.5,  0.5,  0.5,  0.0, 1.0,
    -0.5, -0.5,  0.5,  0.0, 0.0,

    -0.5,  0.5,  0.5,  1.0, 0.0,
    -0.5,  0.5, -0.5,  1.0, 1.0,
    -0.5, -0.5, -0.5,  0.0, 1.0,
    -0.5, -0.5, -0.5,  0.0, 1.0,
    -0.5, -0.5,  0.5,  0.0, 0.0,
    -0.5,  0.5,  0.5,  1.0, 0.0,

     0.5,  0.5,  0.5,  1.0, 0.0,
     0.5,  0.5, -0.5,  1.0, 1.0,
     0.5, -0.5, -0.5,  0.0, 1.0,
     0.5, -0.5, -0.5,  0.0, 1.0,
     0.5, -0.5,  0.5,  0.0, 0.0,
     0.5,  0.5,  0.5,  1.0, 0.0,

    -0.5, -0.5, -0.5,  0.0, 1.0,
     0.5, -0.5, -0.5,  1.0, 1.0,
     0.5, -0.5,  0.5,  1.0, 0.0,
     0.5, -0.5,  0.5,  1.0, 0.0,
    -0.5, -0.5,  0.5,  0.0, 0.0,
    -0.5, -0.5, -0.5,  0.0, 1.0,

    -0.5,  0.5, -0.5,  0.0, 1.0,
     0.5,  0.5, -0.5,  1.0, 1.0,
     0.5,  0.5,  0.5,  1.0, 0.0,
     0.5,  0.5,  0.5,  1.0, 0.0,
    -0.5,  0.5,  0.5,  0.0, 0.0,
    -0.5,  0.5, -0.5,  0.0, 1.0
    ]
    vertices = (c_float * len(vertices))(*vertices)

    # indices = [
    #     0, 1, 3,
    #     1, 2, 3
    # ]
    # indices = (c_uint * len(indices))(*indices)

    vao = gl.glGenVertexArrays(1)
    gl.glBindVertexArray(vao)

    vbo = gl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
    gl.glBufferData(gl.GL_ARRAY_BUFFER, sizeof(vertices), vertices, gl.GL_STATIC_DRAW)

    # ebo = gl.glGenBuffers(1)
    # gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, ebo)
    # gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, gl.GL_STATIC_DRAW)

    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 5 * sizeof(c_float), c_void_p(0))
    gl.glEnableVertexAttribArray(0)

    gl.glVertexAttribPointer(1, 2, gl.GL_FLOAT, gl.GL_FALSE, 5 * sizeof(c_float), c_void_p(3 * sizeof(c_float)))
    gl.glEnableVertexAttribArray(1)

    # gl.glVertexAttribPointer(2, 2, gl.GL_FLOAT, gl.GL_FALSE, 8 * sizeof(c_float), c_void_p(6 * sizeof(c_float)))
    # gl.glEnableVertexAttribArray(2)

    # -- load texture
    texture = gl.glGenTextures(1)
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
    # -- texture wrapping
    gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
    gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
    # -- texture filterting
    gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
    gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)

    img = Image.open(Tex('dog.jpg')).transpose(Image.FLIP_TOP_BOTTOM)
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, img.width, img.height, 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, img.tobytes())
    gl.glGenerateMipmap(gl.GL_TEXTURE_2D)

    shader.use()
    # getUniformLoc 해줘야 제대로 읽어옴
    shader.set_int("texture", 0) 
    
    # depth test 사용
    gl.glEnable(gl.GL_DEPTH_TEST)

    while not glfw.window_should_close(window):
        process_input(window)

        gl.glClearColor(.2, .3, .3, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        
        gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
        
        shader.use()
        # model = glm.mat4()
        # model = glm.rotate(model, glm.radians(-55.0), glm.vec3([1.0, 0.0, 0.0]))

        view = glm.mat4()
        view = glm.translate(view, glm.vec3([0.0, 0.0, -3.0]))

        projection = glm.perspective(glm.radians(45.0), 800 / 600, 0.1, 100.0)
        
        model = glm.mat4()
        model = glm.rotate(model, glfw.get_time()*glm.radians(50.0), glm.vec3([0.5, 1.0, 0.0]))
        
        # shader.set_mat4('transform', glm.value_ptr(trans))
        # transformLoc = gl.glGetUniformLocation(shader.ID, "transform")
        # gl.glUniformMatrix4fv(transformLoc, 1, gl.GL_FALSE, glm.value_ptr(trans))   

        modelLoc = gl.glGetUniformLocation(shader.ID, "model")
        gl.glUniformMatrix4fv(modelLoc, 1, gl.GL_FALSE, glm.value_ptr(model))

        viewLoc = gl.glGetUniformLocation(shader.ID, "view")
        gl.glUniformMatrix4fv(viewLoc, 1, gl.GL_FALSE, glm.value_ptr(view))

        projectionLoc = gl.glGetUniformLocation(shader.ID, "projection")
        gl.glUniformMatrix4fv(projectionLoc, 1, gl.GL_FALSE, glm.value_ptr(projection))

        gl.glBindVertexArray(vao)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 36)

        glfw.poll_events()
        glfw.swap_buffers(window)

    gl.glDeleteVertexArrays(1, id(vao))
    gl.glDeleteBuffers(1, id(vbo))
    glfw.terminate()


def on_resize(window, w, h):
    gl.glViewport(0, 0, w, h)


def process_input(window):
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)


if __name__ == '__main__':
    main()