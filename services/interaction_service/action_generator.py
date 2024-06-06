class ActionGenerator:
    def move_player(self, objects: dict, touch_x: int, touch_y: int, object_size: int, map_size: tuple) -> None:
        """
        Positions visual element of the character into the new coordinates.
        :param objects: All objects on screen.
        :param touch_x: X coordinate of touch event.
        :param touch_y: Y coordinate of touch event.
        :param object_size: Step size.
        :param map_size: Maximum coordinates on screen.
        :return:
        """

        object_character = objects["character"]
        x, y = object_character.pos
        diff_x, diff_y = touch_x - x, touch_y - y
        if abs(diff_x) > object_size:
            x += ((diff_x > 0) - (diff_x < 0)) * object_size
        if abs(diff_y) > object_size:
            y += ((diff_y > 0) - (diff_y < 0)) * object_size

        if 0 <= x < map_size[0] and 0 <= y < map_size[1]:
            object_obstacles = {k: v for k, v in objects.items() if k != "character"}
            if not self.check_collision(object_obstacles, x, y, object_size):
                object_character.pos = x, y

    @staticmethod
    def check_collision(object_obstacles: dict, new_x: int, new_y: int, object_size: int) -> bool:
        """
        Determines whether new position of the character is occupied by any obstacle.
        :param object_obstacles: All obstacle objects on screen.
        :param new_x: X coordinate for the character to be placed on.
        :param new_y: Y coordinate for the character to be placed on.
        :param object_size: Step size.
        :return: True for collision, False otherwise.
        """

        for k in list(object_obstacles.keys()):
            x, y = int(float(k.split("_")[1])), int(float(k.split("_")[2]))
            if abs(new_x - x) < object_size and abs(new_y - y) < object_size:
                return True
        return False
