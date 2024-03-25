import random
import re
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from app.lexicon.lexicon_ru import LEXICON_RU
from app.keyboards.keyboards import order, order_botton
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from app.models.course.dao import course_today
from app.models.order.dao import *
from app.states.states import FSMAdress, FSMOrders
from aiogram.fsm.state import default_state
from config.config import bot, logger
from app.static.images import static

router = Router()

# Кнопка заказ


@router.callback_query(F.data == 'botton_orders')
async def category_botton_order(callback: CallbackQuery):
    try:
        user = callback.from_user.username
        logger.info(f"Пользователь {user} нажал на кнопку заказа")
        await callback.message.edit_text(
            text=LEXICON_RU["Категория"],
            reply_markup=order,
            parse_mode='MarkdownV2'
        )
        await callback.answer(show_alert=True)
    except:
        logger.critical("Ошибка в кнопке заказа")


# Кнопка повтора заказа
@router.callback_query(F.data == 'order_botton')
async def category_botton_order(callback: CallbackQuery):
    try:
        user = callback.from_user.username
        logger.info(f"Пользователь {user} нажал на кнопку заказа")
        await callback.message.edit_text(
            text=LEXICON_RU["Категория"],
            reply_markup=order,
            parse_mode='MarkdownV2'
        )
        await callback.answer(show_alert=True)
    except:
        logger.critical("Ошибка в кнопке заказа")


# Кнопка кросовка
@router.callback_query(F.data == 'button_snecers_order', StateFilter(default_state))
async def sneaks_button_order(callback: CallbackQuery, state: FSMContext):
    try:
        user = callback.from_user.username
        logger.info(
            f"Пользователь {user} нажал на кнопку калькулятора кросовок в заказе")
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
        await state.set_state(FSMOrders.price_snecers)
    except:
        logger.critical("Ошибка в кнопке кросовка в заказе")


# Хендлер по цене кросовок
@router.message(StateFilter(FSMOrders.price_snecers))
async def calculator_rate_value_order(message: Message, state: FSMContext):
    try:
        user = message.from_user.username
        logger.info(f"Пользователь {user} посчитал цену кросовок в заказе")
        try:
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=static.url_order,
                caption=LEXICON_RU["Ссылка на товар"],
                parse_mode='MarkdownV2'
            )
            text = int(message.text)
            value = await course_today()
            value_markup = text * value + 1200
            # round_value = round(value_markup)
            shipping_cost = 1200
            await state.update_data({"shipping_cost": shipping_cost})
            await state.update_data({"round_value": text})
            await state.set_state(FSMOrders.url)
        except ValueError:
            await message.answer(text=LEXICON_RU["Стоимость в юанях"],
                                 parse_mode='MarkdownV2')
    except:
        logger.critical("Ошибка в калькуляторе кросовок в заказе")


# Кнопка Одежды
@router.callback_query(F.data == 'button_clothe_order', StateFilter(default_state))
async def sneaks_button_order(callback: CallbackQuery, state: FSMContext):
    try:
        user = callback.from_user.username
        logger.info(
            f"Пользователь {user} нажал на кнопку калькулятора одежды в заказе")
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
        await state.set_state(FSMOrders.price_clothe)
    except:
        logger.critical("Ошибка в кнопке одежды в заказе")


# Хендлер по цене одежды
@router.message(StateFilter(FSMOrders.price_clothe))
async def calculator_rate_value_order(message: Message, state: FSMContext):
    try:
        user = message.from_user.username
        logger.info(f"Пользователь {user} посчитал цену ордежды в заказе")
        try:
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=static.url_order,
                caption=LEXICON_RU["Ссылка на товар"],
                parse_mode='MarkdownV2'
            )
            text = int(message.text)
            value = await course_today()
            value_markup = text * value + 1000
            round_value = round(value_markup)
            shipping_cost = 1000
            await state.update_data({"shipping_cost": shipping_cost})
            await state.update_data({"round_value": text})
            await state.set_state(FSMOrders.url)
        except ValueError:
            await message.answer(text=LEXICON_RU["Стоимость в юанях"],
                                 parse_mode='MarkdownV2')
    except:
        logger.critical("Ошибка в калькуляторе одежды в заказе")


# Кнопка Пуховики
@router.callback_query(F.data == 'button_down_jacket_order', StateFilter(default_state))
async def sneaks_button_order(callback: CallbackQuery, state: FSMContext):
    try:
        user = callback.from_user.username
        logger.info(
            f"Пользователь {user} нажал на кнопку калькулятора пуховиков в заказе")
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
        await state.set_state(FSMOrders.price_jacket)
    except:
        logger.critical("Ошибка в кнопке пуховиков в заказе")


# Хендлер по цене пуховиков
@router.message(StateFilter(FSMOrders.price_jacket))
async def calculator_rate_value_order(message: Message, state: FSMContext):
    try:
        user = message.from_user.username
        logger.info(f"Пользователь {user} посчитал цену пуховиков в заказе")
        try:
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=static.url_order,
                caption=LEXICON_RU["Ссылка на товар"],
                parse_mode='MarkdownV2'
            )
            text = int(message.text)
            value = await course_today()
            value_markup = text * value + 1000
            round_value = round(value_markup)
            shipping_cost = 1000
            await state.update_data({"shipping_cost": shipping_cost})
            await state.update_data({"round_value": text})
            await state.set_state(FSMOrders.url)
        except ValueError:
            await message.answer(text=LEXICON_RU["Стоимость в юанях"],
                                 parse_mode='MarkdownV2')
    except:
        logger.critical("Ошибка в калькуляторе пуховиков в заказе")


# Кнопка Пуховики
@router.callback_query(F.data == 'button_care_order', StateFilter(default_state))
async def sneaks_button_order(callback: CallbackQuery, state: FSMContext):
    try:
        user = callback.from_user.username
        logger.info(
            f"Пользователь {user} нажал на кнопку калькулятора пуховиков в заказе")
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
        await state.set_state(FSMOrders.price_clothe)
    except:
        logger.critical("Ошибка в кнопке пуховиков в заказе")


# Хенедер по ссылки на товар
@router.message(StateFilter(FSMOrders.url))
async def url_order(message: Message, state: FSMContext):
    try:
        user = message.from_user.username
        logger.info(f"Пользователь {user} вписал ссылку на товар в заказе")
        url = message.text
        await message.answer(
            text=LEXICON_RU["Размер товара"],
            parse_mode='MarkdownV2'
        )
        await state.update_data({"url": url})
        await state.set_state(FSMOrders.color)
    except:
        logger.critical("Ошибка ссылки в заказе")


# Хенедер по цвету и размеру и по вывода итого если пользователь уже оформлял заказы
@router.message(StateFilter(FSMOrders.color))
async def color_order(message: Message, state: FSMContext):
    try:
        user = message.from_user.username
        logger.info(f"Пользователь {user} вписал цвет и размер")
        user_id = message.from_user.id
        color = message.text
        await state.update_data({"color": color})
        phone_user_id = await order_user_id_phone(user_id)
        if phone_user_id is not None:
            value = await course_today()
            round_value = round(value)
            user = message.from_user.username
            user_id = message.from_user.id
            logger.info(f"Пользователь {user} нажал на кнопку адреса пензы")
            addres = await order_user_id_addres(user_id)
            round_value = (await state.get_data())['round_value']
            url = (await state.get_data())['url']
            color = (await state.get_data())['color']
            phone = await order_user_id_phone(user_id)
            username = await order_user_id_username(user_id)
            shipping_cost = (await state.get_data())['shipping_cost']
            order = random.randint(1000000, 9999999)
            await add_order(addres, url, color, round_value, phone, username, order, user_id, shipping_cost)
            order_id = await order_user_id_all(user_id)
            color = []
            orders = []
            url = []
            price = []
            shipping_cost = []
            for order in order_id:
                orders.append(order['order'])
                url.append(order['url'])
                color.append(order['color'])
                price.append(order['price'])
                shipping_cost.append(order['shipping_cost'])
                order_info = '\n'.join(
                    [f'-<code>{u}</code>, цвет: <b>{c}</b> на <b>{p}</b> юаней, заказ№: <code>{o}</code>' for o, u, c, p in zip(orders, url, color, price)])
            total_price = round(sum(price)*value + sum(shipping_cost))
            await message.answer(
                text=f"""<b>Итоговая цена</b> составит <b>{total_price}</b> руб. с учетом всех сборов и доставки до Пензы. 🇷🇺
В заказе товары:\n
{order_info}\n
Курс юаня к рублю {value}\n
Доставка ИЗ Пензы оплачивается отдельно напрямую СДЭКу\n
🏡 Отправим ваш заказ по адресу:
<b>{addres}</b>
<b>{username}</b>
<b>{phone}</b>
Если вы хотите изменить данные, нажмите на кнопку Изменить адрес✏️\n
⚠️Мы выкупаем товар в течение 18 часов после оплаты. 
Если при выкупе цена изменится, с вами свяжется менеджер для доплаты или возврата средств.\n\n
_______________________
Если Вас устраивает, переведите <b>{total_price}</b> руб. на следующую карту 🏧
2202206381488191 Сбербанк! Нурлан А
_____________________\n
Осуществляя перевод, вы подтверждаете что корректно указали товар, его характеристики и согласны со сроками доставки. 
Мы не несем ответственности за соответствие размеров и брак.\n
Оплатите и нажмите кнопку Подтвердить оплату✅""",
                parse_mode='HTML',
                reply_markup=order_botton,
            )
            await state.clear()
        else:
            await message.answer(
                text=LEXICON_RU["Номер телефона"],
                parse_mode='MarkdownV2'
            )
            await state.set_state(FSMOrders.phone)
    except:
        logger.critical("Ошибка ссылки в заказе")


# Хенедер по Номеру телефона
@router.message(StateFilter(FSMOrders.phone))
async def phone_order(message: Message, state: FSMContext):
    try:
        try:
            user = message.from_user.username
            logger.info(f"Пользователь {user} вписал номер телефона")
            phone = message.text
            if not re.match(r'^7\d{10}$', phone):
                await message.answer(text=LEXICON_RU["Введите правильно номер"])
                return
            await state.update_data({"phone": phone})
            await message.answer(
                text=LEXICON_RU["ФИО"],
                parse_mode='MarkdownV2'
            )
            await state.set_state(FSMOrders.name)
        except:
            await message.answer(text=LEXICON_RU["Введите правильно номер"],
                                 parse_mode='MarkdownV2')
            logger.info(
                f"Пользователь {user} совершил ошибку в номере телефона")
        await state.update_data({"phone": phone})
    except:
        logger.critical("Ошибка ссылки в заказе")


# Хенедер по ФИО
@router.message(StateFilter(FSMOrders.name))
async def phone_order(message: Message, state: FSMContext):
    try:
        user = message.from_user.username
        logger.info(f"Пользователь {user} вписал ФИО")
        username = message.text
        await message.answer(
            text=LEXICON_RU["Адрес"],
            parse_mode='MarkdownV2',
        )
        await state.update_data({"username": username})
        await state.set_state(FSMOrders.penza)

    except:
        logger.critical("Ошибка ссылки в заказе")


# Хенедер по адрусу пензы и итого по первому заказу для клиента
@router.message(StateFilter(FSMOrders.penza))
async def phone_order(message: Message, state: FSMContext):
    try:
        value = await course_today()
        round_value = round(value)
        user = message.from_user.username
        user_id = message.from_user.id
        logger.info(f"Пользователь {user} нажал на кнопку адреса пензы")
        addres = message.text
        round_value = (await state.get_data())['round_value']
        url = (await state.get_data())['url']
        color = (await state.get_data())['color']
        phone = (await state.get_data())['phone']
        username = (await state.get_data())['username']
        shipping_cost = (await state.get_data())['shipping_cost']
        order = random.randint(1000000, 9999999)
        await add_order(addres, url, color, round_value, phone, username, order, user_id, shipping_cost)
        order_id = await order_user_id_all(user_id)
        color = []
        orders = []
        url = []
        price = []
        shipping_cost = []
        for order in order_id:
            orders.append(order['order'])
            url.append(order['url'])
            color.append(order['color'])
            price.append(order['price'])
            shipping_cost.append(order['shipping_cost'])
            order_info = '\n'.join(
                [f'-<code>{u}</code>, цвет: <b>{c}</b> на <b>{p}</b> юаней, заказ№: <code>{o}</code>' for o, u, c, p in zip(orders, url, color, price)])
        total_price = round(sum(price)*value + sum(shipping_cost))
        await bot.send_message(
            chat_id=message.from_user.id,
            text=f"""<b>Итоговая цена</b> составит <b>{total_price}</b> руб. с учетом всех сборов и доставки до Пензы. 🇷🇺
В заказе товары:\n
{order_info}\n
Курс юаня к рублю {value}\n
Доставка ИЗ Пензы оплачивается отдельно напрямую СДЭКу\n
🏡 Отправим ваш заказ по адресу:
<b>{addres}</b>
<b>{username}</b>
<b>{phone}</b>
Если вы хотите изменить данные, нажмите на кнопку <b>Изменить адрес доставки</b>✏️\n
⚠️Мы выкупаем товар в течение <b>18 часов после оплаты</b>. 
Если при выкупе цена изменится, с вами свяжется человек для доплаты или возврата средств.\n\n
_____________________
Если Вас устраивает, переведите <b>{total_price}</b> руб. на следующую карту 🏧
2202206381488191 Сбербанк! Нурлан А
_____________________\n
Осуществляя перевод, вы подтверждаете что корректно указали товар, его характеристики и согласны со сроками доставки. 
Мы не несем ответственности за соответствие размеров и брак.\n
Оплатите и нажмите кнопку Подтвердить оплату✅""",
            parse_mode='HTML',
            reply_markup=order_botton,
        )
        await state.clear()
    except:
        logger.critical("Ошибка адреса в заказе ")


# Хенедер кнопки по изменению Номера телефона
@router.callback_query(F.data == 'addres_modify_botton', StateFilter(default_state))
async def phone_order(callback: CallbackQuery, state: FSMContext):
    try:
        user = callback.from_user.username
        user_id = callback.from_user.id
        logger.info(f"Пользователь {user} нажал на изменение данных")
        await bot.send_message(
            chat_id=user_id,
            text=LEXICON_RU["Номер телефона"],
            parse_mode='MarkdownV2'
        )
        await state.set_state(FSMOrders.phone_modify)
    except:
        logger.critical("Ошибка ссылки в заказе")


# Хенедер по изменению Номера телефона
@router.message(StateFilter(FSMOrders.phone_modify))
async def phone_order_modify(message: Message, state: FSMContext):
    try:
        try:
            user = message.from_user.username
            user_id = message.from_user.id
            logger.info(
                f"Пользователь {user} вписал номер телефона в изменение данных")
            phone_old = str(message.text)
            await modify_phone_user_id(user_id, phone_old)
            if not re.match(r'^7\d{10}$', phone_old):
                await message.answer(text=LEXICON_RU["Введите правильно номер"])
                return
            phone = await order_user_id_phone(user_id)
            await state.update_data({"phone": phone})
            await message.answer(
                text=LEXICON_RU["ФИО"],
                parse_mode='MarkdownV2'
            )
            await state.set_state(FSMOrders.name_modify)
            await state.update_data({"phone": phone})
        except:
            await message.answer(text=LEXICON_RU["Введите правильно номер"],
                                 parse_mode='MarkdownV2')
            logger.info(
                f"Пользователь {user} совершил ошибку в  изменение номера телефона")
    except:
        logger.critical("Ошибка изменения номера телефона")


# Хенедер по изменения ФИО
@router.message(StateFilter(FSMOrders.name_modify))
async def phone_order_modify(message: Message, state: FSMContext):
    try:
        user = message.from_user.username
        user_id = message.from_user.id
        logger.info(f"Пользователь {user} вписал ФИО для изменения данных")
        username_old = str(message.text)
        await modify_username_user_id(user_id, username_old)
        await message.answer(
            text=LEXICON_RU["Адрес"],
            parse_mode='MarkdownV2',
        )
        username = await order_user_id_username(user_id)
        await state.update_data({"username": username})
        await state.set_state(FSMOrders.adress_modify)
    except:
        logger.critical("Ошибка ссылки в заказе")


# Хенедер по измененному адрусу пензы и итого по первому заказу для клиента
@router.message(StateFilter(FSMOrders.adress_modify))
async def phone_order(message: Message, state: FSMContext):
    try:
        user = message.from_user.username
        user_id = message.from_user.id
        logger.info(
            f"Пользователь {user} нажал на кнопку измененного адреса пензы и получил ответ заказа")
        addres_old = str(message.text)
        value = await course_today()
        addres = await modify_addres_user_id(user_id, addres_old)
        order_id = await order_user_id_all(user_id)
        addres = await order_user_id_addres(user_id)
        phone = await order_user_id_phone(user_id)
        username = await order_user_id_username(user_id)
        color = []
        orders = []
        url = []
        price = []
        shipping_cost = []
        for order in order_id:
            orders.append(order['order'])
            url.append(order['url'])
            color.append(order['color'])
            price.append(order['price'])
            shipping_cost.append(order['shipping_cost'])
            order_info = '\n'.join(
                [f'-<code>{u}</code>, цвет: <b>{c}</b> на <b>{p}</b> юаней, заказ№: <code>{o}</code>' for o, u, c, p in zip(orders, url, color, price)])
        total_price = round(sum(price)*value + sum(shipping_cost))
        await bot.send_message(
            chat_id=message.from_user.id,
            text=f"""<b>Итоговая цена</b> составит <b>{total_price}</b> руб. с учетом всех сборов и доставки до Пензы. 🇷🇺
В заказе товары:\n
{order_info}\n
Курс юаня к рублю {value}\n
Доставка ИЗ Пензы оплачивается отдельно напрямую СДЭКу\n
🏡 Отправим ваш заказ по адресу:
<b>{addres}</b>
<b>{username}</b>
<b>{phone}</b>
Если вы хотите изменить данные, нажмите на кнопку <b>Изменить адрес доставки</b>✏️\n
⚠️Мы выкупаем товар в течение <b>18 часов после оплаты</b>. 
Если при выкупе цена изменится, с вами свяжется человек для доплаты или возврата средств.\n\n
_____________________
Если Вас устраивает, переведите <b>{total_price}</b> руб. на следующую карту 🏧
2202206381488191 Сбербанк! Нурлан А
_____________________\n
Осуществляя перевод, вы подтверждаете что корректно указали товар, его характеристики и согласны со сроками доставки. 
Мы не несем ответственности за соответствие размеров и брак.\n
Оплатите и нажмите кнопку Подтвердить оплату✅""",
            parse_mode='HTML',
            reply_markup=order_botton,
        )
        await state.clear()
    except:
        logger.critical("Ошибка адреса в заказе ")
