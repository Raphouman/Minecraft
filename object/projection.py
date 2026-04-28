import pyrr
from OpenGL import GL
class Projection:
    def __init__(self):
        self.projection_matrix = pyrr.matrix44.create_perspective_projection(45.0, 1.0, 0.1, 30)

    def set_projection_matrix(self, matrix):
        if not isinstance(matrix, (list, tuple)) or len(matrix) != 16:
            raise ValueError("Projection matrix must be a list or tuple of 16 elements.")
        self.projection_matrix = matrix

    def get_projection_matrix(self):
        return self.projection_matrix
    
    def updateMatrixForAllShaders(self, shaders):
        """Update the projection matrix for all shaders."""
        for name, shader_id in shaders.items():
            GL.glUseProgram(shader_id)
            self.sendProjectionMatrixToGPU()
            
    def update_projection_matrix(self, width, height):
        if height == 0:
            height = 1
        self.projection_matrix = pyrr.matrix44.create_perspective_projection(45.0, width / height, 0.1, 30)

    def sendProjectionMatrixToGPU(self):
        prog = GL.glGetIntegerv(GL.GL_CURRENT_PROGRAM)
        loc = GL.glGetUniformLocation(prog, "projection")
        if loc != -1:
            GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, self.projection_matrix)
        else:
            print("Warning: 'projectionMatrix' uniform not found in the current shader program.")
