from kivy.lang import Builder


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
