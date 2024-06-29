import os
from dotenv import load_dotenv

from enums.environment_type import EnvironmentType

load_dotenv()

environment = os.getenv("ENV", EnvironmentType.DEVELOPMENT.value)
is_production = environment.upper() == EnvironmentType.PRODUCTION.value

app_name = "Treasure Mine"
app_icon = "static/images/game_logo.png"
