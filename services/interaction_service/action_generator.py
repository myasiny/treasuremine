class ActionGenerator:
    def move_player(self, objects: dict, touch_x: int, touch_y: int, object_size: int) -> None:
        object_character = objects["character"]
        x, y = object_character.pos
        diff_x, diff_y = touch_x - x, touch_y - y
        if abs(diff_x) > object_size:
            x += ((diff_x > 0) - (diff_x < 0)) * object_size
        if abs(diff_y) > object_size:
            y += ((diff_y > 0) - (diff_y < 0)) * object_size

        object_obstacles = {k: v for k, v in objects.items() if k != "character"}
        if not self.check_collision(object_obstacles, x, y, object_size):
            object_character.pos = x, y

    @staticmethod
    def check_collision(object_obstacles: dict, new_x: int, new_y: int, object_size: int) -> bool:
        for k in list(object_obstacles.keys()):
            x, y = k.split("_")[1:3]
            if abs(new_x - int(x)) < object_size and abs(new_y - int(y)) < object_size:
                return True
        return False
