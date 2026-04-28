class InputManager():
    def __init__(self):
        self.hold_keys = set()
        self.pressed_keys = set()
        self.released_keys = set()
        
        self.callbackPressFunctions = {}
        self.callbackReleaseFunctions = {}
    
    def addKeyPressed(self, key):
        if key not in self.pressed_keys:
            self.pressed_keys.add(key)
        else:
            print(f"Key {key} already pressed, ignoring duplicate press.")
            
    def removeKeyPressed(self, key):
        if key in self.pressed_keys:
            self.pressed_keys.remove(key)
        else:
            print(f"Key {key} not pressed, ignoring release.")
            
    def addKeyReleased(self, key):
        if key not in self.released_keys:
            self.released_keys.add(key)
        else:
            print(f"Key {key} already released, ignoring duplicate release.")
            
    def removeKeyReleased(self, key):
        if key in self.released_keys:
            self.released_keys.remove(key)
        else:
            print(f"Key {key} not released, ignoring release removal.")

    def execPressFunctions(self):
        for i in self.pressed_keys:
            if i in self.callbackPressFunctions:
                if callable(self.callbackPressFunctions[i]):
                    self.callbackPressFunctions[i]()
        self.pressed_keys.clear()

    def execReleaseFunctions(self):
        for i in self.released_keys:
            if i in self.callbackReleaseFunctions:
                if callable(self.callbackReleaseFunctions[i]):
                    self.callbackReleaseFunctions[i]()
        self.released_keys.clear()

    def execAllFunctions(self):
        self.execPressFunctions()
        self.execReleaseFunctions()

    def addPressFunction(self, key, callbackFunction):
        self.callbackPressFunctions[key] = callbackFunction

    def addReleaseFunction(self, key, callbackFunction):
        self.callbackReleaseFunctions[key] = callbackFunction
