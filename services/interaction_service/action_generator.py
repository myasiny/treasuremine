import random

from kivy import Logger


class ActionGenerator:
    active_item, active_item_power = None, None

    @staticmethod
    def _check_exit(exit_coordinates: tuple, coordinates: tuple) -> bool:
        """
        Determines whether new position of the character is matched with the exit.
        :param exit_coordinates: Coordinates for the exit.
        :param coordinates: Coordinates for the character.
        :return: True for match, False otherwise.
        """

        return exit_coordinates == coordinates

    @staticmethod
    def _check_collision(all_objects: dict, new_x: int, new_y: int, object_size: int) -> bool:
        """
        Determines whether new position of the character is occupied by any object.
        :param all_objects: All objects on screen.
        :param new_x: X coordinate for the character to be placed on.
        :param new_y: Y coordinate for the character to be placed on.
        :param object_size: Tile size.
        :return: True for collision, False otherwise.
        """

        for i in list(all_objects.keys()):
            x, y = int(float(i.split("_")[1])), int(float(i.split("_")[2]))
            if abs(new_x - x) < object_size and abs(new_y - y) < object_size:
                return True
        return False

    @staticmethod
    def _get_collided_objects(all_objects: dict, character_x: int, character_y: int, object_size: int) -> list:
        """
        Returns list of the objects that the coordinates collide with.
        :param all_objects: All objects on screen.
        :param character_x: X coordinate of character.
        :param character_y: Y coordinate of character.
        :param object_size: Tile size.
        :return: List of object ids.
        """

        collided_objects = []
        for i in list(all_objects.keys()):
            x, y = int(float(i.split("_")[1])), int(float(i.split("_")[2]))
            if abs(character_x - x) < object_size * 2 and abs(character_y - y) < object_size * 2:
                collided_objects.append(i)
        return collided_objects

    def move_player(self,
                    objects: dict,
                    touch_x: int,
                    touch_y: int,
                    object_size: int,
                    map_size: tuple,
                    exit_coordinates: tuple) -> bool:
        """
        Positions visual element of the character into the new coordinates.
        :param objects: All objects on screen.
        :param touch_x: X coordinate of touch event.
        :param touch_y: Y coordinate of touch event.
        :param object_size: Tile size.
        :param map_size: Maximum coordinates on screen.
        :param exit_coordinates: Coordinates for the exit.
        :return: True for exit, False otherwise.
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
                all_objects = {k: v for k, v in objects.items() if "obstacle" in k or "creature" in k}
                if not self._check_collision(all_objects, x, y, object_size):
                    object_character.pos = x, y

                    Logger.info(f'Action Generator: Move player to {x}, {y}')

                    return self._check_exit(exit_coordinates, (x, y))
        return False

    def hit_object(self,
                   objects: dict,
                   character_x: int,
                   character_y: int,
                   object_size: int,
                   tool_power: tuple,
                   is_obstacle: bool) -> tuple:
        """
        Damages the objects next to the coordinates.
        :param objects: All objects on screen.
        :param character_x: X coordinate of character.
        :param character_y: Y coordinate of character.
        :param object_size: Tile size.
        :param tool_power: Range of the tool power.
        :param is_obstacle: True for obstacle, False for creature.
        :return: Lists of hit damages and visual elements.
        """

        hit_damages, removed_objects = [], []
        object_key = "obstacle" if is_obstacle else "creature"
        all_objects = {k: v for k, v in objects.items() if object_key in k}
        collided_objects = self._get_collided_objects(all_objects, character_x, character_y, object_size)
        if len(collided_objects) > 0:
            for i in collided_objects:
                hit_damage = random.randint(tool_power[0], tool_power[1])
                hit_damages.append(hit_damage)
                object_health = objects[i]["health"]
                new_health = object_health - hit_damage
                if new_health > 0:
                    objects[i]["health"] = new_health
                else:
                    removed_objects.append(objects[i][object_key])
                    del objects[i]

                Logger.info(f'Action Generator: Hit {i} ({object_health}) by {hit_damage}')
        return hit_damages, removed_objects
