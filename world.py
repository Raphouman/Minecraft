import json

from textureManager import TextureManager

# permet de charger le monde 
class World:
    def __init__(self, name="Default World", description="A default world description"):
        self.name = name
        self.description = description
        self.objects = []
        self.entities = []


    
    def importWorld(self, world_data):
        """
        Import world data from a dictionary or JSON-like structure.
        """
        self.name = world_data.get('name', self.name)
        self.description = world_data.get('description', self.description)
        self.objects = world_data.get('objects', self.objects)
        self.entities = world_data.get('entities', self.entities)
        
    def getWorldDataFromFile(self, file_path):
        """
        Load world data from a file.
        """
        try:
            with open(file_path, 'r') as file:
                world_data = json.load(file)
                # world_data.get()
                return world_data
        except FileNotFoundError:
            print(f"File {file_path} not found.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file {file_path}.") 
    
    def getMeshToLoad(self):
        """
        Returns a list of unique meshes (vertices, edges, faces...) to load from the world.
        """
        def make_hashable(obj):
            if isinstance(obj, dict):
                return tuple(sorted((k, make_hashable(v)) for k, v in obj.items()))
            elif isinstance(obj, list):
                return tuple(make_hashable(x) for x in obj)
            else:
                return obj

        seen = set()
        meshes = []
        for obj in self.objects:
            if 'mesh' in obj:
                mesh_name = obj['mesh']['name']
                mesh_params = obj['mesh']['params']
                key = (mesh_name, make_hashable(mesh_params))
                if key not in seen:
                    seen.add(key)
                    meshes.append({"name": mesh_name, "params": mesh_params})
        return meshes

    def getTexturesToLoad(self):
        """
        Returns a list of textures to load from the world.
        """
        return list({(obj['texture'], TextureManager.getTexturePath(obj['texture'])) for obj in self.objects if 'texture' in obj})
    
    def getShadersToLoad(self):
        """
        Returns a list of shaders to load from the world.
        """
        return list({obj['shader'] for obj in self.objects if 'shader' in obj})
    
    def add_entity(self, entity):
        self.entities.append(entity)

    def remove_entity(self, entity):
        if entity in self.entities:
            self.entities.remove(entity)

    def get_entities(self):
        return self.entities
    
    def __str__(self):
        return f"World(name={self.name}, description={self.description})"
    
    