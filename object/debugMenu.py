from object.camera import Camera
from OpenGL.GL import *
from OpenGL.GLUT import *
import glfw
from OpenGL.GLUT import glutInit
glutInit()


def draw_text(x, y, text):
    glWindowPos2f(x, y)
    for c in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

class DebugMenu:
    def __init__(self):
        self.visible = False
        self.player_pos = (0, 0, 0)
        self.last_time = glfw.get_time()
        self.last_fps_update_time = glfw.get_time()
        self.displayed_fps = 0
        self.fps = 0

    def calculate_fps(self):
        #Gestion du Menu Debug
        current_time = glfw.get_time()
        delta_time = current_time - self.last_time
        self.last_time = current_time

        if delta_time > 0:
            fps = 1/delta_time
        else:
            fps = 0

        #Mise à jour des fps toutes les 0.5s
        if current_time - self.last_fps_update_time >= 0.09:
            self.displayed_fps = fps
            self.last_fps_update_time = current_time 
        self.fps = self.displayed_fps
    def toggle(self):
        self.visible = not self.visible
        # print(f"Debug menu visible: {self.visible}")


    def get_player_pos(self, camera):
        self.player_pos = camera.position


    def render (self, window_width, window_height):
        if not self.visible:
            return
        # print("Render debug menu")

# Basculer temporairement en 2D (projection en pixels)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, window_width, 0, window_height, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glColor3f(1.0, 1.0, 1.0)  # Texte blanc

        x = window_width - 780
        y = window_height - 20

        draw_text(x, y, f"Debug Menu")
        y -= 20
        draw_text(x, y, f"Position du joueur: X={self.player_pos[0]:.2f} Y={self.player_pos[1]:.2f} Z={self.player_pos[2]:.2f}")
        y -= 20
        draw_text(x, y, f"FPS: {self.fps:.2f}")
        # Restaurer la projection normale
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)


        # print("Debug Menu")
        # print(f"Position du joueur: X = {self.player_pos[0]}",
        #       f"Y = {self.player_pos[1]}",
        #       f"Z = {self.player_pos[2]}")
        # print(f"FPS: {self.fps}")