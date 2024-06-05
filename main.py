"""
TREASURE MINE
=============

`Treasure Mine` is a game. TODO: add description
"""

__author__ = "M. Yasin Yildirim"
__maintainer__ = "M. Yasin Yildirim"
__email__ = "myasiny@gmail.com"
__license__ = "Apache License 2.0"
__version__ = "0.0.1"
__status__ = "Development"

from kivy.app import App
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition

from pages.menu_page.menu_be import MenuBE
from pages.splash_page.splash_be import SplashBE


class SplashScreen(Screen):
    splash_screen = SplashBE()
    splash_screen.load_design()

    @staticmethod
    def skip(dt):
        screen.switch_to(screens[1])

    def on_enter(self, *args):
        Clock.schedule_once(self.skip, 2)
        fade_animation = Animation(opacity=1, duration=1) + Animation(opacity=0, duration=1)
        fade_animation.start(self.ids["image_logo"])


class MenuScreen(Screen):
    menu_screen = MenuBE()
    menu_screen.load_design()

    def on_quit(self):
        self.menu_screen.on_quit()


screens = [
    SplashScreen(name=SplashScreen.__class__.__name__),
    MenuScreen(name=MenuScreen.__class__.__name__),
]

screen = ScreenManager(transition=FadeTransition())
screen.add_widget(screens[0])


class TreasureMineApp(App):
    def build(self):
        screen.current = SplashScreen.__class__.__name__
        return screen


if __name__ == "__main__":
    TreasureMineApp().run()
