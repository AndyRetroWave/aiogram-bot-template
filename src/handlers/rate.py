from aiogram import F, types, Router
from aiogram.types import Message
from src.filters.filters import *
from src.keyboards.keyboards import upgrate_rate
from src.handlers.response_rate import value


router = Router()

# Хендлер для сообщений


@router.message()
async def calculator_rate_value(message: Message):
    try:
        text = float(message.text)
        if value is not None:
            value_markup = text * (value + value * 0.2) + 1200
            round_value = round(value_markup)
            await message.answer(text=str(
            f"""Стоимость данного товара будет составлять {round_value} рублей
            """),
)
        else:
            await message.reply(text="Извините, не удалось получить данные о валюте")
    except ValueError:
        await message.reply(text="Пожалуйста, введите стоимость в Юанях.")
