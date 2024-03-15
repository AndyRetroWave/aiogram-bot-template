from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

def my_start_filter(message: Message) -> bool:
    return message.text == '/start'


def file(message: Message) -> bool:
    return message.text == 'Файл'


def photo(message: Message) -> bool:
    return message.text == 'Фото'



