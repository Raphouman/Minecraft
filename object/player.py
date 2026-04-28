from object.keyboardDeplacementHandler import KeyboardDeplacementHandler
from object.mouseDeplacementHandler import MouseDeplacementHandler
import numpy as np
from object.object import Object3D
import pyrr
import math

class Player(Object3D):
    def __init__(self, object3D):
        if not isinstance(object3D, Object3D):
            raise TypeError("object3D must be an instance of Object3D.")
        print("player geo", object3D.geometry)
        super().__init__(object3D.vao, object3D.nbTriangles, object3D.shaderProgram, object3D.geometry, object3D.texture)
        
        self.setAngle(object3D.physics.angle)
        self.setPosition(object3D.physics.position)
        self.setSpeed(object3D.physics.speed)
        
        self.setAcceleration(np.array([0, -9.81, 0], dtype=np.float32)*5)

        # self.position = object3D.position
        # self.angle = object3D.angle
        # self.speed = object3D.speed
        
        self.keySpeed = np.array([3, 3, 3], dtype=np.float32)   #Base speed

        self.vy_max = 20 # Maximum vertical speed (for survival mode), unit per sec
        
        self.deplacement_key_handler = KeyboardDeplacementHandler()
        self.deplacement_mouse_handler = MouseDeplacementHandler()  # Placeholder for mouse handler if needed

        self.jumpImpulse = 13  # Impulse applied when jumping in survival mode

        
        

        

    def applyPhysics(self, delta_time):

        # Determine speed vector scale
        sprint_factor = 2.0 if self.deplacement_key_handler.sprinting else 1.0
        crouch_factor = 0.5 if self.deplacement_key_handler.crouching else 1.0
        currentSpeed = self.keySpeed * sprint_factor * crouch_factor

        # camera rotation 
        self.physics.angle += self.deplacement_mouse_handler.get_rotation() / 50

        if self.deplacement_key_handler.creatif:
            # Creative mode
            # Compute movement vector in 3D
            move_vec = self.deplacement_key_handler.get_movement_vector()
            #Convert to world-space velocity and apply directly to position
            speed_vec = self.physics.getSpeedFromSpeedAndAngle(move_vec) * currentSpeed
            self.physics.position += speed_vec * delta_time

        else:
            # Survival mode: jump, walk, gravity
            # One-shot jump if on ground and tronqued vertical speed

            
            # Check if on ground
            if (self.deplacement_key_handler.deplacement_keys_pressed['UP']
                    and abs(self.physics.velocity[1]) < 0.01):
                self.physics.velocity[1] += self.jumpImpulse
                self.deplacement_key_handler.deplacement_keys_pressed['UP'] = False

            #Horizontal movement on XZ plane
            move_vec = self.deplacement_key_handler.get_movement_vector()
            horiz_speed = self.physics.getSpeedFromSpeedAndAngle(move_vec) * currentSpeed  
            self.physics.velocity[0] = horiz_speed[0]
            self.physics.velocity[2] = horiz_speed[2]


            #Tronquage vertical speed to max value AFTER TEST JUMP !!!
            if  self.physics.velocity[1] <   - self.vy_max : #vy negative value so we check if it is below the max
                self.physics.velocity[1] =   - self.vy_max   #tronquer/KP la vitesse verticale max
             

            # Apply gravity and integrate physics only for survival mode
            self.physics.applyPhysics(delta_time)

            #TODO :Possible Correction to avoid fall through the ground when CTRL (down in crea) in survival

        # Sync Object3D
        self.setPosition(self.physics.position)
        self.setAngle(self.physics.angle)



   
    