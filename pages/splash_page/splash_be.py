from pages.base_be import BaseBE


class SplashBE(BaseBE):
    def load_design(self) -> None:
        super().load_design(name=self.__class__.__name__)
