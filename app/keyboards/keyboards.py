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
    url='https://vk.com/id143809040?w=wall143809040_6977',
    callback_data='button_feedback'
)
instruction = InlineKeyboardButton(
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
course = InlineKeyboardButton(
    text='Изменить курс юаня',
    callback_data='add_course_botton'
)
course = InlineKeyboardButton(
    text='Изменить курс юаня 🇨🇳',
    callback_data='add_course_botton'
)
availability = InlineKeyboardButton(
    text='🧧Как определить наличие модели?',
    callback_data='availability_botton'
)
size = InlineKeyboardButton(
    text='📏Есть ли мой размер на данную модель?',
    callback_data='size_botton'
)
size_pick_up = InlineKeyboardButton(
    text='📐Как подобрать размер?',
    callback_data='size_pick_up_botton'
)
delivery = InlineKeyboardButton(
    text='💸Сколько будет стоить товар с доставкой?',
    callback_data='delivery_botton'
)
terms = InlineKeyboardButton(
    text='🗓Сколько доставка займёт по времени?',
    callback_data='terms_botton'
)
issue = InlineKeyboardButton(
    text='Частые вопросы❓',
    callback_data='issue_botton'
)
appendix = InlineKeyboardButton(
    text='Где установить POIZON🕶',
    callback_data='appendix_botton'
)
android_poizon_botton = InlineKeyboardButton(
    text='POIZON для Андройд',
    callback_data='android_poizon_botton'
)

# Меню админа
meny_admin = InlineKeyboardMarkup(
    inline_keyboard=[[сalculator], [skam, rate],
                    [feedback, instruction], [issue], [appendix], [bot_botton], [course]]
)
# Меню клиента
meny = InlineKeyboardMarkup(
    inline_keyboard=[[сalculator], [skam, rate],
                    [feedback, instruction], [appendix], [issue], [bot_botton]]
)
# Список кнопок с калькулятором
calculator_rate = InlineKeyboardMarkup(
    inline_keyboard=[[big_button_2], [button_down_jacket], [
        button_clothes], [button_care], [button_jewelry], [menu_booton_basic]]
)
# Калькулятор
calculator_update = InlineKeyboardMarkup(
    inline_keyboard=[[сalculator], [menu_booton_basic]]
)
# Повтор расчета
update_calculator = InlineKeyboardMarkup(
    inline_keyboard=[[update_count], [menu_booton_basic]]
)
# Частые вопросы
frequent_questions = InlineKeyboardMarkup(
    inline_keyboard=[[availability], [size], [
        size_pick_up], [terms], [menu_booton_basic]]
)
# Основное меню
menu_rare = InlineKeyboardMarkup(
    inline_keyboard=[[menu_booton_basic]]
)
# Кнопка андройд
android_poizon = InlineKeyboardMarkup(
    inline_keyboard=[[android_poizon_botton], [menu_booton]]
)
menu_one = InlineKeyboardMarkup(
    inline_keyboard=[[menu_booton]]
)
