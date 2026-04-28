import numpy as np
from object.player import Player
from pyrr import Matrix44


class CollisionManager:
    def __init__(self):
        self.collisions = []

    def add_collision(self, collision):
        self.collisions.append(collision)

    def clear_collisions(self):
        self.collisions.clear()

    def get_collisions(self):
        return self.collisions

    def has_collisions(self):
        return len(self.collisions) > 0
    
    def check_collision_spherical(self, obj1, obj2):
        # Vérifie si deux objets 3D se chevauchent en utilisant une collision sphérique
        obj1_radius = obj1.physics.geometry.get_radius()
        obj2_radius = obj2.physics.geometry.get_radius()

        distance = np.linalg.norm(obj1.physics.position - obj2.physics.position)
        return distance < (obj1_radius + obj2_radius)

    def check_collision_aabb(self, obj1, obj2):
        obj1Points = obj1.physics.geometry.getAABB()
        obj2Points = obj2.physics.geometry.getAABB()
        
        # on applique la transformation de l'objet pour obtenir les points AABB
        # obj1TransformedPoints = obj1Points @ obj1.getModelMatrix()
        # obj2TransformedPoints = obj2Points @ obj2.getModelMatrix()
        obj1TransformedPoints = obj1Points + obj1.physics.position
        obj2TransformedPoints = obj2Points + obj2.physics.position
        
        print("obj1TransformedPoints", obj1TransformedPoints)
        print("obj2TransformedPoints", obj2TransformedPoints)
        # Vérifie si les AABB se chevauchent
        # vecteurs en 3x3
        obj1Min = np.min(obj1TransformedPoints, axis=0)
        obj1Max = np.max(obj1TransformedPoints, axis=0)
        obj2Min = np.min(obj2TransformedPoints, axis=0)
        obj2Max = np.max(obj2TransformedPoints, axis=0)

        return (obj1Min[0] <= obj2Max[0] and obj1Max[0] >= obj2Min[0] and
                obj1Min[1] <= obj2Max[1] and obj1Max[1] >= obj2Min[1] and
                obj1Min[2] <= obj2Max[2] and obj1Max[2] >= obj2Min[2])

    def check_all_collisions(self, objects):
        # Vérifie les collisions entre tous les objets
        self.clear_collisions()
        for i in range(len(objects)):
            for j in range(i + 1, len(objects)):
                if self.check_collision_spherical(objects[i], objects[j]):
                    self.add_collision((objects[i], objects[j]))
        return self.get_collisions()
    
    def check_player_collision(self, player, objects):
        # Vérifie les collisions du joueur avec tous les objets
        self.clear_collisions()
        for obj in objects:
            if self.check_collision_spherical(player, obj): # pour éviter de faire des collisions compliqués
                # print(f"Collision detected between player and {obj}")
                # if self.check_collision_aabb(player, obj):
                    print(f"Collision detected between player and {obj}")
                    # Si la collision AABB est vraie, on ajoute la collision
                    self.add_collision((player, obj))
        return self.get_collisions()

    def clear_collisions(self):
        # Vide la liste des collisions
        for i, j in self.collisions:
            i.physics.collisionHandler.resetCollision()
            j.physics.collisionHandler.resetCollision()
        self.collisions.clear()
        
    def apply_collisions(self):
        self.collisions.sort(key=lambda col: CollisionManager.get_overlap_depth(col[0], col[1]), reverse=True)
        for obj1, obj2 in self.collisions:
            self.resolve_aabb_collision(obj1, obj2)
            

    def getPanelCollision(self, player, obj):
        """
        Retourne le panel de collision entre le joueur (sphère) et l'objet (AABB).
        Le joueur est une sphère, l'objet un cube aligné sur les axes.
        """
        center = player.physics.position
        print(player.physics.geometry)
        radius = player.physics.geometry.get_radius()
        min_box = obj.physics.position - obj.physics.geometry.get_radius()
        max_box = obj.physics.position + obj.physics.geometry.get_radius()

        # Trouver le point le plus proche du centre de la sphère sur l'AABB
        closest = np.maximum(min_box, np.minimum(center, max_box))
        direction = center - closest
        dist = np.linalg.norm(direction)

        if dist == 0:
            # Le centre est à l'intérieur de l'AABB, on cherche la direction minimale pour sortir
            distances = [
                (abs(center[0] - min_box[0]), np.array([-1, 0, 0]), "LEFT"),
                (abs(center[0] - max_box[0]), np.array([1, 0, 0]), "RIGHT"),
                (abs(center[1] - min_box[1]), np.array([0, -1, 0]), "BOTTOM"),
                (abs(center[1] - max_box[1]), np.array([0, 1, 0]), "TOP"),
                (abs(center[2] - min_box[2]), np.array([0, 0, -1]), "BACK"),
                (abs(center[2] - max_box[2]), np.array([0, 0, 1]), "FRONT"),
            ]
            min_dist = min(distances, key=lambda x: x[0])
            return min_dist[2], min_dist[1]
        elif dist <= radius:
            # Collision sur la face la plus proche
            normal = direction / dist
            # Trouver le nom du panel le plus aligné avec la normale
            panels = [
                (np.dot(normal, np.array([-1, 0, 0])), np.array([-1, 0, 0]), "LEFT"),
                (np.dot(normal, np.array([1, 0, 0])), np.array([1, 0, 0]), "RIGHT"),
                (np.dot(normal, np.array([0, -1, 0])), np.array([0, -1, 0]), "BOTTOM"),
                (np.dot(normal, np.array([0, 1, 0])), np.array([0, 1, 0]), "TOP"),
                (np.dot(normal, np.array([0, 0, -1])), np.array([0, 0, -1]), "BACK"),
                (np.dot(normal, np.array([0, 0, 1])), np.array([0, 0, 1]), "FRONT"),
            ]
            panel = max(panels, key=lambda x: x[0])
            return panel[2], panel[1]
        else:
            return None
        
    def resolve_aabb_collision(self, movable, static):
        """
        Résout une collision entre deux objets AABB (movable vs static).
        """
        EPSILON = 1e-2

        # Obtenir les AABB centrés autour de la position de chaque objet
        movable_aabb = movable.physics.geometry.getAABB()
        static_aabb = static.physics.geometry.getAABB()

        movable_min = np.min(movable_aabb + movable.physics.position, axis=0)
        movable_max = np.max(movable_aabb + movable.physics.position, axis=0)
        static_min = np.min(static_aabb + static.physics.position, axis=0)
        static_max = np.max(static_aabb + static.physics.position, axis=0)

        # Calcul du chevauchement sur chaque axe
        overlap_x = min(movable_max[0], static_max[0]) - max(movable_min[0], static_min[0])
        overlap_y = min(movable_max[1], static_max[1]) - max(movable_min[1], static_min[1])
        overlap_z = min(movable_max[2], static_max[2]) - max(movable_min[2], static_min[2])

        # Si un des chevauchements est négatif, pas de collision
        if overlap_x <= 0 or overlap_y <= 0 or overlap_z <= 0:
            return

        # Choisir l'axe de plus petit chevauchement pour minimiser le déplacement
        overlaps = [
            (overlap_x, np.array([1, 0, 0])),
            (overlap_y, np.array([0, 1, 0])),
            (overlap_z, np.array([0, 0, 1]))
        ]
        min_overlap, direction = min(overlaps, key=lambda x: abs(x[0]))

        # Déterminer le sens du déplacement
        center_diff = movable.physics.position - static.physics.position
        if np.dot(center_diff, direction) < 0:
            direction = -direction

        # Appliquer la correction de position
        abs_dir = np.abs(direction)
        main_axis = np.argmax(abs_dir)  # 0, 1, ou 2
        axis_vector = np.zeros(3)
        axis_vector[main_axis] = np.sign(direction[main_axis])
        correction = axis_vector * (min_overlap + EPSILON)

        movable.physics.position += correction

        # Supprimer la composante de vitesse dans cette direction
        vel = movable.physics.velocity
        normal_component = np.dot(vel, direction)
        if normal_component < 0:
            movable.physics.velocity -= direction * normal_component
            # Optionnel : "dormir" l'objet si vitesse très faible
            if np.linalg.norm(movable.physics.velocity) < 1e-3:
                movable.physics.velocity = np.zeros(3)
                
    def get_overlap_depth(player, obj):
        center = player.physics.position
        radius = player.physics.geometry.get_radius()
        min_box = obj.physics.position - obj.physics.geometry.get_radius()
        max_box = obj.physics.position + obj.physics.geometry.get_radius()
        closest = np.maximum(min_box, np.minimum(center, max_box))
        direction = center - closest
        dist = np.linalg.norm(direction)
        return radius - dist  # profondeur