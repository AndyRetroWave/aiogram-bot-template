import asyncio
import calendar
from datetime import date, datetime, timedelta
import random
from app.lexicon.lexicon_ru import LEXICON_RU
from app.models.course.dao import course_today, get_bank, get_phone_bank
from config.config import settings

months = {
    'January': 'января',
    'February': 'февраля',
    'March': 'марта',
    'April': 'апреля',
    'May': 'мая',
    'June': 'июня',
    'July': 'июля',
    'August': 'августа',
    'September': 'сентября',
    'October': 'октября',
    'November': 'ноября',
    'December': 'декабря'
}


# Формирование даты получение заказа
async def get_new_date(days: int) -> str:
    # Получение даты доставки
    new_date = datetime.now() + timedelta(days=days)
    # Переобразование из анг в русск месяц
    month_name_en = calendar.month_name[new_date.month]
    month_name_ru = months[month_name_en]
    if days == 30:
        return f'{new_date.day} {month_name_ru} {new_date.year} года'
    else:
        return f'{new_date.day} {month_name_ru}'


# Проход по дате для получение первый даты и 2
async def order_date_receipt():
    return [await get_new_date(days) for days in [settings.DATE_ORDER_TO,
                                                  settings.DATE_ORDER_FROM]]


# создания списков для корзыны
class ReceivingOrderLists:
    """
    Этот класс реализует формирование списков для корзины
    """

    def __init__(self):
        self.order_price_list = []
        self.order_shipping_cost_list = []
        self.order_price_rub_round_list = []
        self.order_url_list = []
        self.order_color_list = []
        self.order_shipping_cost_list = []
        self.order_id_order_list = []
    # Создаем пустые списки для формирование корзины

    def set_data_to_the_list(self, order_list: dict, value: int) -> None:
        for order in order_list:
            # проход по всем элементам в корзине клиента и получение данных
            self.order_shipping_cost_list.append(order.shipping_cost)
            self.order_price_rub_round_list.append(
                value*order.price + order.shipping_cost)
            self.order_price_list.append(order.price)
            self.order_url_list.append(order.url)
            self.order_color_list.append(order.color)
            self.order_shipping_cost_list.append(order.shipping_cost)
            self.order_id_order_list.append(order.order)
            self.total_price = round(sum(self.order_price_list)*value +
                                     sum(self.order_shipping_cost_list))

    async def creating_cart_text(self, data_order,
                                 new_date_20_formatted: str,
                                 new_date_30_formatted: str,
                                 new_client: bool = False):
        bank_phone = await get_phone_bank()
        value = await course_today()  # Получаем курс на данный момент
        bank = await get_bank()  # Получение банка получателя
        order_info = '\n'.join(
            [LEXICON_RU['order_message_part2'].
             format(u, c, p, r, s, o) for u, c, p, r, s, o in
             zip(self.order_url_list, self.order_color_list,
                 self.order_price_list, self.order_price_rub_round_list,
                 self.order_shipping_cost_list, self.order_id_order_list
                 )
             ]
        )
        total_price_message = LEXICON_RU['order_message_part1'].format(
            self.total_price, 'Пензы')
        if new_client == True:
            order_message = LEXICON_RU['order_message_part3'].format(
                value, 'Пензы', data_order["addres"], data_order["username"],
                data_order["phone"], new_date_20_formatted, new_date_30_formatted
            )
        else:
            order_message = LEXICON_RU['order_message_part3'].format(
                value, 'Пензы', data_order.addres, data_order.name, data_order.phone,
                new_date_20_formatted, new_date_30_formatted)
        payment_message = LEXICON_RU['order_message_part4'].format(
            self.total_price, bank_phone, bank)
        # Получение полного текста корзины
        text = total_price_message + order_info + order_message + \
            payment_message
        return text


async def random_order_int():
    order = random.randint(settings.MIN_RANDOM_INT,
                           settings.MAX_RANDOM_INT)
    return order
