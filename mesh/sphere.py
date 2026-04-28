

import numpy as np
from mesh.mesh import Mesh

class Sphere(Mesh):
    def __init__(self, radius=0, lat_segments=16, lon_segments=32):
        super().__init__()

        self.radius = radius
        self.lat_segments = lat_segments
        self.lon_segments = lon_segments

        points, normals, colors, textures = self._generateSphere()

        triangles = self._generateFaces()
        
        self._setPoints(points)
        self._setNormals(normals)
        self._setColors(colors)
        self._setTextures(textures)
        self._setTriangles(triangles)

    def _generateFaces(self):
        triangles = []
        for lat in range(self.lat_segments):
            for lon in range(self.lon_segments):
                first = (lat * (self.lon_segments + 1)) + lon
                second = first + self.lon_segments + 1
                triangles.append((first, second, first + 1))
                triangles.append((second, second + 1, first + 1))
        return np.array(triangles, dtype=np.uint32)
    
    def _generateSphere(self):
        points = []
        normals = []
        colors = []
        textures = []
        
        # Generate points, normals, colors, and texture coordinates
        for lat in range(self.lat_segments + 1):
            theta = lat * np.pi / self.lat_segments
            for lon in range(self.lon_segments):
                phi = lon * 2 * np.pi / self.lon_segments
                x = self.radius * np.sin(theta) * np.cos(phi)
                y = self.radius * np.sin(theta) * np.sin(phi)
                z = self.radius * np.cos(theta)
                points.append((x, y, z))
                normals.append((x, y, z))
                
                u = lon / self.lon_segments
                v = lat / self.lat_segments
                textures.append((u, v))
                
                r, g, b = 1.0, .0, .0 # rouge
                colors.append((r, g, b))

        return np.array(points, dtype=np.float32), np.array(normals, dtype=np.float32), np.array(colors, dtype=np.float32), np.array(textures, dtype=np.float32)

    def __str__(self):
        pass