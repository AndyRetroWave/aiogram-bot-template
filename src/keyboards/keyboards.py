from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Создаем объекты инлайн-кнопок
big_button_1 = InlineKeyboardButton(
    text='Калькулятор цены',
    callback_data='big_button_1_pressed'
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
    inline_keyboard=[[big_button_1]]
)

calculator_rate = InlineKeyboardMarkup(
    inline_keyboard=[[big_button_2, big_button_3, big_button_4]]
)
upgrate_rate = InlineKeyboardMarkup(
    inline_keyboard=[[big_button_5]]
)
