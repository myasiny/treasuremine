"""
TREASURE MINE
=============

`Treasure Mine` is a single-player game with various obstacles in a mine, more challenging with each deeper level.
"""

__author__ = "M. Yasin Yildirim"
__maintainer__ = "M. Yasin Yildirim"
__email__ = "myasiny@gmail.com"
__license__ = "Apache License 2.0"
__version__ = "0.0.1"
__status__ = "Development"

import os

os.environ["KIVY_AUDIO"] = "sdl2"  # should be configured before importing Kivy

from kivy.config import Config

Config.set("graphics", "resizable", False)  # should be used before importing any other Kivy modules

from kivy.app import App
from kivy.cache import Cache
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition

from configs import settings
from enums.item_type import ItemType
from pages.game_page.game_be import GameBE
from pages.menu_page.menu_be import MenuBE
from pages.splash_page.splash_be import SplashBE


class SplashScreen(Screen):
    splash_screen = SplashBE()
    splash_screen.load_design()

    @staticmethod
    def skip(*args):
        screen.switch_to(initial_screens[1])

    def on_enter(self, *args):
        Clock.schedule_once(self.skip, 3)

        fade_animation = Animation(opacity=1, duration=1.5) + Animation(opacity=0, duration=1.5)
        fade_animation.start(self.ids.image_logo)


class MenuScreen(Screen):
    menu_screen = MenuBE()
    menu_screen.load_design()

    def on_start(self):
        self.menu_screen.change_page(screen, GameScreen(name=GameScreen.__name__))

    def on_quit(self):
        self.menu_screen.stop_app()


class GameScreen(Screen):
    game_screen = GameBE()
    game_screen.load_design()

    touch_x, touch_y = None, None

    def on_pre_enter(self, *args):
        current_level = Cache.get("game", "level", default=1)
        self.game_screen.initialize_map(self.canvas, current_level)

    def on_enter(self, **kwargs):
        is_restart = kwargs.get("is_restart", True)
        current_level = Cache.get("game", "level", default=1)
        if is_restart:
            item_pickaxe = self.ids.item_pickaxe
            self.game_screen.select_tool(item_pickaxe, None, ItemType.BASIC_PICKAXE)
        else:
            current_level += 1

        label_level = self.ids.label_level
        self.game_screen.mine_generator.draw_level(label_level, current_level)

        label_health = self.ids.label_health
        self.game_screen.mine_generator.draw_health(label_health, 100)

        Cache.append("game", "level", current_level)
        Clock.schedule_interval(self.on_danger, 1)
        Clock.schedule_interval(self.on_relocate, 0.1)

    def on_move(self, *args):
        self.game_screen.update_character_position(self, self.touch_x, self.touch_y)

    def on_danger(self, *args):
        label_health = self.ids.label_health
        self.game_screen.get_damage(self, self.canvas, label_health)

    def on_relocate(self, *args):
        self.game_screen.update_creature_position()

    def on_touch_down(self, touch):
        button_pause = self.ids.button_pause
        item_pickaxe = self.ids.item_pickaxe
        item_sword = self.ids.item_sword

        if button_pause.collide_point(*touch.pos):
            self.game_screen.select_menu(self, is_exit=False)
        elif item_pickaxe.collide_point(*touch.pos):
            self.game_screen.select_tool(item_pickaxe, item_sword, ItemType.BASIC_PICKAXE)
        elif item_sword.collide_point(*touch.pos):
            self.game_screen.select_tool(item_sword, item_pickaxe, ItemType.BASIC_SWORD)
        else:
            if not touch.is_double_tap:
                self.touch_x, self.touch_y = touch.x, touch.y

                Clock.schedule_interval(self.on_move, 0.05)
            else:
                self.game_screen.use_tool(self.canvas)

    def on_touch_move(self, touch):
        self.touch_x, self.touch_y = touch.x, touch.y

    def on_touch_up(self, touch):
        Clock.unschedule(self.on_move)

    def on_pause(self):
        Clock.unschedule(self.on_move)
        Clock.unschedule(self.on_danger)
        Clock.unschedule(self.on_relocate)

    def on_complete(self):
        self.on_pause()
        self.game_screen.select_menu(self, is_exit=True)

    def on_next(self, *args):
        self.canvas.after.clear()
        self.on_pre_enter()
        self.on_enter(is_restart=args[0] if len(args) > 0 else False)

    def on_quit(self, *args):
        self.game_screen.stop_app()


initial_screens = [
    SplashScreen(name=SplashScreen.__class__.__name__),
    MenuScreen(name=MenuScreen.__class__.__name__),
]

screen = ScreenManager(transition=FadeTransition())
screen.add_widget(initial_screens[0])

Cache.register("game", limit=1)


class TreasureMineApp(App):
    Window.title = settings.app_name
    Window.icon = settings.app_icon

    if settings.is_production:
        Window.fullscreen = "auto"
    else:
        Window.fullscreen = False

    def build(self):
        screen.current = SplashScreen.__class__.__name__
        return screen


if __name__ == "__main__":
    TreasureMineApp().run()
