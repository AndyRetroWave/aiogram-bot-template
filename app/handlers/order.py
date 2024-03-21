import re
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from app.lexicon.lexicon_ru import LEXICON_RU
from app.keyboards.keyboards import order, adress_botton, menu_one
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from app.models.course.dao import course_today
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
                photo = static.url_order,
                caption=LEXICON_RU["Ссылка на товар"],
                parse_mode='MarkdownV2'
                )
            text = float(message.text)
            value = await course_today()
            value_markup = text * value + 1200
            round_value = round(value_markup)
            await state.update_data({"round_value": round_value})
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
                photo = static.url_order,
                caption=LEXICON_RU["Ссылка на товар"],
                parse_mode='MarkdownV2'
                )
            text = float(message.text)
            value = await course_today()
            value_markup = text * value + 1000
            round_value = round(value_markup)
            await state.update_data({"round_value": round_value})
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
                photo = static.url_order,
                caption=LEXICON_RU["Ссылка на товар"],
                parse_mode='MarkdownV2'
                )
            text = float(message.text)
            value = await course_today()
            value_markup = text * value + 1000
            round_value = round(value_markup)
            await state.update_data({"round_value": round_value})
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


# Хенедер по цвету и размеру
@router.message(StateFilter(FSMOrders.color))
async def color_order(message: Message, state: FSMContext):
    try:
        user = message.from_user.username
        logger.info(f"Пользователь {user} вписал цвет и размер")
        color = message.text
        await message.answer(
                text=LEXICON_RU["Номер телефона"],
                parse_mode='MarkdownV2'
                )
        await state.update_data({"color": color})
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
            if not re.match(r'^\d{11}$', phone):
                await message.answer("Неправильный формат номера телефона. Пожалуйста, введите номер в формате +7XXXXXXXXXX.")
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
            logger.info(f"Пользователь {user} совершил ошибку в номере телефона")
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


# Хенедер по адрусу пензы 
@router.message( StateFilter(FSMOrders.penza))
async def phone_order(message: Message, state: FSMContext):
    try:
        user = message.from_user.username
        logger.info(f"Пользователь {user} нажал на кнопку адреса пензы")
        addres = message.text
        round_value = (await state.get_data())['round_value']
        url = (await state.get_data())['url']
        color = (await state.get_data())['color']
        phone = (await state.get_data())['phone']
        username = (await state.get_data())['username']
        await bot.send_message(
                chat_id=message.from_user.id,
                text=f"Вот такой итог мы имеем, имя\-{username}\nссылка\-{url}\nГород\-{addres}\nЦвет\-{color}\nстоимость\-{round_value}\nТелефон\-{phone}",
                )
        await state.clear()
    except:
        logger.critical("Ошибка адреса пензы в заказе ")

