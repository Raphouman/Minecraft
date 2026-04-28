from object.object import Object3D
from object.geometry import Geometry

class CubeObject(Object3D):
    def __init__(self, vao, nbTriangles, shaderProgram, side_length=1.0, texture=None):
        super().__init__(vao, nbTriangles, shaderProgram, geometry=Geometry(Geometry.CUBE, side_length), texture=texture)