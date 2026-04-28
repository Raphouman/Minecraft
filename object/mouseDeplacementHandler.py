import numpy as np

class MouseDeplacementHandler:      
    def __init__(self):
        self.mouse = np.array([0.0, 0.0], dtype=np.float32)
        self.previous_mouse = np.array([0.0, 0.0], dtype=np.float32)
    def update_mouse_position(self, x, y, previous_x=None, previous_y=None):
        # Update the mouse position
        self.previous_mouse = self.mouse.copy()
        self.mouse = np.array([x, y], dtype=np.float32)
        # print(f"Mouse moved to position: {self.mouse}")

    def handle_mouse_click(self, button):
        # Handle mouse click events
        print(f"Mouse button {button} clicked at position: {self.mouse}")

    def get_rotation(self):
        return np.array([-(self.mouse[1]-self.previous_mouse[1]), (self.mouse[0]-self.previous_mouse[0]), 0.0])