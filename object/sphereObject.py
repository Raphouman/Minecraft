from object.object import Object3D
from object.geometry import Geometry

class SphereObject(Object3D):
    def __init__(self, vao, nbTriangles, shaderProgram, radius=1.0, lo=8, la=38, texture=None):
        super().__init__(vao, nbTriangles, shaderProgram, geometry=Geometry(Geometry.SPHERE, radius), texture=texture)