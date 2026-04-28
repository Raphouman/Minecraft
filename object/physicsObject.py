import numpy as np
import glfw
from object.collisionHandler import CollisionHandler

class PhysicsObject:
    def __init__(self, mass, geometry, angle=np.zeros(3, dtype=np.float32),  position=np.zeros(3, dtype=np.float32), velocity=np.zeros(3, dtype=np.float32), acceleration=np.zeros(3, dtype=np.float32)):
        # self.name = name
        self.mass = mass
        self.geometry = geometry
        self.angle = angle  # Angle should be a tuple (pitch, yaw, roll)
        self.position = position  # Position should be a tuple (x, y, z)
        self.velocity = velocity  # Velocity should be a tuple (vx, vy, vz)
        self.acceleration = acceleration
        self.force = np.array([0.0, 0.0, 0.0])
        self.is_static = False
        self.collisionHandler = CollisionHandler() 


    def applyPhysics(self, delta_time):
        if not self.is_static:
            # print(delta_time)
            # self.acceleration = self.force / self.mass
            # Update velocity based on acceleration
            self.velocity += (self.acceleration + self.collisionHandler.collisionAcceleration) * delta_time
            # print()
            # Update position based on velocity
            self.position += (self.velocity + self.collisionHandler.collisionVelocity) * delta_time

            # Reset force for the next frame
            # self.force = np.array([0.0, 0.0, 0.0])

    def getSpeedFromSpeedAndAngle(self, moveVector):
        direction = self.getUnitOrientation()
        speed = np.zeros(3, dtype=np.float32)
        speed += direction * moveVector[2]  # Avancer/reculer
        
        speed += np.array([0, 1, 0], dtype=np.float32) * moveVector[1]  # Monter/descendre
        right = np.array([
            np.sin(np.radians(self.angle[1] + 90)),
            0,
            -np.cos(np.radians(self.angle[1] + 90))
        ], dtype=np.float32)
        right /= np.linalg.norm(right)
        speed += right * moveVector[0]   # Strafe gauche/droite
        return speed
    
    def getUnitOrientation(self):
        """ Retourne l'orientation unitaire de l'objet """
        yaw = self.angle[1]
        pitch = self.angle[0]
        direction = np.array([
            np.cos(np.radians(pitch)) * np.sin(np.radians(yaw)),
            np.sin(np.radians(pitch)),
            -np.cos(np.radians(pitch)) * np.cos(np.radians(yaw))
        ], dtype=np.float32)
        return direction / np.linalg.norm(direction) if np.linalg.norm(direction) > 0 else direction
    
    def __repr__(self):
        return f"Physics of the object (mass={self.mass}, position={self.position}, velocity={self.velocity}, acceleration={self.acceleration})"