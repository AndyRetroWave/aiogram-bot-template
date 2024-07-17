from datetime import timedelta
import re
import textwrap
import traceback
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from app.dependence.dependence import *
from app.lexicon.lexicon_ru import LEXICON_RU
from app.keyboards.keyboards import (
    order, order_botton, meny, order_botton_one,
    meny_order, menu_rare, payment_botton,
    delete_cart, orde_cart_back
)
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from app.models.course.dao import course_today
from app.models.course.models import cost_ships
from app.models.order.dao import *
from app.states.states import FSMDeleteorder, FSMOrders, FSMConfirmation
from aiogram.fsm.state import default_state
from config.config import settings, bot, logger
from app.static.images import static
import calendar
from app.api.response_rate import months
import asyncio

router = Router()

max_length = 4096
wrapper = textwrap.TextWrapper(width=max_length, replace_whitespace=False)


# Кнопка заказ
@router.callback_query(F.data == 'botton_orders')
async def category_botton_order(callback: CallbackQuery):
    try:
        # Отправление сообщения с выбором категори товара
        await callback.message.edit_text(
            text=LEXICON_RU["Категория"],
            reply_markup=order,
            parse_mode='MarkdownV2'
        )
        await callback.answer(show_alert=True)
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Кнопка добавить заказ
@router.callback_query(F.data == 'add_order_botton')
async def category_botton_order_new(callback: CallbackQuery):
    try:
        await callback.message.edit_text(
            text=LEXICON_RU["Категория"],
            reply_markup=orde_cart_back,
            parse_mode='MarkdownV2'
        )
        await callback.answer(show_alert=True)
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Кнопка повтора заказа
@router.callback_query(F.data == 'order_botton')
async def category_botton_order(callback: CallbackQuery):
    try:
        await callback.message.edit_text(
            text=LEXICON_RU["Категория"],
            reply_markup=order,
            parse_mode='MarkdownV2'
        )
        await callback.answer(show_alert=True)
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Кнопка кросовка
@router.callback_query(F.data == 'button_snecers_order', StateFilter(default_state))
async def sneaks_button_order(callback: CallbackQuery, state: FSMContext):
    try:
        await send_photo_calculator(
            static=static, bot=bot, callback=callback
        )
        await state.set_state(FSMOrders.price_snecers)
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Хендлер по цене кросовок
@router.message(StateFilter(FSMOrders.price_snecers))
async def calculator_rate_value_order(message: Message, state: FSMContext):
    try:
        try:
            # Получение цены
            text = int(message.text)
            # Получение актуальной стоимости доставки
            shipping_cost = cost_ships.sneaker
            # Запись данных с ввода от пользователя
            await state.update_data({"shipping_cost": shipping_cost})
            await state.update_data({"round_value": text})
            # Передача машиного состояни на ссылку
            await state.set_state(FSMOrders.url)
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=static.url_order,
                caption=LEXICON_RU["Ссылка на товар"],
                parse_mode='MarkdownV2'
            )
        except ValueError:
            # Если пользователь ввел не правильный тип данных
            await message.answer(text=LEXICON_RU["Стоимость в юанях"],
                                 parse_mode='MarkdownV2')
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Кнопка Одежды
@router.callback_query(F.data == 'button_clothe_order', StateFilter(default_state))
async def sneaks_button_order(callback: CallbackQuery, state: FSMContext):
    try:
        await send_photo_calculator(
            static=static, bot=bot, callback=callback
        )
        await state.set_state(FSMOrders.price_clothe)
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Хендлер по цене одежды
@router.message(StateFilter(FSMOrders.price_clothe))
async def calculator_rate_value_order_clothed(message: Message, state: FSMContext):
    try:
        try:
            # Получение цены от клиента
            text = int(message.text)
            # Получение актуально цены доставки для кроссовка
            shipping_cost = cost_ships.closer
            # Запить данных в машино-состояние
            await state.update_data({"shipping_cost": shipping_cost})
            await state.update_data({"round_value": text})
            # Передача машиного состояния к ссылке
            await state.set_state(FSMOrders.url)
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=static.url_order,
                caption=LEXICON_RU["Ссылка на товар"],
                parse_mode='MarkdownV2'
            )
        except ValueError:
            # Отправка смс если пользователь ввел не тот тип данных
            await message.answer(text=LEXICON_RU["Стоимость в юанях"],
                                 parse_mode='MarkdownV2')
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Кнопка Пуховики
@router.callback_query(F.data == 'button_down_jacket_order', StateFilter(default_state))
async def sneaks_button_order(callback: CallbackQuery, state: FSMContext):
    try:
        await send_photo_calculator(
            static=static, bot=bot, callback=callback
        )
        await state.set_state(FSMOrders.price_jacket)
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Хендлер по цене пуховиков
@router.message(StateFilter(FSMOrders.price_jacket))
async def calculator_rate_value_order_jacket(message: Message, state: FSMContext):
    try:
        try:
            # Получение цены от клиента
            text = int(message.text)
            # Получение актуально цены доставки для пуховика
            shipping_cost = cost_ships.jacket
            # Запить данных в машино-состояние
            await state.update_data({"shipping_cost": shipping_cost})
            await state.update_data({"round_value": text})
            # Передача машиного состояния к ссылке
            await state.set_state(FSMOrders.url)
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=static.url_order,
                caption=LEXICON_RU["Ссылка на товар"],
                parse_mode='MarkdownV2'
            )
        except ValueError:
            # Отправка смс если пользователь ввел не тот тип данных
            await message.answer(text=LEXICON_RU["Стоимость в юанях"],
                                 parse_mode='MarkdownV2')
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Кнопка Пуховики
@router.callback_query(F.data == 'button_care_order', StateFilter(default_state))
async def jacket_button_order(callback: CallbackQuery, state: FSMContext):
    try:
        await send_photo_calculator(
            static=static, bot=bot, callback=callback)
        await state.set_state(FSMOrders.price_clothe)
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Кнопка аксессуары
@router.callback_query(F.data == 'button_jewelr_order')
async def button_jewelry(callback: CallbackQuery):
    try:
        user_id = callback.message.from_user.id
        # Получение сведения о наличии оформленного заказа у клиента
        order = await add_save_order(user_id)
        # Если он есть
        if order:
            await callback.message.edit_text(
                text=LEXICON_RU["Заказ аксессуаров"],
                parse_mode='MarkdownV2',
                reply_markup=meny_order,)
            await callback.answer(show_alert=True)
        # Если его нет
        else:
            await callback.message.edit_text(
                text=LEXICON_RU["Заказ аксессуаров"],
                parse_mode='MarkdownV2',
                reply_markup=meny,)
            await callback.answer(show_alert=True)
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Хенедер по ссылки на товар
@router.message(StateFilter(FSMOrders.url))
async def url_order(message: Message, state: FSMContext):
    try:
        text = message.text
        # Регулярное выражение поиска url ссылки из текста
        try:
            url = re.search(r'https?://\S+', text).group(0)
            await state.update_data({"url": url})
        # Если не получилось то просто отдаем этот текст боту
        except:
            await state.update_data({"url": text})
        await message.answer(
            text=LEXICON_RU["Размер товара"],
            parse_mode='MarkdownV2'
        )
        # Передаем машино-состояние дальше
        await state.set_state(FSMOrders.color)
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Хенедер по Номеру телефона
@router.message(StateFilter(FSMOrders.phone))
async def phone_order(message: Message, state: FSMContext):
    try:
        try:
            user = message.from_user.username
            # Получение данных о номере телефона клиента
            phone = message.text
            # Проверяем правильность ввода номера телефона
            if re.match(r'^7\d{10}$', phone):
                # Записываем данные в машино-состояние
                await state.update_data({"phone": phone})
                await message.answer(
                    text=LEXICON_RU["ФИО"],
                    parse_mode='MarkdownV2'
                )
                # Передаем машино-состояние дальше
                await state.set_state(FSMOrders.name)
            else:
                await message.answer(text=LEXICON_RU["Введите правильно номер"],
                                     parse_mode='MarkdownV2')
        except:
            await message.answer(text=LEXICON_RU["Введите правильно номер"],
                                 parse_mode='MarkdownV2')
            logger.info(
                f"Пользователь {user} совершил ошибку в номере телефона")
        await state.update_data({"phone": phone})
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Хенедер по ФИО
@router.message(StateFilter(FSMOrders.name))
async def phone_order(message: Message, state: FSMContext):
    try:
        # Получаем ФИО от клиента
        username = message.text
        await message.answer(
            text=LEXICON_RU["Адрес"],
            parse_mode='MarkdownV2',
        )
        # Записываем ее в машино состояние
        await state.update_data({"username": username})
        # Идем дальше
        await state.set_state(FSMOrders.penza)
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Хенедер по адрусу пензы и итого по первому заказу для клиента ИТОГО
@router.message(StateFilter(FSMOrders.penza))
async def phone_order(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id  # Получение id клиента
        addres = message.text  # Получение адреса с прошлого смс
        # Получение данных из машино-состоянии
        await state.update_data({"addres": addres})
        data_order = await state.update_data()
        value = await course_today()  # Получаем курс на данный момент
        order = await random_order_int()  # Генерация номера заказ
        # Добавления заказа в корзину (базу данных)
        await add_order(
            addres, data_order['url'], data_order['color'],
            data_order["round_value"], data_order["phone"],
            data_order["username"], order, user_id,
            data_order['shipping_cost']
        )
        # Добавление данных о клиенте в базу данных
        await add_diven_user(
            addres, data_order["phone"], data_order["username"], user_id
        )
        # формирование и отправка смс клиетну
        await order_formation(
            bot=bot, client_data=data_order, message=message,
            order_botton=order_botton, state=state, user_id=user_id,
            value=value, new_client=True
        )
        await state.clear()
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Хенедер по цвету и размеру и по вывода итого если пользователь уже оформлял заказы ИТОГО
@router.message(StateFilter(FSMOrders.color))
async def color_order(message: Message, state: FSMContext):
    try:
        # Получаем id клиента
        user_id = message.from_user.id
        # Получаем цвет и размер товара
        color = message.text
        # Записываем цвет в машиносостояние
        await state.update_data({"color": color})
        # Получение данных из машинно состояния
        data_order = await state.update_data()
        # Получение актуальных данных клиента
        client_data = await get_clien_data(user_id)
        # Если клиент уже формировал корзину не просить его вводить клиенские данные
        if client_data != None:
            # получение актуального курса юаня
            value = round(await course_today())
            # получение номера заказа
            order = await random_order_int()
            # добавление заказа в базу данных для корзины
            await add_order(
                round_value=data_order["round_value"],
                shipping_cost=data_order['shipping_cost'],
                url=data_order['url'], addres=client_data.addres,
                phone=client_data.phone, username=client_data.name,
                order=order, color=color, user_id=user_id,
            )
            # формируем и отправляем смс
            await order_formation(
                bot=bot, client_data=client_data, message=message,
                order_botton=order_botton, state=state, user_id=user_id,
                value=value
            )
        else:
            # Если у клиента еще небыло корзины
            await message.answer(
                text=LEXICON_RU["Номер телефона"],
                parse_mode='MarkdownV2'
            )
            await state.set_state(FSMOrders.phone)
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Хенедер кнопки по изменению Номера телефона
@router.callback_query(F.data == 'addres_modify_botton', StateFilter(default_state))
async def phone_order(callback: CallbackQuery, state: FSMContext):
    try:
        user_id = callback.from_user.id
        await bot.send_message(
            chat_id=user_id,
            text=LEXICON_RU["Номер телефона"],
            parse_mode='MarkdownV2'
        )
        await state.set_state(FSMOrders.phone_modify)
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Хенедер по изменению Номера телефона
@router.message(StateFilter(FSMOrders.phone_modify))
async def phone_order_modify(message: Message, state: FSMContext):
    try:
        try:
            # получение данных
            user = message.from_user.username
            user_id = message.from_user.id
            phone_old = str(message.text)
            # Изменение данных в базе по корзине и в данных клиента
            await modify_phone_user_id(user_id, phone_old)
            await modify_phone_user_id_order(user_id, phone_old)
            # если неправильно отправил номер телефона
            if not re.match(r'^7\d{10}$', phone_old):
                await message.answer(
                    text=LEXICON_RU["Введите правильно номер"],
                    parse_mode='MarkdownV2')
                return
            # Получение номера телефона
            phone = await get_clien_data(user_id)
            # записть в машино-состояние
            await state.update_data({"phone": phone.phone})
            await message.answer(
                text=LEXICON_RU["ФИО"],
                parse_mode='MarkdownV2'
            )
            # передача машино-состояние дальше
            await state.set_state(FSMOrders.name_modify)
            await state.update_data({"phone": phone})
        except:
            await message.answer(text=LEXICON_RU["Введите правильно номер"],
                                 parse_mode='MarkdownV2')
            logger.info(
                f"Пользователь {user} совершил ошибку в  изменение номера телефона")
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Хенедер по изменения ФИО
@router.message(StateFilter(FSMOrders.name_modify))
async def phone_order_modify(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        username_old = str(message.text)
        await modify_username_user_id(user_id, username_old)
        await modify_username_user_id_order(user_id, username_old)
        await message.answer(
            text=LEXICON_RU["Адрес"],
            parse_mode='MarkdownV2',
        )
        clien_data = await get_clien_data(user_id)
        await state.update_data({"username": clien_data.name})
        await state.set_state(FSMOrders.adress_modify)
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Хенедер по измененному адрусу пензы и итого по первому заказу для клиента ИТОГО
@router.message(StateFilter(FSMOrders.adress_modify))
async def phone_order(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        addres_old = str(message.text)
        value = await course_today()
        await modify_addres_user_id(user_id, addres_old)
        await modify_addres_user_id_order(user_id, addres_old)
        client_data = await get_clien_data(user_id)
        await order_formation(
            bot=bot, client_data=client_data, message=message,
            order_botton=order_botton, state=state, user_id=user_id,
            value=value
        )
        await state.clear()
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )

# Кнопка удалить заказ


@router.callback_query(F.data == 'delete_order_botton', StateFilter(default_state))
async def category_botton_order(callback: CallbackQuery, state: FSMContext):
    try:
        use_id = callback.from_user.id
        await bot.send_message(
            chat_id=use_id,
            text=LEXICON_RU["Удалить заказ"],
            parse_mode='MarkdownV2'
        )
        await state.set_state(FSMDeleteorder.delete)
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Хенедер по удалению заказа итого по заказам ИТОГО
@router.message(StateFilter(FSMDeleteorder.delete))
async def delete_order_botton(message: Message, state: FSMContext):
    try:
        try:
            user_id = message.from_user.id
            order = int(message.text)
            await delete_order_user_id(user_id, order)
            value = await course_today()
            order_id = await order_user_id_all(user_id)
            client_data = await get_clien_data(user_id)
            order_data = await get_user_id_all_save(user_id=user_id)
            if order_id != []:
                await order_formation(
                    bot=bot, client_data=client_data, message=message,
                    order_botton=order_botton, state=state, user_id=user_id,
                    value=value
                )
            else:
                if order_data != []:
                    await bot.send_message(
                        chat_id=user_id,
                        text=LEXICON_RU["Привет"],
                        reply_markup=meny_order,
                        parse_mode='MarkdownV2',
                        disable_web_page_preview=True)
                    await state.clear()
                else:
                    await bot.send_message(
                        chat_id=user_id,
                        text=LEXICON_RU["Привет"],
                        reply_markup=meny,
                        parse_mode='MarkdownV2',
                        disable_web_page_preview=True)
        except:
            await bot.send_message(
                chat_id=user_id,
                text="Введите номер заказа числом, а не буквами")
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )

# Кнопка Корзины


@router.callback_query(F.data == 'cart_botton')
async def basket(callback: CallbackQuery):
    try:
        user_id = callback.from_user.id
        value = await course_today()
        order_id = await order_user_id_all(user_id)
        client_data = await get_clien_data(user_id)
        if order_id != []:
            await order_formation(
                bot=bot, client_data=client_data, message=callback,
                order_botton=order_botton, user_id=user_id,
                value=value, callback=True
            )
            callback.answer()
        else:
            await callback.answer(
                text=LEXICON_RU["Корзина"],
                reply_markup=order_botton_one,
                parse_mode='MarkdownV2',
            )
        callback.answer()
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# кнопка обновить корзину
@router.callback_query(F.data == 'upgrate_botton')
async def basket(callback: CallbackQuery):
    try:
        user_id = callback.from_user.id
        value = await course_today()
        client_data = await get_clien_data(user_id)
        order_id = await order_user_id_all(user_id)
        await bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        if order_id != []:
            await order_formation(
                bot=bot, client_data=client_data, message=callback,
                order_botton=order_botton, user_id=user_id,
                value=value, callback=True
            )
        else:
            await callback.answer(
                text=LEXICON_RU["Корзина"],
                reply_markup=order_botton_one,
                parse_mode='MarkdownV2',
            )
        callback.answer()
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Кнопка подверждения заказа
@router.callback_query(F.data == 'payment_botton')
async def order_confirmation(callback: CallbackQuery, state: FSMContext):
    try:
        user = callback.from_user
        user_id = callback.from_user.id
        value = await course_today()
        client_data = await get_clien_data(user_id)
        order_id = await order_user_id_all(user_id)
        await state.update_data(user_id=user_id)
        user_link = f"https://t.me/{user.username}" if user.username \
                    else f"<code>{client_data.phone}</code> "
        if order_id != []:
            order_info = await get_order_list_data(
                order_id=order_id, value=value, user_link=user_link
            )
            new_dates = await order_date_receipt()
            new_date_20_formatted, new_date_30_formatted = new_dates
            await delete_order(user_id)
            text = LEXICON_RU['Спасибо за заказ'].format(
                new_date_20_formatted, new_date_30_formatted
            )
            await callback.message.edit_text(
                text=text,
                parse_mode='MarkdownV2',
                reply_markup=meny_order,
            )
            callback.answer()
            text_phone = LEXICON_RU['Отчет о заказе с телефоном'].format(
                user_link, user_id, value, order_info[0], client_data.addres,
                client_data.name, client_data.phone, order_info[1]
            )
            text_url = LEXICON_RU['Отчет о заказе с ссылкой'].format(
                user_link, user_id, value, order_info[0], client_data.addres,
                client_data.name, client_data.phone, order_info[1]
            )

            order_list = ShoppingСartЕextGeneration()
            if user_link.startswith("<code>7"):
                await order_list.send_finish_message_order(
                    bot=bot, chat_id=settings.ADMIN_ID2, text=text_phone,
                    parse_mode="HTML", reply_markup=payment_botton
                )
            else:
                await order_list.send_finish_message_order(
                    bot=bot, chat_id=settings.ADMIN_ID2, text=text_url,
                    parse_mode="HTML", reply_markup=payment_botton
                )
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# кнопка подтверждение заказа от продавца
@router.callback_query(F.data == 'payment_botton_money', StateFilter(default_state))
async def order_confirmation_money(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    await bot.send_message(
        chat_id=user_id,
        text="Введи id клиента для подтверждения заказа")
    await state.set_state(FSMConfirmation.user_id)


# Отправка подтверждения заказа для клиента
@router.message(StateFilter(FSMConfirmation.user_id))
async def message_confirmation_money(message: Message, state: FSMContext):
    try:
        try:
            user_id = int(message.text)
            await bot.send_message(
                chat_id=user_id,
                text="Мы получили деньги и вот уже выкупаем ваш заказ❗ Ожидайте его в установленные сроки🌊")
            await message.answer(text="Подтверждение успешно отправленно")
            await state.clear()
        except:
            await message.answer(text="Произошла ошибка, смс не отправленно клиенту")
            await state.clear()
    except:
        message.answer(text="Введи id клиента")


# Ваш заказ
@router.callback_query(F.data == 'order_client_botton')
async def order_user(callback: CallbackQuery):
    try:
        value = await course_today()
        user = callback.from_user
        user_id = user.id
        order_id = await get_user_id_all_save(user_id)
        addres, phone, username, orders, url, color, price, \
            price_rub, shipping_cost, data_20, data_30 = [
            ], [], [], [], [], [], [], [], [], [], []
        if order_id:
            for order in order_id:
                orders.append(order.order)
                url.append(order.url)
                color.append(order.color)
                price.append(order.price)
                addres.append(order.addres)
                phone.append(order.phone)
                username.append(order.name)
                shipping_cost.append(order.shipping_cost)
                price_rub_round = round(
                    value*order.price + order.order)
                price_rub.append(price_rub_round)
                data = order.data
                new_date_20 = data + timedelta(days=20)
                new_date_30 = data + timedelta(days=30)
                month_name_en_20 = calendar.month_name[new_date_20.month]
                month_name_ru_20 = months[month_name_en_20]
                month_name_en_30 = calendar.month_name[new_date_30.month]
                month_name_ru_30 = months[month_name_en_30]
                data_20.append(f'{new_date_20.day} {month_name_ru_20}')
                data_30.append(
                    f'{new_date_30.day} {month_name_ru_30} {new_date_30.year} года')
                order_info = '\n'.join(
                    [f"""---- Ссылка: {u}\nЦвет и размер: <b>{c}</b> на сумму <b>{p}</b> юаней\nЦена с доставкой: <b>{r}</b> ₽
Стоимость доставки составило: <b>{s}</b> ₽\nПримерная дата доставки: <b>{d_20} - {d_30}</b>
Данные получателя:\n<b>{name}\n{ph}\n{adr}</b>\nНомер заказа: <code>{o}</code>⚠\n"""
                     for o, u, c, p, r, s, d_20, d_30, name, ph, adr in zip(
                         orders, url, color, price, price_rub, shipping_cost,
                         data_20, data_30, username, phone, addres
                     )
                     ]
                )
        lines = wrapper.wrap(text=order_info)
        if len(order_info) > 4096:
            line_list = []
            for line in lines:
                lines_replace = line.replace(
                    "</b>", "").replace("<b>", "").replace("</code>", "").\
                    replace("<code>", "")
                line_list.append(lines_replace)
            for line in line_list:
                await bot.send_message(
                    chat_id=user_id,
                    text=f"""{line}""",
                    parse_mode="HTML",
                    disable_web_page_preview=True
                )
                await asyncio.sleep(1)
            await bot.send_message(
                chat_id=user_id,
                text="Это список ваших заказов💌\nПри получение товара, позиция будет удалена из истории❗",
                reply_markup=menu_rare,
                disable_web_page_preview=True)
            await asyncio.sleep(1)
        else:
            await bot.send_message(
                chat_id=user_id,
                text=f"""{order_info}""",
                parse_mode="HTML",
            )
            await asyncio.sleep(1)
            await bot.send_message(
                chat_id=user_id,
                text="Это список ваших заказов💌\nПри получение товара, позиция будет удалена из истории❗",
                reply_markup=menu_rare,
                disable_web_page_preview=True)
            await asyncio.sleep(1)
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Кнопка очищение корзины
@router.callback_query(F.data == 'delete_order')
async def order_user(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON_RU["Подтверждения удаления"],
        reply_markup=delete_cart)


# Очищение корзины
@router.callback_query(F.data == 'delete_order_2')
async def order_user(callback: CallbackQuery):
    user_id = callback.from_user.id
    await delete_order(user_id)
    await callback.message.edit_text(
        text=LEXICON_RU["Удаление корзины"],
        reply_markup=menu_rare)


async def delete_month_order():
    await delete_old_order()
