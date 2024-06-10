import random

from kivy.core.window import Window
from kivy.graphics import Canvas, Color, Ellipse, Rectangle


class MineGenerator:
    max_width, max_height = Window.width, Window.height
    map_size = max_width * 0.8, max_height
    tile_amount = 50
    object_size = min(map_size) // tile_amount
    objects = {}
    coordinates = {
        "character": [],
        "obstacles": []
    }

    def generate_x_y(self) -> tuple:
        """
        Creates random coordinates.
        :return: X and y coordinates.
        """

        x = random.randint(1, self.map_size[0] // self.object_size - 1) * self.object_size
        y = random.randint(1, self.map_size[1] // self.object_size - 1) * self.object_size
        return x, y

    def check_x_y(self, x: int, y: int) -> bool:
        """
        Determines whether the coordinates are occupied.
        :param x: X coordinate.
        :param y: Y coordinate.
        :return: True if occupied, False otherwise.
        """

        occupied_tiles = []
        for i in list(self.coordinates.values()):
            occupied_tiles.extend(i)
        return (x, y) in occupied_tiles

    def draw_right_bar(self, canvas: Canvas) -> None:
        """
        Creates visual elements on screen's right side for in-game buttons.
        :param canvas: Kivy canvas.
        :return:
        """

        with canvas.before:
            Color(0.128, 0.128, 0.128, 1)
            Rectangle(
                pos=(self.map_size[0] + self.object_size, 0),
                size=(self.max_width - self.map_size[0] - self.object_size, self.max_height)
            )

    def create_character(self) -> None:
        """
        Assigns random coordinates for character to be placed on.
        :return:
        """

        while True:
            x, y = self.generate_x_y()
            if not self.check_x_y(x, y):
                self.coordinates["character"].append((x, y))
                break

    def draw_character(self, canvas: Canvas) -> None:
        """
        Creates visual element on screen for the character.
        :param canvas: Kivy canvas.
        :return:
        """

        self.create_character()

        with canvas:
            Color(1, 1, 1)
            x, y = self.coordinates["character"][0]
            object_character = Rectangle(
                pos=(x, y),
                size=(self.object_size, self.object_size)
            )
            self.objects["character"] = object_character

    def create_obstacles(self) -> None:
        """
        Assigns random coordinates for obstacles to be placed on.
        :return:
        """

        while True:
            x, y = self.generate_x_y()
            if not self.check_x_y(x, y):
                self.coordinates["obstacles"].append((x, y))

            if len(self.coordinates["obstacles"]) == (self.tile_amount // 2):
                break

    def draw_obstacles(self, canvas: Canvas) -> None:
        """
        Creates visual elements on screen for the obstacles.
        :param canvas: Kivy canvas.
        :return:
        """

        self.create_obstacles()

        with canvas:
            Color(1, 0, 0)
            for x, y in self.coordinates["obstacles"]:
                object_obstacle = Ellipse(
                    pos=(x, y),
                    size=(self.object_size, self.object_size)
                )
                self.objects[f"obstacle_{x}_{y}"] = {"obstacle": object_obstacle, "health": 100}

    @staticmethod
    def remove_obstacles(canvas: Canvas, removed_obstacles: list) -> None:
        """
        Deletes the visual elements on screen.
        :param canvas: Kivy canvas.
        :param removed_obstacles: List of visual elements.
        :return:
        """

        for i in removed_obstacles:
            canvas.remove(i)
