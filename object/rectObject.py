from object.object import Object3D
from object.geometry import Geometry

class RectObject(Object3D):
    def __init__(self, vao, nbTriangles, shaderProgram, width=1.0, height=1.0, depth=1.0, texture=None):
        super().__init__(vao, nbTriangles, shaderProgram, geometry=Geometry(Geometry.RECTANGLE, width, height, depth), texture=texture)