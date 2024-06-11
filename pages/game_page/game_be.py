from kivy.graphics import Canvas

from enums.item_type import ItemType
from pages.base_be import BaseBE
from services.graphic_service.mine_generator import MineGenerator
from services.interaction_service.action_generator import ActionGenerator


class GameBE(BaseBE):
    def load_design(self) -> None:
        super().load_design(name=self.__class__.__name__)

    def __init__(self):
        self.mine_generator = MineGenerator()
        self.action_generator = ActionGenerator()

    def initialize_map(self, canvas: Canvas) -> None:
        self.mine_generator.draw_character(canvas)
        self.mine_generator.draw_obstacles(canvas)

    def update_position(self, touch_x: int, touch_y: int) -> None:
        objects = self.mine_generator.objects
        object_size = self.mine_generator.object_size
        map_size = self.mine_generator.map_size
        self.action_generator.move_player(objects, touch_x, touch_y, object_size, map_size)

    def select_tool(self, new_item, old_item, item_type: ItemType) -> None:
        current_item = self.action_generator.active_item
        if new_item != current_item:
            self.mine_generator.draw_item_selection(new_item, old_item)
            self.action_generator.active_item = item_type

    def use_pickaxe(self, canvas: Canvas) -> None:
        objects = self.mine_generator.objects
        object_size = self.mine_generator.object_size
        x, y = objects["character"].pos
        hit_damages, removed_obstacles = self.action_generator.hit_obstacle(objects, x, y, object_size, (50, 100))  # TODO: pickaxe power
        self.mine_generator.draw_hit_damages(canvas, hit_damages, x, y, is_received=False)
        self.mine_generator.remove_obstacles(canvas, removed_obstacles)
