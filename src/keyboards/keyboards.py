from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


kb_builder = InlineKeyboardBuilder()

# Создаем объекты инлайн-кнопок
сalculator = InlineKeyboardButton(
    text='👜Калькулятор цены',
    callback_data='big_button_1_pressed'
)

skam = InlineKeyboardButton(
    text='☠Про скам',
    callback_data='button_skam'
)

rate = InlineKeyboardButton(
    text='⛩️Про курс',
    callback_data='button_rate'
)

feedback = InlineKeyboardButton(
    text='⚡Отзывы',
    callback_data='button_feedback'
)

instruction = InlineKeyboardButton(
    text='Инструкция📃',
    callback_data='instruction'
)

question = InlineKeyboardButton(
    text='Задать вопрос🚑',
    callback_data='question'
)

big_button_2 = InlineKeyboardButton(
    text='Кросовки',
    callback_data='Кросовки'
)
big_button_3 = InlineKeyboardButton(
    text='Одежда',
    callback_data='Одежда'
)
big_button_4 = InlineKeyboardButton(
    text='Уход',
    callback_data='Уход'
)
big_button_5 = InlineKeyboardButton(
    text='Повтор подсчета стоимости товара',
    callback_data='Подсчет'
)
meny = InlineKeyboardMarkup(
    inline_keyboard=[[сalculator], [skam, rate], [feedback,instruction], [question]]
)
calculator_rate = InlineKeyboardMarkup(
    inline_keyboard=[[big_button_2, big_button_3, big_button_4]]
)
upgrate_rate = InlineKeyboardMarkup(
    inline_keyboard=[[big_button_5]]
)
