from mesh.cube import Cube
from mesh.sphere import Sphere
from mesh.plan import Plan
from mesh.rect import Rect

import OpenGL.GL as GL
from ctypes import c_float, c_void_p, sizeof

class MeshManager:
    def __init__(self, meshs=None):

        self.__existing_meshes = {"Cube":Cube, "Sphere":Sphere, "Plan":Plan, "Rectangle":Rect}

        if meshs is not None and not isinstance(meshs, dict):
            raise TypeError("meshs must be a dictionary.")
        self.meshes = meshs if meshs is not None else {}
        self.vaos = {}

    def add_meshes(self, meshes):
        if not isinstance(meshes, list):
            raise TypeError("meshes must be a list of dictionaries.")
        print(meshes)
        for mesh in meshes:
            print("test for")
            if not isinstance(mesh, dict) or 'name' not in mesh or 'params' not in mesh:
                raise ValueError("Each mesh must be a dictionary with 'name' and 'params'.")
            print('test end for')
            self.add_mesh(f"{mesh['name']}{mesh['params']}", (mesh['name'], mesh['params']))
    
    def add_mesh(self, name, mesh_data):
        self.meshes[name] = mesh_data

    def get_mesh(self, name):
        return self.meshes.get(name)

    def remove_mesh(self, name):
        if name in self.meshes:
            del self.meshes[name]
            
    def load_meshes(self):
        for mesh in self.meshes.items():
            print(mesh)
            name = mesh[1][0]
            params = mesh[1][1]
            print(name, params)
            print(self.__existing_meshes[name])
            if name in self.__existing_meshes:
                print('dans le if')
                mesh_class = self.__existing_meshes[name]
                if mesh_class:
                    # [1] Cube([1])
                    # [1, 40, 59] Sphere(*[1, 40, 59]) => Sphere(1, 40, 59)
                    
                    mesh_instance = mesh_class(*params) 
                    if name not in self.vaos:
                        self.vaos[name] = {}
                    self.vaos[name][str(params)] = {"params":MeshManager.load_to_gpu(mesh_instance.getSummits(), mesh_instance.getTriangles()), "nbTriangles": len(mesh_instance.getTriangles())}

                    print(f"Mesh '{name}' loaded with parameters {params}.")
            else:
                print(f"Mesh '{name}' not found in existing meshes.")

    def get_vao(self, name, params):
        """Retrieve the VAO for a mesh by name and parameters."""
        if name in self.vaos and str(params) in self.vaos[name]:
            return self.vaos[name][str(params)]['params'], self.vaos[name][str(params)]['nbTriangles']
        else:
            print(f"VAO for mesh '{name}' with parameters {params} not found.")
            return None
        
    @staticmethod
    def load_to_gpu(summits, triangles):
        
        """ data structur : 
        ((posx, poxy, posz),
        (normalx, normaly, normalz), 
        (colorR, colorG, colorB),
        (uvx, uvy)) in float32 type in only one vbo
        """
        
        vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vao)
        vbo = GL.glGenBuffers(1)
        
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, summits, GL.GL_STATIC_DRAW)
        
        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, (3*3+1*2)*sizeof(c_float()), None)
        
        GL.glEnableVertexAttribArray(1)
        GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, GL.GL_TRUE, (3*3+1*2)*sizeof(c_float()), c_void_p(3*sizeof(c_float())))
        
        GL.glEnableVertexAttribArray(2)
        GL.glVertexAttribPointer(2, 3, GL.GL_FLOAT, GL.GL_TRUE, (3*3+1*2)*sizeof(c_float()), c_void_p(2*3*sizeof(c_float())))
        
        GL.glEnableVertexAttribArray(3)
        GL.glVertexAttribPointer(3, 2, GL.GL_FLOAT, GL.GL_TRUE, (3*3+1*2)*sizeof(c_float()), c_void_p(3*3*sizeof(c_float())))
        
        vboi = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, vboi)
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, triangles, GL.GL_STATIC_DRAW)
        
        return vao
        
