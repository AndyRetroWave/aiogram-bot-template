from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


kb_builder = InlineKeyboardBuilder()

# Создаем объекты инлайн-кнопок
menu_booton_basic = InlineKeyboardButton(
    text='Меню🎛',
    callback_data='menu_booton_basic'
)
bot_botton = InlineKeyboardButton(
    text='🤖Нужен бот?',
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
button_orders = InlineKeyboardButton(
    text='Оформить заказ💸',
    callback_data='botton_orders'
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
    text='Кроссовки👟',
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
    text='Аксессуары💄',
    callback_data='button_jewelry'
)
button_care = InlineKeyboardButton(
    text='Украшения/духи/ковры💍',
    callback_data='button_care'
)
sneacker_button_order = InlineKeyboardButton(
    text='Кроссовки👟',
    callback_data='button_snecers_order'
)
button_clothes_order = InlineKeyboardButton(
    text='Одежда🩳',
    callback_data='button_clothe_order'
)
button_down_jacke_order = InlineKeyboardButton(
    text='Пуховики🥼',
    callback_data='button_down_jacket_order'
)
button_jewelr_order = InlineKeyboardButton(
    text='Аксессуары💄',
    callback_data='button_jewelr_order'
)
button_care_order = InlineKeyboardButton(
    text='Украшения/духи/ковры💍',
    callback_data='button_care_order'
)
button_admin = InlineKeyboardButton(
    text='Админ панель',
    callback_data='add_course_admin'
)
button_course = InlineKeyboardButton(
    text='Изменить курс юаня 🇨🇳',
    callback_data='add_course_botton'
)
button_mailing = InlineKeyboardButton(
    text='Сделать рассылку',
    callback_data='mailing_botton'
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
button_сonfirm_and_send = InlineKeyboardButton(
    text='Отправляем📌',
    callback_data='button_сonfirm_and_send'
)
button_modify = InlineKeyboardButton(
    text='Изменяем✂',
    callback_data='button_modify'
)
addres_penza_botton = InlineKeyboardButton(
    text='Пенза💖',
    callback_data='addres_penza_botton'
)
add_order_botton = InlineKeyboardButton(
    text='Добавить заказ➕',
    callback_data='add_order_botton'
)
payment_botton = InlineKeyboardButton(
    text='Подтвердить заказ✔',
    callback_data='payment_botton'
)
delete_order_botton = InlineKeyboardButton(
    text='Удалить заказ ➖',
    callback_data='delete_order_botton'
)
addres_modify_botton = InlineKeyboardButton(
    text='Изменить адрес доставки✏️',
    callback_data='addres_modify_botton'
)
cart_botton = InlineKeyboardButton(
    text='Ваша корзина🛒',
    callback_data='cart_botton'
)
order_client_botton = InlineKeyboardButton(
    text='Вашы заказы📦',
    callback_data='order_client_botton'
)
question_client_botton = InlineKeyboardButton(
    text='Есть вопрос по заказу?🚑',
    callback_data='question_client_botton'
)
# Меню админа
meny_admin = InlineKeyboardMarkup(
    inline_keyboard=[[button_сalculator], [button_orders], [cart_botton], [button_guide, button_rate],
                    [button_feedback, button_instruction], [question_client_botton], [bot_botton], [button_admin]]
)
# Меню клиента
meny = InlineKeyboardMarkup(
    inline_keyboard=[[button_сalculator], [button_orders], [cart_botton], [button_guide, button_rate],
                    [button_feedback, button_instruction], [question_client_botton], [bot_botton]]
)
meny_order = InlineKeyboardMarkup(
    inline_keyboard=[[button_сalculator], [button_orders], [cart_botton, order_client_botton], [button_guide, button_rate],
                    [button_feedback, button_instruction], [question_client_botton], [bot_botton]]
)
# Список кнопок с калькулятором
calculator_rate = InlineKeyboardMarkup(
    inline_keyboard=[[big_button_2], [button_down_jacket], [
        button_clothes], [button_care], [button_jewelry], [menu_booton_basic]]
)
# Список кнопок с заказом
order = InlineKeyboardMarkup(
    inline_keyboard=[[sneacker_button_order], [button_clothes_order], [
        button_down_jacke_order], [button_care_order], [button_jewelr_order], [menu_booton_basic]]
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
    inline_keyboard=[[menu_booton_basic], [button_guide]]
)
# Основное меню
menu_rare = InlineKeyboardMarkup(
    inline_keyboard=[[menu_booton_basic]]
)
# Кнопка андройд
android_poizon = InlineKeyboardMarkup(
    inline_keyboard=[[button_android_poizon_botton], [button_next]]
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
# Админ панель
admin = InlineKeyboardMarkup(
    inline_keyboard=[[button_course], [button_mailing], [menu_booton_basic]]
)
# Рассылка
mailing_botton = InlineKeyboardMarkup(
    inline_keyboard=[[button_сonfirm_and_send], [button_modify]]
)
# Выбор доставки
order_botton = InlineKeyboardMarkup(
    inline_keyboard=[[payment_botton], [delete_order_botton,
                                        add_order_botton], [addres_modify_botton], [menu_booton]]
)
# Отдельная кнопка заказа
order_botton_one = InlineKeyboardMarkup(
    inline_keyboard=[[button_orders]]
)
