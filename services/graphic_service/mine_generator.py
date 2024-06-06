import random

from kivy.core.window import Window
from kivy.graphics import Canvas, Color, Ellipse


class MineGenerator:
    max_width, max_height = Window.width, Window.height
    map_size = min(max_width, max_height)
    tile_amount = 50
    object_size = map_size // tile_amount
    occupied_tiles = set()
    obstacles = []

    def create_obstacles(self) -> None:
        """
        Assigns random coordinates for obstacles to be placed on.
        :return:
        """

        while True:
            x = random.randint(0, self.map_size // self.object_size - 1) * self.object_size
            y = random.randint(0, self.map_size // self.object_size - 1) * self.object_size
            if (x, y) not in self.occupied_tiles:
                self.occupied_tiles.add((x, y))
                self.obstacles.append((x, y))

            if len(self.obstacles) == (self.tile_amount // 2):
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
            for x, y in self.obstacles:
                Ellipse(
                    pos=(x - self.object_size, y - self.object_size),
                    size=(self.object_size, self.object_size)
                )
