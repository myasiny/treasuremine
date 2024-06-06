from kivy.graphics import Canvas

from pages.base_be import BaseBE
from services.graphic_service.mine_generator import MineGenerator


class GameBE(BaseBE):
    def __init__(self):
        self.mine_generator = MineGenerator()

    def load_design(self) -> None:
        super().load_design(name=self.__class__.__name__)

    def initialize_map(self, canvas: Canvas) -> None:
        self.mine_generator.draw_obstacles(canvas)
