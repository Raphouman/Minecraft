import numpy as np

class Mesh:
    def __init__(self):
        self._points = None
        self._normals = None
        self._colors = None
        self._textures = None
        self._triangles = None
        
    def getSummits(self):
    # Retourne un tableau (nb_sommets, 11) où chaque ligne est un sommet complet
        return np.hstack((self._points, self._normals, self._colors, self._textures)).astype(np.float32)
        # return np.concatenate((self._points, self._normals, self._colors, self._textures), axis=1)
    
    def getTriangles(self):
        return self._triangles
        
    def _setPoints(self, points):
        if isinstance(points, np.ndarray):
            self._points = points
        else:
            raise TypeError("Points must be a numpy array.")
    def _setNormals(self, normals):
        if isinstance(normals, np.ndarray):
            self._normals = normals
        else:
            raise TypeError("Normals must be a numpy array.")
    def _setColors(self, colors):
        if isinstance(colors, np.ndarray):
            self._colors = colors
        else:
            raise TypeError("Colors must be a numpy array.")
    def _setTextures(self, textures):
        if isinstance(textures, np.ndarray):
            self._textures = textures
        else:
            raise TypeError("Textures must be a numpy array.")
    def _setTriangles(self, triangles):
        if isinstance(triangles, np.ndarray):
            self._triangles = triangles
        else:
            raise TypeError("Triangles must be a numpy array.")
        
    @property
    def points(self):
        return self._points
    
    @property
    def normals(self):
        return self._normals
    
    @property
    def colors(self):
        return self._colors
    
    @property
    def textures(self):
        return self._textures
    
    @property
    def triangles(self):
        return self._triangles
    
    def __str__(self):
        return f"Plan - Points: {self._points.shape}, Normals: {self._normals.shape}, Colors: {self._colors.shape}, Textures: {self._textures.shape}, Triangles: {self._triangles.shape}"
        
        
        
        
        
        