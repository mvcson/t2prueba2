import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.scene_graph as sg
import grafica.lighting_shaders as ls
from grafica.assets_path import getAssetPath
import obj_reader as obj

import modelo


# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True
###########################################################
        self.theta = np.pi
        self.eye = [1, 0, 0.7]
        self.at = [0, 0, 0.7]
        self.up = [0, 0, 1]
###########################################################
# global controller as communication with the callback function
controller = Controller()



def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS and action != glfw.REPEAT:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)
    

if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Building Viewer", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Creating shader programs for textures and for colors
    textureShaderProgram = es.SimpleTextureModelViewProjectionShaderProgram()
    lightShaderProgram = ls.SimpleGouraudShaderProgram()  # Spoiler de luces

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

    # Creating shapes on GPU memory

    skyboxEmpire = modelo.create_skybox(textureShaderProgram,"newyork.jfif")
    floorEmpire = modelo.create_floor(textureShaderProgram,"asfalto.jfif")
    skyEmpire = modelo.create_sky(textureShaderProgram,"cielo.jfif")

    skyboxWilliam = modelo.create_skybox(textureShaderProgram,"chicago.jfif")
    floorWilliam = modelo.create_floor(textureShaderProgram,"asfalto.jfif")
    skyWilliam = modelo.create_sky(textureShaderProgram,"cielo.jfif")

    skyboxBurj = modelo.create_skybox(textureShaderProgram,"arabia.jfif")
    floorBurj = modelo.create_floor(textureShaderProgram,"asfalto.jfif")
    skyBurj = modelo.create_sky(textureShaderProgram,"cielo.jfif")
    shapeEmpire = obj.readOBJ(getAssetPath('empire.obj'), (0.7, 0.64, 0.61))
    gpuEmpire = es.GPUShape().initBuffers()
    lightShaderProgram.setupVAO(gpuEmpire)
    gpuEmpire.fillBuffers(shapeEmpire.vertices, shapeEmpire.indices, GL_STATIC_DRAW)

    shapeWilliam = obj.readOBJ(getAssetPath('willis.obj'), (0.7, 0.64, 0.61))
    gpuWilliam = es.GPUShape().initBuffers()
    lightShaderProgram.setupVAO(gpuWilliam)
    gpuWilliam.fillBuffers(shapeWilliam.vertices, shapeWilliam.indices, GL_STATIC_DRAW)

    shapeBurj = obj.readOBJ(getAssetPath('arabe.obj'), (0.7, 0.64, 0.61))
    gpuBurj = es.GPUShape().initBuffers()
    lightShaderProgram.setupVAO(gpuBurj)
    gpuBurj.fillBuffers(shapeBurj.vertices, shapeBurj.indices, GL_STATIC_DRAW)


    # View and projection
    projection = tr.perspective(60, float(width)/float(height), 0.1, 100)

    t0 = glfw.get_time()
    camera_theta = -3 * np.pi / 4

    # glfw will swap buffers as soon as possible
    glfw.swap_interval(0)

    t1 = glfw.get_time()
    t1 = glfw.get_time()

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        dt = t1 - t0
        t0 = t1

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        if glfw.get_key(window,glfw.KEY_1) == glfw.PRESS:
            controller.theta = 3.14
            controller.eye = [1, 0, 0.7]
            controller.at = [0, 0, 0.65]
            
        if glfw.get_key(window,glfw.KEY_2) == glfw.PRESS:
            controller.theta = 0.06
            controller.eye = [-1.08, 0, 0.7]
            controller.at = [0, 0, 0.65]
        
        if glfw.get_key(window,glfw.KEY_3 ) == glfw.PRESS:
            controller.theta = 1.66
            controller.eye = [0, -1, 0.7]
            controller.at = [0, 0, 0.65]

        if glfw.get_key(window,glfw.KEY_4 ) == glfw.PRESS:
            controller.theta = -1.66
            controller.eye = [0, 1, 0.7]
            controller.at = [0, 0, 0.65]
        #if glfw.get_key(window,glfw.KEY_5 ) == glfw.PRESS:
        #    if glfw.get_key(window,glfw.KEY_RIGHT ) == glfw.PRESS:
         #       
          #      controller.eye += (controller.at - controller.eye) * dt
           #     controller.at = [0,0,0.7]
               
                
        #if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
        #    controller.theta += 2 * dt
            
        #if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
        #    controller.theta -= 2 * dt

        if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
            controller
            controller.eye += (controller.at - controller.eye) * dt
            controller.at = [0,0,0.7]

        #if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
         #   controller.eye -= (controller.at - controller.eye) * dt
          #  controller.at -= (controller.at - controller.eye) * dt

        at_x = controller.eye[0] + np.cos(controller.theta)
        at_y = controller.eye[1] + np.sin(controller.theta)
        controller.at = np.array([at_x, at_y, controller.at[2]])

        view = tr.lookAt(controller.eye, controller.at, controller.up)

###########################################################################

        # Drawing dice (with texture, another shader program)

      
        if glfw.get_key(window, glfw.KEY_E) ==   glfw.PRESS:
            lightShaderProgram.drawCall(gpuEmpire)
            glUseProgram(textureShaderProgram.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "projection"), 1, GL_TRUE, projection)
            glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "view"), 1, GL_TRUE, view)
            sg.drawSceneGraphNode(skyboxEmpire, textureShaderProgram, "model")
            sg.drawSceneGraphNode(floorEmpire, textureShaderProgram, "model")
            sg.drawSceneGraphNode(skyEmpire, textureShaderProgram, "model")

        elif glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
            lightShaderProgram.drawCall(gpuWilliam)
            glUseProgram(textureShaderProgram.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "projection"), 1, GL_TRUE, projection)
            glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "view"), 1, GL_TRUE, view)
            sg.drawSceneGraphNode(skyboxWilliam, textureShaderProgram, "model")
            sg.drawSceneGraphNode(floorWilliam, textureShaderProgram, "model")
            sg.drawSceneGraphNode(skyWilliam, textureShaderProgram, "model")
        
        elif glfw.get_key(window, glfw.KEY_B) == glfw.PRESS:
            lightShaderProgram.drawCall(gpuBurj)
            glUseProgram(textureShaderProgram.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "projection"), 1, GL_TRUE, projection)
            glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "view"), 1, GL_TRUE, view)
            sg.drawSceneGraphNode(skyboxBurj, textureShaderProgram, "model")
            sg.drawSceneGraphNode(floorBurj, textureShaderProgram, "model")
            sg.drawSceneGraphNode(skyBurj, textureShaderProgram, "model")
        
        # Dibujamos el modelo de Suzanne con OBJ:
        # Indicamos que usamos el modelo de luz
        # Se escala, se rota y se sube, en ese orden
        suzanne_transform = tr.matmul(
            [
                # tr.translate(0.0, 0.0, 0.3),
                tr.rotationX(np.pi/2),
                tr.uniformScale(0.00003),
            ]
        )