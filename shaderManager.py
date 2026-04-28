import os
from OpenGL import GL

class ShaderManager:
    def __init__(self):
        self.shadersToLoad = []
        self.shaders = {}
    def add_shader_to_load(self, name):
        """Add a shader to the manager."""
        self.shadersToLoad.append(name)
        
    def add_shaders_to_load(self, shaders):
        """Add multiple shaders to the manager."""
        if not isinstance(shaders, list):
            raise TypeError("shaders must be a list of shader names.")
        self.shadersToLoad.extend(shaders)
        
    def get_program(self, name):
        """Retrieve a shader program by name."""
        return self.shaders.get(name)
    
    def get_shader(self, name):
        """Retrieve a shader by name."""
        return self.shaders.get(name)

    def remove_shader(self, name):
        """Remove a shader from the manager."""
        if name in self.shaders:
            del self.shaders[name]

    def list_shaders(self):
        """List all shaders managed by this instance."""
        return list(self.shaders.keys())
    
    def createAllPrograms(self):
        """Create all programs from a dictionary of shaders."""
        for i in self.shadersToLoad:
            vs_file = f'./public/shaders/{i}.vert'
            fs_file = f'./public/shaders/{i}.frag'
            program_id = ShaderManager.create_program_from_file(vs_file, fs_file)
            if program_id:
                self.shaders[i] = program_id
                print(f"Shader '{i}' created successfully.")
            else:
                print(f"Failed to create shader '{i}'.")
                
    @staticmethod
    def compile_shader(shader_content, shader_type):
        # compilation d'un shader donne selon son type ´
        shader_id = GL.glCreateShader(shader_type)
        GL.glShaderSource(shader_id, shader_content)
        GL.glCompileShader(shader_id)
        success = GL.glGetShaderiv(shader_id, GL.GL_COMPILE_STATUS)
        if not success:
            log = GL.glGetShaderInfoLog(shader_id).decode('ascii')
            print(f'{25*"-"}\nError compiling shader: \n\ {shader_content}\n{5*"-"}\n{log}\n{25*"-"}')
        return shader_id
    
    @staticmethod     
    def create_program(vertex_source, fragment_source):
        # creation d'un programme GPU ´
        vs_id = ShaderManager.compile_shader(vertex_source, GL.GL_VERTEX_SHADER)
        fs_id = ShaderManager.compile_shader(fragment_source, GL.GL_FRAGMENT_SHADER)
        if vs_id and fs_id:
            program_id = GL.glCreateProgram()
            GL.glAttachShader(program_id, vs_id)
            GL.glAttachShader(program_id, fs_id)
            GL.glLinkProgram(program_id)
            success = GL.glGetProgramiv(program_id, GL.GL_LINK_STATUS)
            if not success:
                log = GL.glGetProgramInfoLog(program_id).decode('ascii')
                print(f'{25*"-"}\nError linking program:\n{log}\n{25*"-"}')
            GL.glDeleteShader(vs_id)
            GL.glDeleteShader(fs_id)
        return program_id
    
    @staticmethod       
    def create_program_from_file(vs_file, fs_file):
        # creation d'un programme GPU ´ a partir de fichiers `
        vs_content = open(vs_file, 'r').read() if os.path.exists(vs_file)\
            else print(f'{25*"-"}\nError reading file:\n{vs_file}\n{25*"-"}')
        fs_content = open(fs_file, 'r').read() if os.path.exists(fs_file)\
            else print(f'{25*"-"}\nError reading file:\n{fs_file}\n{25*"-"}')
        return ShaderManager.create_program(vs_content, fs_content)