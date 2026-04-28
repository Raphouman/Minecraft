import numpy as np
import glfw

class PhysicsManager:
    def __init__(self):
        self.deltaTime = 0
        self.currentTime = glfw.get_time()
        self.previousTime = glfw.get_time()

    def updateDeltaTime(self):
        self.deltaTime = self.currentTime - self.previousTime
        self.previousTime = self.currentTime
        self.currentTime = glfw.get_time()

        

    def applyPhysics(self, objects):
        """#BEFORE MAX STEP IMPLEMENTATION :
        for obj in objects:
            obj.applyPhysics(self.deltaTime)"""
        
        dt = self.deltaTime
        max_step = 0.02  # Durée maximale d'une sous-étape (20 ms)
        # nombre de sous-étapes
        steps = max(1, int(np.ceil(dt / max_step)))
        sub_dt = dt / steps

        for _ in range(steps):
            for obj in objects:
                obj.applyPhysics(sub_dt)