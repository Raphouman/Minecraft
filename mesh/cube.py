import numpy as np
from mesh.mesh import Mesh

class Cube(Mesh):
    def __init__(self, length=1):
        super().__init__()
        
        
        #on le centre en 0
        # Define the 8 vertices of the cube
        
        # face 1
        p0 = (-length/2, -length/2, -length/2)
        p1 = (length/2, -length/2, -length/2)
        p2 = (-length/2, length/2, -length/2)
        p3 = (length/2, length/2, -length/2)

        # face 2
        p4 = (-length/2, -length/2, -length/2)
        p5 = (-length/2, -length/2, length/2)
        p6 = (-length/2, length/2, -length/2)
        p7 = (-length/2, length/2, length/2)
        
        # face 3
        
        p8 = (-length/2, -length/2, -length/2)
        p9 = (-length/2, -length/2, length/2)
        p10 = (length/2, -length/2, -length/2)
        p11 = (length/2, -length/2, length/2)
        
        # face 4
        p12 = (length/2, length/2, length/2)
        p13 = (length/2, length/2, -length/2)
        p14 = (-length/2, length/2, length/2)
        p15 = (-length/2, length/2, -length/2)
        

        # face 5
        p16 = (length/2, length/2, length/2)
        p17 = (-length/2, length/2, length/2)
        p18 = (length/2, -length/2, length/2)
        p19 = (-length/2, -length/2, length/2)

        # face 6
        p20 = (length/2, length/2, length/2)
        p21 = (length/2, length/2, -length/2)
        p22 = (length/2, -length/2, length/2)
        p23 = (length/2, -length/2, -length/2)

        points = np.array([p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, p17, p18, p19, p20, p21, p22, p23], dtype=np.float32)
        normals = np.array([(0, 0, -1), (0, 0, -1), (0, 0, -1), (0, 0, -1), (0, -1, 0),(0, -1, 0), (0, -1, 0), (0, -1, 0), (-1, 0, 0), (-1, 0, 0), (-1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 1, 0), (0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1), (1, 0, 0),(1, 0, 0), (1, 0, 0), (1, 0, 0) ], dtype=np.float32)
        colors = np.array([(1, 1, 1)] * 24, dtype=np.float32)
        textures = np.array([(2/3,1/2), (1/3,1/2), (2/3,1), (1/3,1), (1/3,0), (2/3,0), (1/3,1/2), (2/3,1/2), (1/3,0), (0,0), (1/3,1/2), (0,1/2), (0,1/2), (1/3,1/2), (0,1), (1/3,1), (1,1), (2/3,1), (1,1/2), (2/3,1/2), (2/3,1/2), (1,1/2), (2/3,0), (1,0)], dtype=np.float32)
        triangles = np.array([(0, 1, 2), (1, 2, 3), (4, 5, 6), (5, 6, 7), (8, 9, 10), (9, 10, 11), (12, 13, 14), (13, 14, 15), (16, 17, 18), (17, 18, 19), (20, 21, 22), (21, 22, 23)], dtype=np.uint32)

        print("Cube created with points:", len(points))
        print("Normals:", len(normals))
        print("Colors:", len(colors))
        print("Textures:", len(textures))
        print("Triangles:", len(triangles))
        # Initialize the mesh with the defined points, normals, colors, textures, and triangles
        
        self._setPoints(points)
        self._setNormals(normals)
        self._setColors(colors)
        self._setTextures(textures)
        self._setTriangles(triangles)

    def __str__(self):
        return "Plan"