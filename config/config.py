from dataclasses import dataclass
import logging

from dotenv import load_dotenv

from config.base import getenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from aiogram import F, types, Router, Bot



class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    BOT_TOKEN: str
    ADMIN_ID: int

settings = Settings()

bot = Bot(token=settings.BOT_TOKEN)

logger = logging.getLogger(__name__)

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
