import random

from kivy import Logger


class ActionGenerator:
    @staticmethod
    def _check_collision(object_obstacles: dict, new_x: int, new_y: int, object_size: int) -> bool:
        """
        Determines whether new position of the character is occupied by any obstacle.
        :param object_obstacles: All obstacle objects on screen.
        :param new_x: X coordinate for the character to be placed on.
        :param new_y: Y coordinate for the character to be placed on.
        :param object_size: Tile size.
        :return: True for collision, False otherwise.
        """

        for i in list(object_obstacles.keys()):
            x, y = int(float(i.split("_")[1])), int(float(i.split("_")[2]))
            if abs(new_x - x) < object_size and abs(new_y - y) < object_size:
                return True
        return False

    @staticmethod
    def _get_collided_obstacles(object_obstacles: dict, character_x: int, character_y: int, object_size: int) -> list:
        """
        Returns list of the obstacles that the coordinates collide with.
        :param object_obstacles: All obstacle objects on screen.
        :param character_x: X coordinate of character.
        :param character_y: Y coordinate of character.
        :param object_size: Tile size.
        :return: List of obstacle ids.
        """

        collided_obstacles = []
        for i in list(object_obstacles.keys()):
            x, y = int(float(i.split("_")[1])), int(float(i.split("_")[2]))
            if abs(character_x - x) < object_size * 2 and abs(character_y - y) < object_size * 2:
                collided_obstacles.append(i)
        return collided_obstacles

    def move_player(self, objects: dict, touch_x: int, touch_y: int, object_size: int, map_size: tuple) -> None:
        """
        Positions visual element of the character into the new coordinates.
        :param objects: All objects on screen.
        :param touch_x: X coordinate of touch event.
        :param touch_y: Y coordinate of touch event.
        :param object_size: Tile size.
        :param map_size: Maximum coordinates on screen.
        :return:
        """

        if 0 <= touch_x < map_size[0] and 0 <= touch_y < map_size[1]:
            object_character = objects["character"]
            x, y = object_character.pos
            diff_x, diff_y = touch_x - x, touch_y - y
            if abs(diff_x) > object_size:
                x += ((diff_x > 0) - (diff_x < 0)) * object_size
            if abs(diff_y) > object_size:
                y += ((diff_y > 0) - (diff_y < 0)) * object_size

            if 0 <= x < map_size[0] and 0 <= y < map_size[1]:
                object_obstacles = {k: v for k, v in objects.items() if k != "character"}
                if not self._check_collision(object_obstacles, x, y, object_size):
                    object_character.pos = x, y

                    Logger.info(f'Action Generator: Move player to {x}, {y}')

    def hit_obstacle(self,
                     objects: dict,
                     character_x: int,
                     character_y: int,
                     object_size: int,
                     pickaxe_power: tuple) -> tuple:
        """
        Applies damage to the obstacles next to the coordinates.
        :param objects: All objects on screen.
        :param character_x: X coordinate of character.
        :param character_y: Y coordinate of character.
        :param object_size: Tile size.
        :param pickaxe_power: Range of the pickaxe power.
        :return: Lists of hit damages and visual elements.
        """

        hit_damages, removed_obstacles = [], []
        object_obstacles = {k: v for k, v in objects.items() if k != "character"}
        collided_obstacles = self._get_collided_obstacles(object_obstacles, character_x, character_y, object_size)
        if len(collided_obstacles) > 0:
            for i in collided_obstacles:
                hit_damage = random.randint(pickaxe_power[0], pickaxe_power[1])
                hit_damages.append(hit_damage)
                obstacle_health = objects[i]["health"]
                new_health = obstacle_health - hit_damage
                if new_health > 0:
                    objects[i]["health"] = new_health
                else:
                    removed_obstacles.append(objects[i]["obstacle"])
                    del objects[i]

                Logger.info(f'Action Generator: Hit {i} ({obstacle_health}) by {hit_damage}')
        return hit_damages, removed_obstacles
