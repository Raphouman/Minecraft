import numpy as np
from mesh.mesh import Mesh

class Plan(Mesh):
    def __init__(self, length=1, width=1):
        
        super().__init__()
        
        self.length = length
        self.width = width
        
        # Define the 4 vertices of the plan
        p0 = (0, 0, 0)
        p1 = (length, 0, 0)
        p2 = (length, 0, width)
        p3 = (0, 0, width)

        points = np.array([p0, p1, p2, p3], dtype=np.float32)
        normals = np.array([(0, 0, 1)] * 4, dtype=np.float32)
        colors = np.array([(1, 1, 0)] * 4, dtype=np.float32)
        textures = np.array([(0, 0), (1, 0), (1, 1), (0, 1)], dtype=np.float32)
        triangles = np.array([0, 1, 2, 0, 2, 3], dtype=np.uint32)
        
        self._setPoints(points)
        self._setNormals(normals)
        self._setColors(colors)
        self._setTextures(textures)
        self._setTriangles(triangles)

    def __str__(self):
        return f"Plan - Points: {self._points.shape}, Normals: {self._normals.shape}, Colors: {self._colors.shape}, Textures: {self._textures.shape}, Triangles: {self._triangles.shape}"