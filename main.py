from object.mouseManager import MouseManager
from object.player import Player
from object.objectManager import ObjectManager
from object.projection import Projection
from mesh.plan import Plan
from mesh.cube import Cube
from world import World
from loadManager import LoadManager
from meshManager import MeshManager
from shaderManager import ShaderManager
from mesh.sphere import Sphere
from object.object import Object3D
from object.inputManager import InputManager
from textureManager import TextureManager
import OpenGL.GL as GL
import glfw
import numpy as np
import pyrr
from ctypes import *
from object.camera import Camera
from object.debugMenu import DebugMenu

class Game(object):
    """ fenêtre GLFW avec openGL """

    def __init__(self):
        self.window = self.init_window()
        self.init_context()
        self.init_programs()

        self.world = World()
        
        self.textureManager = TextureManager()
        self.objectManager = ObjectManager()
        self.meshManager = MeshManager()
        self.shaderManager = ShaderManager()
        self.inputManager = InputManager()
        self.mouseManager = MouseManager(glfw.get_cursor_pos(self.window)[0], glfw.get_cursor_pos(self.window)[1])
        
        self.debugmenu = DebugMenu()

        self.loadManager = LoadManager(self.world, self.objectManager, self.textureManager, self.meshManager, self.shaderManager, self.inputManager, self.mouseManager, self.debugmenu, self.window)
        
        self.loadManager.load_world("world3")
        
        # monitor = glfw.get_primary_monitor()
        # mode = glfw.get_video_mode(monitor)
        # width, height = mode.size.width, mode.size.height
        # self.resize_callback(self.window, width, height)  # Initial window size

        
    def init_window(self):
        # initialisation de la librairie glfw et du context opengl associé
        glfw.init()
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        # création et parametrage de la fenêtre
        glfw.window_hint(glfw.RESIZABLE, False)
        
        monitor = glfw.get_primary_monitor()
        mode = glfw.get_video_mode(monitor)
        width, height = mode.size.width, mode.size.height
        print("Monitor size:", width, height)
        # width, height = 800, 800  # Set a fixed window size for simplicity
        self.window = glfw.create_window(width, height, 'OpenGL', monitor, None)
        # height, width = mode.size.height, mode.size.width
        

        # glfw.set_window_monitor(self.window, None, 0, 0, height, width, 60)
        glfw.set_cursor_pos_callback(self.window, self.mouse_callback)
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)
        # parametrage de la fonction de gestion des évènements
        glfw.set_key_callback(self.window, self.key_callback)
        glfw.set_window_size_callback(self.window, self.resize_callback)
        return self.window

    def init_context(self): 
        # activation du context OpenGL pour la fenêtre
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        # activation de la gestion de la profondeur
        GL.glEnable(GL.GL_DEPTH_TEST)

    def init_programs(self):
        # program = ShaderManager.create_program_from_file("./public/shaders/shader.vert", "./public/shaders/shader.frag")
        pass
    def init_data(self):
        pass


    def run(self):
        # boucle d'affichage        
        
        while not glfw.window_should_close(self.window):
            # choix de la couleur de fond
            GL.glClearColor(135/255, 206/255, 235/255, 1)
            # nettoyage de la fenêtre : fond et profondeur
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
            
            self.inputs()
            self.update()
            self.render()
            # print("Camera orientation:", self.objectManager.camera.orientation, "Camera position:", self.objectManager.camera.position)
            # print("Player orientation:", self.player.angle)
   
            self.debugmenu.get_player_pos(self.objectManager.camera)
            self.debugmenu.calculate_fps()
            self.debugmenu.render(800, 800)
            # changement de buffer d'affichage pour éviter un effet de scintillement
            glfw.swap_buffers(self.window)
            # gestion des évènements
            glfw.poll_events()           
    
    def inputs(self):
        self.inputManager.execAllFunctions()
        self.mouseManager.execCallback()


    def update(self):
        self.objectManager.update()
        
    def render(self):
        self.objectManager.render()
        
        

    def key_callback(self, win, key, scancode, action, mods):
        # sortie du programme si appui sur la touche 'echap'
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(win, glfw.TRUE)
        ## for input manager
        if action == glfw.PRESS:
            print(f"Key pressed: {key}")
            self.inputManager.addKeyPressed(key)
           
        elif action == glfw.RELEASE:
            #print(f"Key released: {key}")
            self.inputManager.addKeyReleased(key)
            
    def mouse_callback(self, win, xpos, ypos):
        self.mouseManager.update_mouse(xpos, ypos)
        
    def resize_callback(self, win, width, height):
        print("Window resized to:", width, height)
        # mise à jour de la taille de la fenêtre
        GL.glViewport(0, 0, width, height)
        self.loadManager.projectionMatrix.update_projection_matrix(width, height)
        self.loadManager.projectionMatrix.updateMatrixForAllShaders(self.loadManager.shaderManager.shaders)
        
        # print("Window resized to:", width, height)
        # mise à jour de la matrice de projection
        # for name, id in self.shaderManager.shaders.items():
        #     GL.glUseProgram(id)
        #     self.projectionMatrix.sendProjectionMatrixToGPU()

def main():
    g = Game()
    g.run()
    glfw.terminate()


if __name__ == '__main__':
    main()