from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


kb_builder = InlineKeyboardBuilder()

# Создаем объекты инлайн-кнопок
menu_booton_basic = InlineKeyboardButton(
    text='Меню🎛',
    callback_data='menu_booton_basic'
)
bot_botton = InlineKeyboardButton(
    text='🤖Хочешь себе такого бота?',
    callback_data='bot_botton'
)
menu_booton = InlineKeyboardButton(
    text='Меню🎛',
    callback_data='menu_booton'
)
button_сalculator = InlineKeyboardButton(
    text='👜Калькулятор цены',
    callback_data='big_button_1_pressed'
)
button_update_count = InlineKeyboardButton(
    text='🔄Посчитать повторно',
    callback_data='big_button_1_pressed'
)
button_skam = InlineKeyboardButton(
    text='☠Про скам',
    callback_data='button_skam'
)
button_rate = InlineKeyboardButton(
    text='⛩️Про курс',
    callback_data='button_rate'
)
button_feedback = InlineKeyboardButton(
    text='⚡Отзывы',
    url='https://vk.com/id143809040?w=wall143809040_6977',
    callback_data='button_feedback'
)
button_instruction = InlineKeyboardButton(
    text='Инструкция📃',
    callback_data='instruction'
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
button_course = InlineKeyboardButton(
    text='Изменить курс юаня',
    callback_data='add_course_botton'
)
button_course = InlineKeyboardButton(
    text='Изменить курс юаня 🇨🇳',
    callback_data='add_course_botton'
)
button_issue = InlineKeyboardButton(
    text='Частые вопросы❓',
    callback_data='issue_botton'
)
button_appendix = InlineKeyboardButton(
    text='Где установить POIZON🕶',
    callback_data='appendix_botton'
)
button_guide = InlineKeyboardButton(
    text='Гайд по POIZON🔑',
    callback_data='button_guide'
)
button_android_poizon_botton = InlineKeyboardButton(
    text='POIZON для Андройд',
    callback_data='android_poizon_botton'
)
button_next = InlineKeyboardButton(
    text='Далee',
    callback_data='button_next'
)

# Меню админа
meny_admin = InlineKeyboardMarkup(
    inline_keyboard=[[button_сalculator], [button_skam, button_rate],
                    [button_feedback, button_instruction], [button_guide], [button_appendix],  [bot_botton], [button_course]]
)
# Меню клиента
meny = InlineKeyboardMarkup(
    inline_keyboard=[[button_сalculator], [button_skam, button_rate],
                    [button_feedback, button_instruction], [button_guide], [button_appendix], [bot_botton]]
)
# Список кнопок с калькулятором
calculator_rate = InlineKeyboardMarkup(
    inline_keyboard=[[big_button_2], [button_down_jacket], [
        button_clothes], [button_care], [button_jewelry], [menu_booton_basic]]
)
# Калькулятор
calculator_update = InlineKeyboardMarkup(
    inline_keyboard=[[button_сalculator], [menu_booton_basic]]
)
# Повтор расчета
update_calculator = InlineKeyboardMarkup(
    inline_keyboard=[[button_update_count], [menu_booton_basic]]
)
# Гайд по poizon
frequent_questions = InlineKeyboardMarkup(
    inline_keyboard= [[menu_booton_basic], [button_guide]]
)
# Основное меню
menu_rare = InlineKeyboardMarkup(
    inline_keyboard=[[menu_booton_basic]]
)
# Кнопка андройд
android_poizon = InlineKeyboardMarkup(
    inline_keyboard=[[button_android_poizon_botton], [menu_booton]]
)
# Меню с проскальзыванием
menu_one = InlineKeyboardMarkup(
    inline_keyboard=[[menu_booton]]
)
# Кнопка дальше
next = InlineKeyboardMarkup(
    inline_keyboard=[[button_next]]
)
# Кнопка далее и установить пойзон
next_and_poizon = InlineKeyboardMarkup(
    inline_keyboard=[[button_appendix], [button_next]]
)