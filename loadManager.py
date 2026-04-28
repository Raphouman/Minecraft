from world import World
from textureManager import TextureManager
from meshManager import MeshManager
from shaderManager import ShaderManager
from object.objectManager import ObjectManager
from object.inputManager import InputManager
from object.mouseManager import MouseManager
from object.object import Object3D
from object.player import Player
from object.projection import Projection
import numpy as np  
import OpenGL.GL as GL
import glfw
from object.debugMenu import DebugMenu
from object.cubeObject import CubeObject
from object.rectObject import RectObject
from object.sphereObject import SphereObject
from object.geometry import Geometry

class LoadManager:
    def __init__(self, world:World, objectManager:ObjectManager, textureManager:TextureManager, meshManager:MeshManager, shaderManager:ShaderManager, inputManager:InputManager, mouseManager:MouseManager, debugmenu:DebugMenu, window):
        self.world = world
        self.objectManager = objectManager
        self.textureManager = textureManager
        self.meshManager = meshManager
        self.shaderManager = shaderManager
        self.inputManager = inputManager
        self.mouseManager = mouseManager
        self.debugmenu = debugmenu
        self.window = window
        self.meshs = self.world.getMeshToLoad()

        self.all3DObjects = {
            "Cube": CubeObject,
            "Sphere": SphereObject,
            "Rectangle": RectObject
        }
        
    def load_world(self, worldName):
        self.world.importWorld(self.world.getWorldDataFromFile(f"./worlds/{worldName}.json"))
        
        self.textureManager.load_textures(self.world.getTexturesToLoad())
        
        # print(self.world.getShadersToLoad())
        self.shaderManager.add_shaders_to_load(self.world.getShadersToLoad())
        # print(self.shaderManager.shadersToLoad)
        self.shaderManager.createAllPrograms()
        
        # GL.glUseProgram(self.shaderManager.get_program("phong")) 
        # GL.glUseProgram(self.shaderManager.get_program("shader")) 
        
        # print(self.shaderManager.shaders['shader'])
        print("mesh to load", self.world.getMeshToLoad())
        
        self.meshManager.add_meshes(self.world.getMeshToLoad())
        print(self.meshManager.meshes)
        self.meshManager.load_meshes()
        
        # Load objects from the world data
        for obj3D in self.world.entities:
            if 'type' in obj3D and obj3D['type'] in [obj['name'] for obj in self.world.objects]:
                print(f"Loading object of type: {obj3D['type']}")
                meshInfo = next((obj for obj in self.world.objects if obj['name'] == obj3D['type']), None)
                print(meshInfo)
                # print(self.meshManager.vaos)
                vao, nbTriangles = self.meshManager.get_vao(meshInfo['mesh']['name'], meshInfo['mesh']['params'])
                
                # print(vao, nbTriangles)
                if vao:
                    texture = self.textureManager.get_texture(meshInfo['texture'])
                    # print("programme :", self.shaderManager.get_program(meshInfo['shader']))
                    print(self.shaderManager.shaders)
                    shaderProgram = self.shaderManager.get_program(meshInfo['shader'])
                    print(shaderProgram)
                    
                    
                    # object3D = Object3D(vao, nbTriangles, shaderProgram, texture)
                    # objectGeometry = Geometry(Geometry.get_shape_type_from_name(meshInfo['mesh']['name']), *meshInfo['mesh']['params'])
                    # print(objectGeometry)
                    object3D = self.all3DObjects[meshInfo['mesh']['name']](vao, nbTriangles, shaderProgram, *meshInfo['mesh']['params'], texture=texture)
                    object3D.setPosition(np.array(obj3D.get('position', [0, 0, 0]), dtype=np.float32))
                    object3D.setAngle(np.array(obj3D.get('angle', [0, 0, 0]), dtype=np.float32))
                    object3D.setSpeed(np.array(obj3D.get('speed', [0, 0, 0]), dtype=np.float32))
                    if "attrib" in obj3D:
                        if obj3D["attrib"] == "Player":
                            object3D = Player(object3D)
                            self.objectManager.set_camera(position=np.array([0, 0, 0], dtype=np.float32),orientation=np.array([0, 0, 0], dtype=np.float32), object3D=object3D, shaders=self.shaderManager.shaders)
                            self.objectManager.player = object3D
                            print("player : ", self.objectManager.player.shaderProgram)
                    self.objectManager.add_object(object3D)
                else:
                    print(f"Mesh '{meshInfo['mesh']['name']}' not found.")
                    
        if self.objectManager.player is not None:
            print("Player object loaded.")
            self.loadInputs()
            self.mouseManager.set_callback(self.objectManager.player.deplacement_mouse_handler.update_mouse_position)
            self.projectionMatrix = Projection()
            height, width = glfw.get_window_size(self.window)
            # GL.glViewport(0, 0, width, height)
            # print("Window size:", height, width)
            self.projectionMatrix.update_projection_matrix(height, width)
            print("Projection matrix updated:")
            # self.projectionMatrix.update_projection_matrix(800, 800)
            self.projectionMatrix.updateMatrixForAllShaders(self.shaderManager.shaders)
            # for name, id in self.shaderManager.shaders.items():
            #     GL.glUseProgram(id)
            #     self.projectionMatrix.sendProjectionMatrixToGPU()
            
    def loadInputs(self):
        """Load input handlers for the player."""
        self.inputManager.addPressFunction(glfw.KEY_W, lambda: self.objectManager.player.deplacement_key_handler.update_key_state('FORWARD', True))
        self.inputManager.addPressFunction(glfw.KEY_S, lambda: self.objectManager.player.deplacement_key_handler.update_key_state('BACKWARD', True))
        self.inputManager.addPressFunction(glfw.KEY_A, lambda: self.objectManager.player.deplacement_key_handler.update_key_state('LEFT', True))
        self.inputManager.addPressFunction(glfw.KEY_D, lambda: self.objectManager.player.deplacement_key_handler.update_key_state('RIGHT', True))
        self.inputManager.addPressFunction(glfw.KEY_SPACE, lambda: self.objectManager.player.deplacement_key_handler.update_key_state('UP', True))  #also jump in survival mode
        self.inputManager.addPressFunction(glfw.KEY_LEFT_CONTROL, lambda: self.objectManager.player.deplacement_key_handler.update_key_state('DOWN', True))
        self.inputManager.addPressFunction(glfw.KEY_LEFT_SHIFT,lambda: self.objectManager.player.deplacement_key_handler.set_sprint(True))
        self.inputManager.addPressFunction(glfw.KEY_LEFT_ALT,lambda: self.objectManager.player.deplacement_key_handler.set_crouch(True))

        #self.inputManager.addPressFunction(glfw.KEY_C, lambda:(print("C pressed"), self.debugmenu.toggle()))
        self.inputManager.addPressFunction(glfw.KEY_M, lambda:(print("Survie/Créatif"), self.objectManager.player.deplacement_key_handler.toggleMode()))
        self.inputManager.addPressFunction(59, lambda:(print("Survie/Créatif"), self.objectManager.player.deplacement_key_handler.toggleMode()))    #M en AZERTY (sinon il faudrait appuyer sur virgule)
        self.inputManager.addPressFunction(glfw.KEY_P,lambda:(print("Changement de Camera") ,self.objectManager.camera.toggle_mode()))



        self.inputManager.addReleaseFunction(glfw.KEY_W, lambda: self.objectManager.player.deplacement_key_handler.update_key_state('FORWARD', False))
        self.inputManager.addReleaseFunction(glfw.KEY_S, lambda: self.objectManager.player.deplacement_key_handler.update_key_state('BACKWARD', False))
        self.inputManager.addReleaseFunction(glfw.KEY_A, lambda: self.objectManager.player.deplacement_key_handler.update_key_state('LEFT', False))
        self.inputManager.addReleaseFunction(glfw.KEY_D, lambda: self.objectManager.player.deplacement_key_handler.update_key_state('RIGHT', False))
        self.inputManager.addReleaseFunction(glfw.KEY_SPACE, lambda: self.objectManager.player.deplacement_key_handler.update_key_state('UP', False))
        self.inputManager.addReleaseFunction(glfw.KEY_LEFT_CONTROL, lambda: self.objectManager.player.deplacement_key_handler.update_key_state('DOWN', False))
        self.inputManager.addReleaseFunction(glfw.KEY_LEFT_SHIFT, lambda: self.objectManager.player.deplacement_key_handler.set_sprint(False))
        self.inputManager.addReleaseFunction(glfw.KEY_LEFT_ALT, lambda: self.objectManager.player.deplacement_key_handler.set_crouch(False))

        print("Input handlers loaded for player.")
        