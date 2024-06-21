from kivy.graphics import Canvas

from enums.item_class import ItemClass
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
        self.mine_generator.initialize_objects()
        self.mine_generator.draw_character(canvas)
        self.mine_generator.draw_obstacles(canvas)
        self.mine_generator.draw_creatures(canvas)

    def update_position(self, root, touch_x: int, touch_y: int) -> None:
        objects = self.mine_generator.objects
        object_size = self.mine_generator.object_size
        map_size = self.mine_generator.map_size
        exit_coordinates = self.mine_generator.coordinates["exit"][0]
        is_exit = self.action_generator.move_player(objects, touch_x, touch_y, object_size, map_size, exit_coordinates)
        if is_exit:
            root.on_complete()

    def select_menu(self, root, is_exit: bool = False) -> None:
        if is_exit:
            self.mine_generator.draw_exit_menu(root)
        else:
            self.mine_generator.draw_popup_menu(root)

    def select_tool(self, new_item, old_item, item_type: ItemType) -> None:
        current_item = self.action_generator.active_item
        if new_item != current_item:
            self.mine_generator.draw_item_selection(new_item, old_item)
            self.action_generator.active_item = item_type
            self.action_generator.active_item_power = (item_type.low_bound, item_type.high_bound)

    def use_tool(self, canvas: Canvas) -> None:
        active_item = self.action_generator.active_item
        active_item_power = self.action_generator.active_item_power

        if active_item.value == ItemClass.PICKAXE:
            self.apply_damage(canvas, active_item_power, is_pickaxe=True)
        elif active_item.value == ItemClass.SWORD:
            self.apply_damage(canvas, active_item_power, is_pickaxe=False)

    def apply_damage(self, canvas: Canvas, tool_power: tuple, is_pickaxe: bool) -> None:
        objects = self.mine_generator.objects
        object_size = self.mine_generator.object_size
        x, y = objects["character"].pos
        hit_damages, removed_objects = self.action_generator.hit_object(
            objects, x, y, object_size, tool_power, is_obstacle=is_pickaxe
        )
        self.mine_generator.draw_hit_damages(canvas, hit_damages, x, y, is_received=False)
        self.mine_generator.remove_objects(canvas, removed_objects)
