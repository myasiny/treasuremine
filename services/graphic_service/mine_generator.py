import random

from kivy import Logger
from kivy.animation import Animation
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Canvas, Color, Ellipse, Rectangle, Line
from kivy.uix.popup import Popup


class MineGenerator:
    max_width, max_height = Window.width, Window.height
    map_size = max_width, max_height * 0.9
    tile_amount = 50
    object_size = min(map_size) // tile_amount
    objects = {}
    coordinates = {
        "character": [],
        "obstacles": []
    }

    def _generate_x_y(self) -> tuple:
        """
        Creates random coordinates.
        :return: X and y coordinates.
        """

        x = random.randint(1, self.map_size[0] // self.object_size - 1) * self.object_size
        y = random.randint(1, self.map_size[1] // self.object_size - 1) * self.object_size
        return x, y

    def _check_x_y(self, x: int, y: int) -> bool:
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

    @staticmethod
    def draw_popup_menu(root) -> None:
        """
        Creates visual element on screen for the pop-up menu.
        :param root: Kivy root.
        :return:
        """

        layout_box = BoxLayout(orientation="vertical")

        button_quit = Button(text="QUIT")
        layout_box.add_widget(button_quit)

        button_close = Button(text="CLOSE")
        layout_box.add_widget(button_close)

        menu_popup = Popup(title="POP-UP MENU", content=layout_box, size_hint=(.5, .5))
        menu_popup.open()

        button_quit.bind(on_press=root.on_quit)
        button_close.bind(on_press=menu_popup.dismiss)

        Logger.info('Mine Generator: Draw pop-up menu')

    def create_character(self) -> None:
        """
        Assigns random coordinates for character to be placed on.
        :return:
        """

        while True:
            x, y = self._generate_x_y()
            if not self._check_x_y(x, y):
                self.coordinates["character"].append((x, y))
                break

        Logger.info(f'Mine Generator: Create character at {x}, {y}')

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

        Logger.info('Mine Generator: Draw character')

    def create_obstacles(self) -> None:
        """
        Assigns random coordinates for obstacles to be placed on.
        :return:
        """

        while True:
            x, y = self._generate_x_y()
            if not self._check_x_y(x, y):
                self.coordinates["obstacles"].append((x, y))

            if len(self.coordinates["obstacles"]) == (self.tile_amount // 2):
                break

        Logger.info(f'Mine Generator: Create {len(self.coordinates["obstacles"])} obstacles')

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

        Logger.info('Mine Generator: Draw obstacles')

    def draw_hit_damages(self, canvas: Canvas, hit_damages: list, x: int, y: int, is_received: bool = True) -> None:
        """
        Creates visual elements on screen for the hit damages.
        :param canvas: Kivy canvas.
        :param hit_damages: List of hit damages.
        :param x: X coordinate of character.
        :param y: Y coordinate of character.
        :param is_received: True for received damage, False for given damage.
        :return:
        """

        with canvas:
            if is_received:
                font_color = (1, 0, 0, 0.5)
                y -= self.object_size
                next_y = y - self.object_size
            else:
                font_color = (0, 1, 0, 0.5)
                y += self.object_size
                next_y = y + self.object_size

            for i in hit_damages:
                label = Label(
                    text=str(i),
                    pos=(x, y),
                    size=(self.object_size, self.object_size),
                    color=font_color
                )
                fade_animation = Animation(y=next_y, opacity=0, duration=1)
                fade_animation.start(label)

        Logger.info('Mine Generator: Draw hit damages')

    @staticmethod
    def remove_obstacles(canvas: Canvas, removed_obstacles: list) -> None:
        """
        Deletes the visual elements of the obstacles from screen.
        :param canvas: Kivy canvas.
        :param removed_obstacles: List of visual elements.
        :return:
        """

        for i in removed_obstacles:
            canvas.remove(i)

        Logger.info(f'Mine Generator: Remove {len(removed_obstacles)} obstacles')

    @staticmethod
    def draw_item_selection(new_item, old_item) -> None:
        """
        Creates visual element on screen for the selected item.
        :param new_item: Kivy item image that is currently selected.
        :param old_item: Kivy item image that is previously selected.
        :return:
        """

        with new_item.canvas.after:
            Color(0, 1, 0, 1)
            Line(rectangle=(new_item.x, new_item.y, new_item.width, new_item.height), width=2)

        if old_item is not None:
            old_item.canvas.after.clear()

        Logger.info('Mine Generator: Draw item selection')
