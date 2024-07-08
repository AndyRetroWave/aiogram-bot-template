import asyncio
import calendar
import textwrap
from datetime import datetime, timedelta
import random
from app.lexicon.lexicon_ru import LEXICON_RU
from app.models.course.dao import course_today, get_bank, get_phone_bank
from app.models.order.dao import add_order, order_user_id_all_2
from config.config import settings

max_length = 4096
wrapper = textwrap.TextWrapper(width=max_length, replace_whitespace=False)

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
class ShoppingСartЕextGeneration:
    """
    Этот класс реализует формирование корзины
    """
    # Создаем списки для формирования позиций в корзине

    def __init__(self):
        self.order_price_list = []  # Список цен
        self.order_shipping_cost_list = []  # Список цен доставок
        self.order_price_rub_round_list = []  # Список цен с доставкой в рублях
        self.order_url_list = []  # Список ссылок на товар
        self.order_color_list = []  # Список цвет и размеров
        self.order_id_order_list = []  # Список номеров заказа

    def set_data_to_the_list(self, order_list: list, value: int) -> None:
        """
        Устанавливает данные из списка заказов в соответствующие атрибуты класса.

        Аргументы:
        order_list (list): Список заказов, каждый элементы этого списка это объект класса базы данных

        value (int): Целочисленное значение, используемое для вычисления итоговой стоимости заказа.

        Возвращает:
        None
        """
        for order in order_list:
            # проход по всем элементам в корзине клиента и получение данных
            self.order_shipping_cost_list.append(order.shipping_cost)
            self.order_price_rub_round_list.append(
                value*order.price + order.shipping_cost)
            self.order_price_list.append(order.price)
            self.order_url_list.append(order.url)
            self.order_color_list.append(order.color)
            self.order_id_order_list.append(order.order)
            self.total_price = round(sum(self.order_price_list)*value +
                                     sum(self.order_shipping_cost_list))

    async def creating_cart_text(self, data_order,
                                 new_date_20_formatted: str,
                                 new_date_30_formatted: str,
                                 new_client: bool = False):
        """
        Формирует текст корзины для заказа.

        Аргументы:
        data_order: Объект заказа или если клиент новый передаем словарь из машинного состояния.
        new_date_20_formatted: строка, представляющий ожидаемую дату доставки заказа через 20 дней.
        new_date_30_formatted: строка, представляющий ожидаемую дату доставки заказа через 30 дней.
        new_client: Флаг, указывающий, является ли клиент новым. По умолчанию False.
        """
        bank_phone = await get_phone_bank()  # Получает нормер телефона продавца
        value = await course_today()  # Получаем курс на данный момент
        bank = await get_bank()  # Получение банка получателя
        # Формирует текс для корзины. Тут лежат данные о позициях
        order_info = '\n'.join(
            [LEXICON_RU['order_message_part2'].
             format(u, c, p, r, s, o) for u, c, p, r, s, o in
             zip(self.order_url_list, self.order_color_list,
                 self.order_price_list, self.order_price_rub_round_list,
                 self.order_shipping_cost_list, self.order_id_order_list
                 )
             ]
        )
        # Тут формируеться адреса доставки и обшая цена
        total_price_message = LEXICON_RU['order_message_part1'].format(
            self.total_price, 'Пензы')
        # Тут проверяется условие, если клиент обращаеться впервые, мы берем данные из словаря машинного состояния
        if new_client == True:
            order_message = LEXICON_RU['order_message_part3'].format(
                value, 'Пензы', data_order["addres"], data_order["username"],
                data_order["phone"], new_date_20_formatted, new_date_30_formatted
            )
        # А тут берем данные из базы данных
        else:
            order_message = LEXICON_RU['order_message_part3'].format(
                value, 'Пензы', data_order.addres, data_order.name, data_order.phone,
                new_date_20_formatted, new_date_30_formatted)
        # Формируем данные продавца
        payment_message = LEXICON_RU['order_message_part4'].format(
            self.total_price, bank_phone, bank)
        # Получение полного текста корзины
        text = total_price_message + order_info + order_message + \
            payment_message
        return text

    async def send_messange_bot_client_line(
            self, text: str, message, reply_markup, bot, state):
        """
        Отправляет сообщение клиенту с разбиением на несколько сообщений, если длина текста превышает 4096 символов.

        Аргументы:
        text (str): Текст сообщения.
        message: Объект сообщения от клиента.
        reply_markup: Клавиатура для ответа на сообщение.
        bot: Объект бота.
        state: Объект состояния машины состояний.

        Возвращает:
        None
        """
        lines = wrapper.wrap(text=text)
        if len(text) > 4096:
            line_list = []
            # удаление форматирование текста
            for line in lines:
                lines_replace = line.replace(
                    "</b>", "").replace("<b>", "").\
                    replace("</code>", "").replace("<code>", "")
                line_list.append(lines_replace)
            # отправка клиенту с ожиданием в 1 секунду
            for line in line_list:
                await bot.send_message(
                    chat_id=message.from_user.id,
                    text=line,
                    parse_mode='HTML',
                    reply_markup=reply_markup,
                    disable_web_page_preview=True
                )
                await asyncio.sleep(1)
        else:
            await bot.send_message(
                chat_id=message.from_user.id,
                text=text,
                parse_mode='HTML',
                reply_markup=reply_markup,
                disable_web_page_preview=True
            )
        await state.clear()


async def random_order_int():
    order = random.randint(settings.MIN_RANDOM_INT,
                           settings.MAX_RANDOM_INT)
    return order

# Формирование отправки сообщения для клиента


async def order_formation(
    user_id: int, value: int, client_data, bot, message, order_botton, state,
    new_client: bool = False
):
    """
    Формирует заказ для клиента и отправляет ему сообщение с информацией о заказе.

    Аргументы:
    user_id (int): Идентификатор пользователя.
    value (int): Целочисленное значение, используемое для вычисления итоговой стоимости заказа.
    client_data: Данные клиента.
    bot: Объект бота.
    message: Объект сообщения от клиента.
    order_botton: Клавиатура для ответа на сообщение.
    state: Объект состояния машины состояний.
    new_client (bool): Флаг, указывающий, является ли клиент новым. По умолчанию False.

    Возвращает:
    None
    """
    # получение данных корзины клинета
    order_all_date = await order_user_id_all_2(user_id)
    # формирования даты получения
    new_dates = await order_date_receipt()
    new_date_20_formatted, new_date_30_formatted = new_dates
    order_list = ShoppingСartЕextGeneration()
    # формирования списков для корзины
    order_list.set_data_to_the_list(
        order_list=order_all_date, value=value)
    # получение текста для корзины
    if new_client == True:
        text = await order_list.creating_cart_text(
            data_order=client_data, new_date_20_formatted=new_date_20_formatted,
            new_date_30_formatted=new_date_30_formatted, new_client=True
        )
    else:
        text = await order_list.creating_cart_text(
            data_order=client_data, new_date_20_formatted=new_date_20_formatted,
            new_date_30_formatted=new_date_30_formatted,
        )
        # проверка длины текста если оно больше 4096, то делить его на разные смс
    await order_list.send_messange_bot_client_line(
        bot=bot, message=message, reply_markup=order_botton,
        state=state, text=text
    )
