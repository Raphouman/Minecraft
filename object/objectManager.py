from object.camera import Camera
from object.physicsManager import PhysicsManager
from object.collisionManager import CollisionManager

class ObjectManager:
    def __init__(self):
        self.objects = []
        self.camera = None
        self.player = None
        self.physics_manager = PhysicsManager()
        self.collision_manager = CollisionManager()

    def set_camera(self, position, orientation, object3D=None, shaders=None):
        if self.camera is None:
            self.camera = Camera(position, orientation, object3D, shaders)
        else:
            self.camera.position = position
            self.camera.orientation = orientation
            self.camera.object3D = object3D
            self.camera.shaders = shaders

    def add_object(self, obj):
        self.objects.append(obj)

    def remove_object(self, obj):
        self.objects.remove(obj)

    def update(self):


        # print(self.player in self.objects)
        self.physics_manager.updateDeltaTime()
        self.physics_manager.applyPhysics([self.player])
        
        self.collision_manager.check_player_collision(self.player, [self.objects[i] for i in range(len(self.objects)) if self.objects[i] is not self.player])
        print("Collisions detected:", self.collision_manager.get_collisions())
        self.collision_manager.apply_collisions()
        
        
        print(self.player.physics.position)

        if self.camera:
            self.camera.update()

    def render(self):
        for obj in self.objects:
            # Ne dessine pas l'objet suivi par la caméra (player)
            if self.camera and obj is self.camera.object3D:
                if self.camera.mode != 0:
                    obj.render()                           #decommenter pour afficher le player, et decaler dans le if pour version finale et pas de joueur à la 1ere personne
                continue
            obj.render()
        if self.camera:
            self.camera.render()
