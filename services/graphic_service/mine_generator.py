import math
import random
from functools import partial

from kivy import Logger
from kivy.animation import Animation
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.image import Image
from kivy.core.window import Window
from kivy.graphics import Canvas, Color, Rectangle, Line
from kivy.uix.popup import Popup
from kivy.uix.splitter import Splitter
from kivy.uix.image import Image as Pic


class MineGenerator:
    max_width, max_height = Window.width, Window.height
    map_size = max_width, max_height * 0.9
    tile_amount = 20
    object_size = min(map_size) // tile_amount
    objects, coordinates, level_multiplier = None, None, None

    def _generate_x_y(self) -> tuple:
        """
        Creates random coordinates.
        :return: X and y coordinates.
        """

        x = random.randint(1, self.map_size[0] // self.object_size - 1) * self.object_size
        y = random.randint(1, self.map_size[1] // self.object_size - 1) * self.object_size
        return int(x), int(y)

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
    def _load_image(filename: str, random_range: int = None):
        """
        Loads the image file to create visual element on screen.
        :param filename: Image file name.
        :param random_range: Range for random suffix.
        :return: Kivy image.
        """

        prefix = "static/images/"
        suffix = ".png"
        if random_range is not None:
            suffix = f"_{str(random.randint(1, random_range))}.png"

        return Image(prefix + filename + suffix)

    def initialize_objects(self, level: int):
        self.objects = {}
        self.coordinates = {
            "character": [],
            "obstacles": [],
            "creatures": [],
            "exit": []
        }
        self.level_multiplier = int(math.log(level + 1, 2))

    @staticmethod
    def draw_exit_menu(root, is_dead: bool) -> None:
        """
        Creates visual element on screen for the exit menu.
        :param root: Kivy root.
        :param is_dead: True if character is dead, False otherwise.
        :return:
        """

        root.on_pause()

        layout_box = BoxLayout(orientation="vertical")

        if not is_dead:
            text_next = "PLAY"
            text_exit = "WOW! READY FOR NEXT LEVEL?"
        else:
            text_next = "RESTART"
            text_exit = "OOPS... MAYBE NEXT TIME?"

        button_next = Button(
            text=text_next,
            background_color=(.5, .3, .1),
            background_normal="static/images/button_up.png",
            background_down="static/images/button_down.png"
        )
        layout_box.add_widget(button_next)

        splitter = Splitter(sizable_from="top", size_hint_y=.1)
        layout_box.add_widget(splitter)

        button_quit = Button(
            text="QUIT",
            background_color=(.5, .3, .1),
            background_normal="static/images/button_up.png",
            background_down="static/images/button_down.png"
        )
        layout_box.add_widget(button_quit)

        menu_exit = Popup(
            title=text_exit,
            content=layout_box,
            size_hint=(.5, .5),
            separator_color=(.5, .3, .1),
            background_color=(.5, .3, .1),
            auto_dismiss=False
        )
        menu_exit.open()

        button_next.bind(on_press=menu_exit.dismiss)
        button_next.bind(on_press=partial(root.on_next, is_dead))
        button_quit.bind(on_press=root.on_quit)

        Logger.info('Mine Generator: Draw exit menu')

    @staticmethod
    def draw_popup_menu(root) -> None:
        """
        Creates visual element on screen for the pop-up menu.
        :param root: Kivy root.
        :return:
        """

        layout_box = BoxLayout(orientation="vertical")

        button_close = Button(
            text="CONTINUE",
            background_color=(.5, .3, .1),
            background_normal="static/images/button_up.png",
            background_down="static/images/button_down.png"
        )
        layout_box.add_widget(button_close)

        splitter = Splitter(sizable_from="top", size_hint_y=.1)
        layout_box.add_widget(splitter)

        button_quit = Button(
            text="QUIT",
            background_color=(.5, .3, .1),
            background_normal="static/images/button_up.png",
            background_down="static/images/button_down.png"
        )
        layout_box.add_widget(button_quit)

        menu_popup = Popup(
            title="",
            content=layout_box,
            size_hint=(.5, .5),
            separator_color=(.5, .3, .1),
            background_color=(.5, .3, .1)
        )
        menu_popup.open()

        button_close.bind(on_press=menu_popup.dismiss)
        button_quit.bind(on_press=root.on_quit)

        Logger.info('Mine Generator: Draw pop-up menu')

    @staticmethod
    def draw_item_selection(new_item, old_item) -> None:
        """
        Creates visual element on screen for the selected item.
        :param new_item: Kivy item image that is currently selected.
        :param old_item: Kivy item image that is previously selected.
        :return:
        """

        with new_item.canvas.after:
            Color(.5, .3, .1)
            Line(rectangle=(new_item.x, new_item.y, new_item.width, new_item.height), width=2)

        if old_item is not None:
            old_item.canvas.after.clear()

        Logger.info('Mine Generator: Draw item selection')

    @staticmethod
    def draw_health(health_bar, health: int) -> None:
        """
        Creates visual element on screen for the health.
        :param health_bar: Kivy label.
        :param health: Health of character.
        :return:
        """

        if health > 50:
            font_color = "36e685"
        elif 50 >= health > 25:
            font_color = "f6d84b"
        else:
            font_color = "fa0e0e"

        health_bar.text = f"[color={font_color}]{str(max(0, health))}[/color]"

    def draw_level(self, level_bar, level: int) -> None:
        """
        Creates visual element on screen for the level.
        :param level_bar: Kivy label.
        :param level: Mine depth.
        :return:
        """

        font_colors = ["36e685", "f6d84b", "d58102", "cb650e", "be4818", "ae2a1e", "fa0e0e"]
        font_color = font_colors[min(len(font_colors) - 1, self.level_multiplier - 1)]

        level_bar.text = f"[color={font_color}]{str(level)}[/color]"

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

        with canvas.after:
            x, y = self.coordinates["character"][0]

            Color(1, 1, 1)
            image_character = self._load_image(filename="object_character")
            object_character = Rectangle(
                texture=image_character.texture,
                pos=(x, y),
                size=(self.object_size, self.object_size)
            )

            self.objects["character_main"] = {"character": object_character, "health": 100}

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

        with canvas.after:
            for i, (x, y) in enumerate(self.coordinates["obstacles"]):
                if i == 0:
                    Color(1, 1, 1)
                    image_exit = self._load_image(filename="object_exit")
                    _ = Rectangle(
                        texture=image_exit.texture,
                        pos=(x, y),
                        size=(self.object_size, self.object_size)
                    )

                    self.coordinates["exit"].append((x, y))

                Color(1, 1, 1)
                image_obstacle = self._load_image(filename="object_obstacle", random_range=3)
                object_obstacle = Rectangle(
                    texture=image_obstacle.texture,
                    pos=(x, y),
                    size=(self.object_size, self.object_size)
                )

                self.objects[f"obstacle_{x}_{y}"] = {"obstacle": object_obstacle, "health": 100 * self.level_multiplier}

        Logger.info('Mine Generator: Draw obstacles')

    def create_creatures(self) -> None:
        """
        Assigns random coordinates for creatures to be placed on.
        :return:
        """

        while True:
            x, y = self._generate_x_y()
            if not self._check_x_y(x, y):
                self.coordinates["creatures"].append((x, y))

            if len(self.coordinates["creatures"]) == (self.tile_amount // 3):
                break

        Logger.info(f'Mine Generator: Create {len(self.coordinates["creatures"])} creatures')

    def draw_creatures(self, canvas: Canvas) -> None:
        """
        Creates visual elements on screen for the creatures.
        :param canvas: Kivy canvas.
        :return:
        """

        self.create_creatures()

        with canvas.after:
            for x, y in self.coordinates["creatures"]:
                Color(1, 1, 1)
                image_creature = self._load_image(filename="object_creature", random_range=3)
                object_creature = Rectangle(
                    texture=image_creature.texture,
                    pos=(x, y),
                    size=(self.object_size, self.object_size)
                )

                self.objects[f"creature_{x}_{y}"] = {"creature": object_creature,
                                                     "health": 150 * self.level_multiplier,
                                                     "power": (5 * self.level_multiplier, 15 * self.level_multiplier)}

        Logger.info('Mine Generator: Draw creatures')

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

        with canvas.after:
            self.draw_effect(x=x, y=y, is_smoke=not is_received)

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

    def draw_effect(self, x: int, y: int, is_smoke: bool = True) -> None:
        """
        Creates visual element on screen for action effects.
        :param x: X coordinate.
        :param y: Y coordinate.
        :param is_smoke: True for rising smoke, False for flowing drop.
        :return:
        """

        if is_smoke:
            source = "static/images/pic_smoke.png"
            next_y = y + (self.object_size * 2 / 3)
            y += self.object_size / 3
        else:
            source = "static/images/pic_water.png"
            next_y = y + (self.object_size / 3)
            y += self.object_size * 2 / 3

        pic_effect = Pic(
            source=source,
            pos=(x + self.object_size / 3, y),
            size=(self.object_size / 3, self.object_size / 3)
        )
        fade_animation = Animation(y=next_y, opacity=0, duration=0.5)
        fade_animation.start(pic_effect)

    def remove_objects(self, canvas: Canvas, removed_objects: list) -> None:
        """
        Deletes the visual elements of the objects from screen.
        :param canvas: Kivy canvas.
        :param removed_objects: List of visual elements.
        :return:
        """

        for i in removed_objects:
            with canvas.after:
                self.draw_effect(x=i.pos[0], y=i.pos[1])

            canvas.after.remove(i)

        Logger.info(f'Mine Generator: Remove {len(removed_objects)} objects')
