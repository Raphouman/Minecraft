import pyrr
import numpy as np
import OpenGL.GL as GL
from object.object import Object3D
import math

class Camera:
    def __init__(self, position, orientation, object3D=None, shaders=None):
        self.position = position  # Position should be a tuple (x, y, z)
        self.baseOrientation = orientation  # Base orientation should be a tuple (pitch, yaw, roll)
        self.orientation = orientation  # Orientation should be a tuple (pitch, yaw, roll)
        self.object3D = object3D
        self.shaders = shaders if shaders else []
        self.mode = 0   # 0 : first person, 1 : third person, 2 : front-view

    def update(self):
        if self.object3D:
            # Update the camera position and orientation to stick to the 3D object
            self.position = self.object3D.physics.position + self.object3D.physics.geometry.get_geometry_info()[1]/2 * np.array([0, 1, 0], dtype=np.float32)  # Assuming the camera is positioned above the object

            self.orientation = self.object3D.physics.angle  # Assuming angle is a tuple (pitch, yaw, roll)
        self.boundOrientation()
        self.target = self.getUnitOrientation(self.position, self.orientation[1], self.orientation[0])
        self.target = self.object3D.physics.getUnitOrientation() + self.object3D.physics.position if self.object3D else self.target


    def boundOrientation(self):
        # Limite l'orientation de la caméra
        self.orientation[0] = max(-89, min(89, self.orientation[0]))
        
    def getUnitOrientation(self, position, yaw, pitch):     #yaw = lacet (non avec la tete), pitch = tangage (oui avec la tete)
        # Yaw et pitch en radians
        direction = np.array([
            math.cos(math.radians(pitch)) * math.sin(math.radians(yaw)),
            math.sin(math.radians(pitch)),
            -math.cos(math.radians(pitch)) * math.cos(math.radians(yaw))
        ], dtype=np.float32)
        return position + direction
    

    def toggle_mode(self):
        """Cycle camera : 0 ==> 1 ==> 2 ==> 0 ..."""
        self.mode = (self.mode + 1) % 3
        modes = ["First-person", "Third-person", "Front-view"]
        print(f"[Camera] Switched to {modes[self.mode]}")



        
    def render(self):
        # print(self.orientation)

        eye_offset_crouch = np.array([0, -1.0, 0], dtype=np.float32) if self.object3D.deplacement_key_handler.crouching else np.array([0, 0, 0], dtype=np.float32)
        pos = np.array(self.position, dtype=np.float32) + eye_offset_crouch   # Adjust camera just in front of eyes
        pitch, yaw ,  _ = self.orientation
        distance = 10.0  # Distance for third-person and front-view cameras

        if self.mode == 0:
            view = pyrr.matrix44.create_look_at(eye= pos,
                                              target= self.target + eye_offset_crouch,
                                              up=np.array([0, 1, 0], dtype=np.float32), dtype=np.float32)
            
        else : 

            target = pos 
            forward = self.getUnitOrientation(np.zeros(3, dtype = np.float32), yaw, pitch)

            if self.mode == 1:
                eye = (pos - forward * distance)  # Position the camera behind the object
                view = pyrr.matrix44.create_look_at(eye= eye,
                                                target=target,
                                                up=np.array([0, 1, 0], dtype=np.float32), dtype=np.float32)
                
            elif self.mode == 2:
                eye = (pos + forward * distance)  # Position the camera in front of the object
                view = pyrr.matrix44.create_look_at(eye= eye,
                                                target=target,
                                                up=np.array([0, 1, 0], dtype=np.float32), dtype=np.float32)
        
        
        
        
        for name, id in self.shaders.items():
            GL.glUseProgram(id)
            loc = GL.glGetUniformLocation(id, "view")
            if loc != -1:
                GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, view)
        pass



    
