from dataclasses import dataclass

from dotenv import load_dotenv

from config.base import getenv
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    BOT_TOKEN: str

settings = Settings()


@dataclass
class TelegramBotConfig:
    token: str


@dataclass
class Config:
    tg_bot: TelegramBotConfig


def load_config() -> Config:
    # Parse a `.env` file and load the variables into environment valriables
    load_dotenv()

    return Config(tg_bot=TelegramBotConfig(token=getenv("BOT_TOKEN")))

print(load_config())
