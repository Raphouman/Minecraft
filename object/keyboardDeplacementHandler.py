

import numpy as np


class KeyboardDeplacementHandler:
    def __init__(self):
        self.deplacement_keys = {
            'FORWARD': np.array([0, 0, 1]),  # Move forward
            'BACKWARD': np.array([0, 0, -1]),  # Move backward
            'UP': np.array([0, 1, 0]),  # Move up
            'DOWN': np.array([0, -1, 0]),  # Move down
            'LEFT': np.array([-1, 0, 0]),  # Move left
            'RIGHT': np.array([1, 0, 0])   # Move right
        }
        
        # UP DOWN LEFT RIGHT
        self.deplacement_keys_pressed = {
            'FORWARD': False,  # Move forward
            'BACKWARD': False,
            'UP': False,
            'DOWN': False,
            'LEFT': False,
            'RIGHT': False
        }
        
        self.jump_key_pressed = False  # Jump key state
        self.jump_key = np.array([0, 1, 0], dtype=np.float32)  # Jump direction vector


         # Mode: True = Créatif , False = Survie. Initalise to Survival Mode.
        self.creatif = False

        self.sprinting = False  # Initial Sprinting state
        self.crouching = False  # Initial Crouching state

    def toggleMode(self):
        """Bascule entre Créatif et Survie."""
        self.creatif = not self.creatif
        print(f"[Mode] {'Créatif (vol)' if self.creatif else 'Survie (saut...)'}")

    def set_sprint(self, is_sprinting):
        self.sprinting = is_sprinting 

    def set_crouch(self, is_crouching):
        self.crouching = is_crouching
            



    def update_key_state(self, key, pressed):
        if key in self.deplacement_keys:
            self.deplacement_keys_pressed[key] = pressed
        else:
            print(f"Key {key} is not a valid movement key.")
            
    
    
    
    def get_movement_vector(self):              #a modifier ici pour le mode survie et voir acceleration saut dans player.py

        movement_vector = np.array([0, 0, 0], dtype=np.float32)
        for key, pressed in self.deplacement_keys_pressed.items():
            if not pressed :
                continue
            if not self.creatif and key in ['UP', 'DOWN']:
                # In survival mode, UP and DOWN keys are not used for movement
                continue
            if pressed:
                movement_vector += self.deplacement_keys[key]

        if not self.creatif:
            # In survival mode, we only allow horizontal movement
            movement_vector[1] = 0.0
            
        # Normalize the movement vector if its magnitude is greater than 0
        return movement_vector/np.linalg.norm(movement_vector) if np.linalg.norm(movement_vector) > 0 else movement_vector
