from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


kb_builder = InlineKeyboardBuilder()

# Создаем объекты инлайн-кнопок
сalculator = InlineKeyboardButton(
    text='👜Калькулятор цены',
    callback_data='big_button_1_pressed'
)
update_count = InlineKeyboardButton(
    text='🔄Посчитать повторно',
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
    text='Кросовки👟',
    callback_data='button_snecers'
)
button_clothes = InlineKeyboardButton(
    text='Одежда🩳',
    callback_data='button_clothes'
)
button_down_jacket = InlineKeyboardButton(
    text='Пуховики🥼',
    callback_data='button_down_jacket'
)
button_jewelry = InlineKeyboardButton(
    text='Аксесуары💄',
    callback_data='button_jewelry'
)
button_care = InlineKeyboardButton(
    text='Украшения/духи/ковры💍',
    callback_data='button_care'
)
counting = InlineKeyboardButton(
    text='Повтор подсчета стоимости товара',
    callback_data='Подсчет'
)
course= InlineKeyboardButton(
    text='Изменить курс юаня',
    callback_data='add_course_botton')
meny_admin = InlineKeyboardMarkup(
    inline_keyboard=[[сalculator], [skam, rate],
                    [feedback, instruction], [question], [course]]
)
meny = InlineKeyboardMarkup(
    inline_keyboard=[[сalculator], [skam, rate],
                    [feedback, instruction], [question]]
)
calculator_rate = InlineKeyboardMarkup(
    inline_keyboard=[[big_button_2], [button_down_jacket], [button_clothes], [button_care], [button_jewelry], ]
)
calculator_update =InlineKeyboardMarkup(
    inline_keyboard=[[сalculator]]
)
update_calculator = InlineKeyboardMarkup(
    inline_keyboard=[[update_count]]
)
upgrate_rate = InlineKeyboardMarkup(
    inline_keyboard=[[counting]]
)

