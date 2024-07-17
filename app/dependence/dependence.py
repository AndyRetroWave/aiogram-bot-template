import asyncio
import calendar
import textwrap
from datetime import datetime, timedelta
import random

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from aiogram import Bot
from app.lexicon.lexicon_ru import LEXICON_RU
from app.models.course.dao import course_today, get_bank, get_phone_bank
from app.models.order.dao import add_order_save, order_user_id_all
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
                                 new_client: bool = False) -> str:
        """
        Формирует текст корзины для заказа.

        Аргументы:
        data_order: Объект заказа или если клиент новый передаем словарь из машинного состояния.
        new_date_20_formatted: строка, представляющий ожидаемую дату доставки заказа через 20 дней.
        new_date_30_formatted: строка, представляющий ожидаемую дату доставки заказа через 30 дней.
        new_client: Флаг, указывающий, является ли клиент новым. По умолчанию False.

        Возвращает text: str.
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
            self, text: str, message, reply_markup, bot, state=None):
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
        if state != None:
            await state.clear()

    async def send_messange_bot_seller_line(self,
                                            bot, chat_id: int, text: str, parse_mode: str,
                                            reply_markup: InlineKeyboardMarkup,
                                            disable_web_page_preview: bool = False
                                            ) -> None:
        """
        Отправляет сообщение в чат с разбиением на несколько сообщений, если длина текста превышает 4096 символов.

        Аргументы:
        bot (Bot): Объект бота.
        chat_id (int): Идентификатор чата.
        text (str): Текст сообщения.
        parse_mode (str): Тип разметки текста.
        reply_markup (InlineKeyboardMarkup): Клавиатура для ответа на сообщение.
        disable_web_page_preview (bool): Флаг, указывающий, нужно ли отключить предварительный просмотр ссылок. По умолчанию False.

        Возвращает:
        None
        """
        lines = wrapper.wrap(text=text)
        line_list = []
        for line in lines:
            lines_replace = line.replace("</b>", "").\
                replace("<b>", "").replace("</code>", "").replace("<code>", "")
            line_list.append(lines_replace)
        for l in line_list:
            await bot.send_message(
                chat_id=chat_id,
                text=l,
                parse_mode=parse_mode,
                reply_markup=reply_markup,
                disable_web_page_preview=disable_web_page_preview
            )
            await asyncio.sleep(1)

    async def send_finish_message_order(self,
                                        bot, chat_id: int, text: str, parse_mode: str,
                                        reply_markup: InlineKeyboardMarkup,
                                        disable_web_page_preview: bool = True
                                        ) -> None:
        """
        Отправляет финальное сообщение о заказе в чат с разбиением на несколько сообщений, если длина текста превышает 4096 символов.

        Аргументы:
        bot (Bot): Объект бота.
        chat_id (int): Идентификатор чата.
        text (str): Текст сообщения.
        parse_mode (str): Тип разметки текста.
        reply_markup (InlineKeyboardMarkup): Клавиатура для ответа на сообщение.
        disable_web_page_preview (bool): Флаг, указывающий, нужно ли отключить предварительный просмотр ссылок. По умолчанию False.

        Возвращает:
        None
        """
        order_list = ShoppingСartЕextGeneration()

        if len(text) > 4096:
            await order_list.send_messange_bot_seller_line(
                bot=bot, chat_id=chat_id, text=text, parse_mode=parse_mode,
                reply_markup=reply_markup,
                disable_web_page_preview=disable_web_page_preview
            )
        else:
            await bot.send_message(
                chat_id=chat_id, text=text, parse_mode=parse_mode,
                reply_markup=reply_markup,
                disable_web_page_preview=disable_web_page_preview
            )


async def random_order_int() -> int:
    """Создает рандомное число в радиусе MIN_RANDOM_INT до MAX_RANDOM_INT

    Returns:
        int: order
    """
    order = random.randint(settings.MIN_RANDOM_INT,
                           settings.MAX_RANDOM_INT)
    return order


# Формирование отправки сообщения для клиента
async def order_formation(
    user_id: int, value: int, client_data, bot, message, order_botton, state=None,
    new_client: bool = False, callback: bool = False
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
    callback (bool): Флаг, указывающий, являеться ли отправка сообщение message или callback.

    Возвращает:
    None
    """
    # получение данных корзины клинета
    order_all_date = await order_user_id_all(user_id)
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
    if callback == False:
        # проверка длины текста если оно больше 4096, то делить его на разные смс
        await order_list.send_messange_bot_client_line(
            bot=bot, message=message, reply_markup=order_botton,
            state=state, text=text
        )
    else:
        await order_list.send_messange_bot_client_line(
            bot=bot, message=message, reply_markup=order_botton, text=text
        )


async def get_order_list_data(order_id: int, value: int, user_link: str) -> tuple:
    """
    Получает информацию о заказах и общую стоимость для списка заказов.

    Аргументы:
        order_id (list): Список объектов заказов.
        value (int): Значение, используемое в расчете цены.
        user_link (str): Ссылка пользователя, используемая в информации о заказе.

    Возвращает:
        tuple: Кортеж, содержащий информацию о заказе в виде строки и общую стоимость в виде целого числа.
    """
    price = []
    shipping_cost = []
    order_info = []
    for order in order_id:
        price.append(order.price)
        shipping_cost_int = order.shipping_cost
        shipping_cost.append(order.shipping_cost)
        price_rub_round = int(
            value*order.price + order.shipping_cost)
        addres = order.addres
        url = order.url
        color = order.color
        price_int = order.price
        phone = order.phone
        name = order.name
        orders = order.order
        user_id = order.user_id
        order_info.append(LEXICON_RU['Форма заказа'].format(
            url, color, price_int, price_rub_round, shipping_cost_int, orders
        )
        )
        total_price = round(sum(price)*value + sum(shipping_cost))
        price_rub = (price_int*value)+shipping_cost_int
        user_link_phone = phone
        if user_link.startswith("<code>7"):
            await add_order_save(addres, url, color, price_int, phone,
                                 name, orders, user_id, shipping_cost_int,
                                 user_link_phone, price_rub)
        else:
            await add_order_save(addres, url, color, price_int, phone,
                                 name, orders, user_id, shipping_cost_int,
                                 user_link, price_rub)
    order_info = '\n'.join(order_info)
    return order_info, total_price


async def send_messages(
    bot, lines, chat_id, parse_mode, reply_markup,
    disable_web_page_preview=None
):
    line_list = []
    for line in lines:
        lines_replace = line.replace(
            "</b>", "").replace("<b>", "").replace("</code>", "").\
            replace("<code>", "")
        line_list.append(lines_replace)
    for l in line_list:
        await bot.send_message(
            chat_id=chat_id,
            text=l,
            parse_mode=parse_mode,
            reply_markup=reply_markup,
            disable_web_page_preview=disable_web_page_preview
        )
        await asyncio.sleep(1)


async def shipping_costing(
        message, cost_ships, reply_markup, state, category
):
    text = float(message.text)
    value = await course_today()
    if value is not None:
        value_markup = text * value + cost_ships
        round_value = round(value_markup)
        formatted_num = "{}\\.{}".format(
            int(value), int(value * 100) % 100)
        await message.answer(text=LEXICON_RU['Калькулятор цен'].format(
            round_value, cost_ships, formatted_num, category),
            parse_mode='MarkdownV2',
            reply_markup=reply_markup
        )
        await state.clear()
    else:
        await message.reply(text=LEXICON_RU["Данные о валюте"])


async def send_photo_calculator(bot, callback, static):
    await bot.send_photo(
        chat_id=callback.message.chat.id,
        caption=LEXICON_RU["Ввести стоимость"],
        photo=static.photo_url_rate_1,
        parse_mode='MarkdownV2'
    )
    await bot.send_photo(
        chat_id=callback.message.chat.id,
        caption=LEXICON_RU["Выкуп"],
        photo=static.photo_url_rate_2,
        parse_mode='MarkdownV2',
        allow_sending_without_reply=True
    )
    await callback.answer(show_alert=True)


async def logger_error_critical_send_message_admin(logger, traceback, bot):
    logger.critical(msg="Где-то ошибенка", exc_info=True)
    error_message = str({traceback.format_exc()})
    await bot.send_message(
        chat_id=settings.ADMIN_ID2,
        text="Эй герой, произошел пиздец, иди решай его\n\n" + error_message
    )
