import numpy as np
from mesh.mesh import Mesh
import OpenGL.GL as GL
import pyrr
from object.physicsObject import PhysicsObject
from object.geometry import Geometry

class Object3D:
    def __init__(self, vao, nbTriangles, shaderProgram, geometry=Geometry(Geometry.SPHERE, 1.0), texture=None):
        self.vao = vao
        self.nbTriangles = nbTriangles
        self.shaderProgram = shaderProgram
        self.texture = texture
        self.geometry = geometry
        self.physics = PhysicsObject(1.0, geometry)
        self.model_matrix = pyrr.matrix44.create_identity(dtype=np.float32)

    def applyPhysics(self, delta_time):
        self.physics.applyPhysics(delta_time)

    def render(self):
        # print("Rendering Object3D with VAO:", self.vao)
        GL.glBindVertexArray(self.vao)
        # print(self.shaderProgram)
        GL.glUseProgram(self.shaderProgram)
        prog = GL.glGetIntegerv(GL.GL_CURRENT_PROGRAM)
        
        loc = GL.glGetUniformLocation(prog, "modelMatrix")
        if loc != -1:
            
            translation = pyrr.matrix44.create_from_translation(self.physics.position, dtype=np.float32)
            rotationz = pyrr.matrix44.create_from_z_rotation(np.radians(self.physics.angle[2]), dtype=np.float32)
            rotationy = pyrr.matrix44.create_from_y_rotation(np.radians(self.physics.angle[1]), dtype=np.float32)
            rotationx = pyrr.matrix44.create_from_x_rotation(np.radians(self.physics.angle[0]), dtype=np.float32)
            
            rotation = pyrr.matrix44.multiply(rotationz, rotationx)
            rotation = pyrr.matrix44.multiply(rotation, rotationy)
            
            self.rotationMatrix = rotation
            self.model_matrix = pyrr.matrix44.multiply(rotation, translation)
            GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, self.model_matrix)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture)
        GL.glDrawElements(GL.GL_TRIANGLES, self.nbTriangles*3, GL.GL_UNSIGNED_INT, None)

    def setPosition(self, position):
        if isinstance(position, np.ndarray) and position.shape == (3,):
            self.physics.position = position
        else:
            raise TypeError("Position must be a numpy array of shape (3,).")
        
    def setAngle(self, angle):
        if isinstance(angle, np.ndarray) and angle.shape == (3,):
            self.physics.angle = angle
        else:
            raise TypeError("Angle must be a numpy array of shape (3,).")
    
    def setSpeed(self, speed):
        if isinstance(speed, np.ndarray) and speed.shape == (3,):
            self.physics.speed = speed
        else:
            raise TypeError("Speed must be a numpy array of shape (3,).")
        
    def setAcceleration(self, acceleration):
        if isinstance(acceleration, np.ndarray) and acceleration.shape == (3,):
            self.physics.acceleration = acceleration
        else:
            raise TypeError("Acceleration must be a numpy array of shape (3,).")
    
    def getModelMatrix(self):
        """ Retourne la matrice de transformation du modèle en 3x3"""

        return self.model_matrix[1:4, :3]