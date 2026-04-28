

import numpy as np


class Geometry: # basicaly the hit box of the object
    SPHERE = 0 # geometry info : RADIUS
    CUBE = 1 # geometry info : SIDE_LENGTH
    RECTANGLE = 2 # geometry info : WIDTH, HEIGHT

    def __init__(self, shape_type, *geometry_info):
        if shape_type not in (self.SPHERE, self.CUBE, self.RECTANGLE):
            raise ValueError("Invalid shape type. Must be one of SPHERE, CUBE, or RECTANGLE.")
        self.shape_type = shape_type
        self.geometry_info = geometry_info
        
        
    def get_shape_type(self):
        return self.shape_type
    
    def get_geometry_info(self):
        return self.geometry_info
    
    def get_radius(self):
        if self.shape_type == self.SPHERE:
            return self.geometry_info[0]
        elif self.shape_type == self.CUBE:
            return np.sqrt(3) * self.geometry_info[0] / 2
        elif self.shape_type == self.RECTANGLE:
            width, height, depth = self.geometry_info
            return np.sqrt((width / 2) ** 2 + (height / 2) ** 2 + (depth / 2) ** 2)
        
    def getAABB(self):
        if self.shape_type == self.SPHERE:
            radius = self.geometry_info[0]
            a = radius/np.sqrt(3)
            # 8 points centrés sur 0
            return np.array([
                [-a, -a, -a],
                [ a, -a, -a],
                [-a,  a, -a],
                [ a,  a, -a],
                [-a, -a,  a],
                [ a, -a,  a],
                [-a,  a,  a],
                [ a,  a,  a]
            ], dtype=np.float32)
            
        elif self.shape_type == self.CUBE:
            side_length = self.geometry_info[0]
            a = side_length / 2
            # 8 points centrés sur 0
            return np.array([
                [-a, -a, -a],
                [ a, -a, -a],
                [-a,  a, -a],
                [ a,  a, -a],
                [-a, -a,  a],
                [ a, -a,  a],
                [-a,  a,  a],
                [ a,  a,  a]
            ], dtype=np.float32)
            
        elif self.shape_type == self.RECTANGLE:
            width, height, depth = self.geometry_info
            a = width / 2
            b = height / 2
            c = depth / 2
            # 8 points centrés sur 0
            return np.array([
                [-a, -b, -c],
                [ a, -b, -c],
                [-a,  b, -c],
                [ a,  b, -c],
                [-a, -b,  c],
                [ a, -b,  c],
                [-a,  b,  c],
                [ a,  b,  c]
            ], dtype=np.float32)

    def __repr__(self):
        return f"Geometry(shape_type={self.shape_type}, geometry_info={self.geometry_info})"

    @staticmethod
    def get_shape_name(shape_type):
        if shape_type == Geometry.SPHERE:
            return "Sphere"
        elif shape_type == Geometry.CUBE:
            return "Cube"
        elif shape_type == Geometry.RECTANGLE:
            return "Rectangle"
        else:
            raise ValueError("Invalid shape type.")
        
    @staticmethod
    def get_shape_type_from_name(shape_name):
        if shape_name == "Sphere":
            return Geometry.SPHERE
        elif shape_name == "Cube":
            return Geometry.CUBE
        elif shape_name == "Rectangle":
            return Geometry.RECTANGLE
        else:
            raise ValueError("Invalid shape name.")