from kivy.graphics import Canvas

from pages.base_be import BaseBE
from services.graphic_service.mine_generator import MineGenerator
from services.interaction_service.action_generator import ActionGenerator


class GameBE(BaseBE):
    def __init__(self):
        self.mine_generator = MineGenerator()
        self.action_generator = ActionGenerator()

    def load_design(self) -> None:
        super().load_design(name=self.__class__.__name__)

    def initialize_map(self, canvas: Canvas) -> None:
        self.mine_generator.draw_character(canvas)
        self.mine_generator.draw_obstacles(canvas)

    def update_position(self, touch_x: int, touch_y: int) -> None:
        objects = self.mine_generator.objects
        object_size = self.mine_generator.object_size
        self.action_generator.move_player(objects, touch_x, touch_y, object_size)
