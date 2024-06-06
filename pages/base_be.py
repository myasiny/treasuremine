from typing import Any

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager


class BaseBE:
    @staticmethod
    def load_design(name: str) -> None:
        """
        Loads page design by reading screen's frontend configuration file.
        :param name: Screen name.
        :return:
        """

        folder_name = "_page".join(name.lower().rsplit("be", 1))
        file_name = "_fe".join(name.lower().rsplit("be", 1))
        with open(f"pages/{folder_name}/{file_name}.kv", "r") as file:
            Builder.load_string(file.read())

    @staticmethod
    def stop_app():
        App.get_running_app().stop()

    @staticmethod
    def change_page(screen: ScreenManager, page: Any) -> None:
        """
        Switches current screen to the given one.
        :param screen: Kivy screen manager.
        :param page: Page object.
        :return:
        """

        try:
            screen.switch_to(page)
        except:
            screen.current = page.name
