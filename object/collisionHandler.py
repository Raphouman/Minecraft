import numpy as np

class CollisionHandler:
    def __init__(self):
        self.collisionVelocity = np.zeros(3, dtype=np.float32)
        self.collisionAngle = np.zeros(3, dtype=np.float32)
        self.collisionAcceleration = np.zeros(3, dtype=np.float32)

    def resetCollision(self):
        self.collisionVelocity = np.zeros(3, dtype=np.float32)
        self.collisionAngle = np.zeros(3, dtype=np.float32)
        self.collisionAcceleration = np.zeros(3, dtype=np.float32)
