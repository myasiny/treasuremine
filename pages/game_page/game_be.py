from kivy.graphics import Canvas

from pages.base_be import BaseBE
from services.graphic_service.mine_generator import MineGenerator
from services.interaction_service.action_generator import ActionGenerator


class GameBE(BaseBE):
    def __init__(self):
        self.mine_generator = MineGenerator()
        self.action_generator = ActionGenerator()

    def initialize_map(self, canvas: Canvas) -> None:
        self.mine_generator.draw_right_bar(canvas)
        self.mine_generator.draw_character(canvas)
        self.mine_generator.draw_obstacles(canvas)

    def update_position(self, touch_x: int, touch_y: int) -> None:
        objects = self.mine_generator.objects
        object_size = self.mine_generator.object_size
        map_size = self.mine_generator.map_size
        self.action_generator.move_player(objects, touch_x, touch_y, object_size, map_size)

    def use_pickaxe(self, canvas: Canvas) -> None:
        objects = self.mine_generator.objects
        object_size = self.mine_generator.object_size
        x, y = objects["character"].pos
        removed_obstacles = self.action_generator.hit_obstacle(objects, x, y, object_size, (50, 100))  # TODO: pickaxe power
        self.mine_generator.remove_obstacles(canvas, removed_obstacles)
