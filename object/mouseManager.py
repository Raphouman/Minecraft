import numpy as np

class MouseManager:
    def __init__(self, x, y, callback=None):
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise TypeError("Mouse coordinates must be numeric values.")
        self.mouse = np.array([x, y], dtype=np.float32)
        
        self.previous_mouse = np.array([x, y], dtype=np.float32)

        self.callback = callback
        
    def execCallback(self):
        if self.callback is not None:
            try:
                self.callback(self.mouse[0], self.mouse[1], self.previous_mouse[0], self.previous_mouse[1])
            except Exception as e:
                print(f"Error executing callback: {e}")
        else:
            print("No callback set.")

    def update_mouse(self, x, y):
        self.previous_mouse = self.mouse.copy()
        self.mouse = np.array([x, y], dtype=np.float32)

    def set_callback(self, callback):
        self.callback = callback

    def get_mouse(self):
        return self.mouse

    def set_mouse(self, mouse):
        self.mouse = mouse

    def __str__(self):
        return f"MouseManager(mouse={self.mouse})"

    def __repr__(self):
        return self.__str__()