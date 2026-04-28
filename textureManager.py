from OpenGL import GL
import PIL.Image as Image
import os

class TextureManager:
    def __init__(self):
        self.textures = {}

    def load_texture(self, name, path):
        self.textures[name] = TextureManager.load_texture_on_gpu(path)

    def load_textures(self, textures):
        """Load multiple textures from a dictionary."""
        for name, path in textures:
            self.load_texture(name, path)
            
    def get_texture(self, name):
        """Retrieve a texture by name."""
        return self.textures.get(name, None)

    def unload_texture(self, name):
        """Unload a texture by name."""
        if name in self.textures:
            del self.textures[name]
        else:
            print(f"Texture '{name}' not found.")
            
    def sendAllTexturesToGPU(self):
        """Send all loaded textures to the GPU."""
        for name, texture in self.textures.items():
            if texture is not None:
                self.sendTextureToGPU(name)
            else:
                print(f"Texture '{name}' is None and cannot be sent to GPU.")
    
    def sendTextureToGPU(self, name):
        """Send a specific texture to the GPU."""
        texture = self.get_texture(name)
        if texture is not None:
            prog = GL.glGetIntegerv(GL.GL_CURRENT_PROGRAM)
            # Recup ´ ere l'identifiant de la variable translation dans le programme courant `
            loc = GL.glGetUniformLocation(prog, "tex")
            # Verifie que la variable existe ´
            if loc == -1 :
                print("Pas de variable uniforme : texture")
            # Modifie la variable pour le programme courant
            GL.glUniform1i(loc, 0)
        else:
            print(f"Texture '{name}' not found or is None.")
            
    @staticmethod
    def getTexturePath(name):
        """Get the file path of a texture by its name."""
        # This method should return the path based on the texture name.
        # For now, it returns a placeholder path.
        return f"./public/textures/{name}.png"
    
    @staticmethod
    def load_texture_on_gpu(filename):
        if not os.path.exists(filename):
            print(f'{25*"-"}\nError reading file:\n{filename}\n{25*"-"}')
            return None

        # Charger l'image, la retourner verticalement et la convertir en RGBA
        im = Image.open(filename).transpose(Image.Transpose.FLIP_TOP_BOTTOM).convert('RGBA')
        img_data = im.tobytes()  # Convertir en bytes utilisables par OpenGL

        # Générer un ID de texture
        texture_id = GL.glGenTextures(1)

        # Sélectionner cette texture
        GL.glBindTexture(GL.GL_TEXTURE_2D, texture_id)

        # Paramétrage des filtres et des modes de répétition
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)

        # Charger les données de texture dans le GPU
        GL.glTexImage2D(
            GL.GL_TEXTURE_2D, 0, GL.GL_RGBA,
            im.width, im.height, 0,
            GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, img_data
        )

        # Générer automatiquement les mipmaps (optionnel mais recommandé)
        GL.glGenerateMipmap(GL.GL_TEXTURE_2D)

        return texture_id