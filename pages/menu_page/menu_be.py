from kivy.app import App

from pages.base_be import BaseBE


class MenuBE(BaseBE):
    def load_design(self) -> None:
        super().load_design(name=self.__class__.__name__)

    @staticmethod
    def on_quit():
        App.get_running_app().stop()
