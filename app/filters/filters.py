from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

def my_start_filter(message: Message) -> bool:
    return message.text == '/start'

def calculator(message: Message) -> bool:
    return message.text == 'Калькулятор цены'


def calculator_2(message: Message) -> bool:
    return message.text == 'Калькулятор'

