import logging
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from app.lexicon.lexicon_ru import LEXICON_RU
from app.keyboards.keyboards import calculator_rate, update_calculator, meny
from app.api.response_rate import formatted_num
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from app.models.course.dao import course_today
from app.states.states import FSMCare, FSMClothes, FSMSneakers, FSMDownJacket
from app.static.images import photo_rate_1, photo_rate_2
from aiogram.fsm.state import default_state
from config.config import bot, logger

router = Router()


# Кнопка категория
@router.callback_query(F.data == 'big_button_1_pressed')
async def category_botton(callback: CallbackQuery):
    try:
        user = callback.from_user.username
        logger.info(f"Пользователь {user} нажал на кнопку Калькулятор цены")
        await callback.message.edit_text(
            text=LEXICON_RU["Категория"],
            reply_markup=calculator_rate,
            parse_mode='MarkdownV2'
        )
        await callback.answer(show_alert=True)
    except:
        logger.critical("Ошибка в кнопке категории")


# Кнопка повтора
@router.callback_query(F.data == 'big_button_1_pressed')
async def repetition_buttons(callback: CallbackQuery):
    try:
        user = callback.from_user.username
        logger.info(f"Пользователь {user} нажал на кнопку повтора")
        await callback.message.edit_text(
            text=LEXICON_RU["Категория"],
            reply_markup=calculator_rate,
            parse_mode='MarkdownV2'
        )
        await callback.answer(show_alert=True)
    except:
        logger.critical("Ошибка в кнопке повтора")

# Кнопка кросовка


@router.callback_query(F.data == 'button_snecers', StateFilter(default_state))
async def sneaks_button(callback: CallbackQuery, state: FSMContext):
    try:
        user = callback.from_user.username
        logger.info(
            f"Пользователь {user} нажал на кнопку калькулятора кросовок")
        await bot.send_photo(
            chat_id=callback.message.chat.id,
            caption=LEXICON_RU["Ввести стоимость"],
            photo=photo_rate_1,
            parse_mode='MarkdownV2'
        )
        await bot.send_photo(
            chat_id=callback.message.chat.id,
            caption=LEXICON_RU["Выкуп"],
            photo=photo_rate_2,
            parse_mode='MarkdownV2',
            allow_sending_without_reply=True
        )
        await callback.answer(show_alert=True)
        await state.set_state(FSMSneakers.rate_sneakers)
    except:
        logger.critical("Ошибка в кнопке кросовка")


# Хендлер по цене кросовок
@router.message(StateFilter(FSMSneakers.rate_sneakers))
async def calculator_rate_value(message: Message, state: FSMContext):
    try:
        user = message.from_user.username
        logger.info(f"Пользователь {user} посчитал цену кросовок")
        try:
            text = float(message.text)
            value = await course_today()
            if value is not None:
                value_markup = text * value + 1200
                round_value = round(value_markup)
                formatted_num = "{}\\.{}".format(
                    int(value), int(value * 100) % 100)
                await message.answer(text=str(
                    f"""Итого *{round_value}* руб\. с учетом всех расходов до Пензы❤️\n\nДля информации\:\nСтоимость доставки составила\: *1200 рублей\! \(уже учтено в цене\)*\nКурс юаня *{formatted_num}*\nКатегория\: Кросовки👟"""),
                    parse_mode='MarkdownV2',
                    reply_markup=update_calculator
                )
                await state.clear()
            else:
                await message.reply(text=LEXICON_RU["Данные о валюте"])
        except ValueError:
            await message.answer(text=LEXICON_RU["Стоимость в юанях"],
                                parse_mode='MarkdownV2')
    except:
        logger.critical("Ошибка в калькуляторе кросовок")


# Кнопка пуховики
@router.callback_query(F.data == 'button_down_jacket', StateFilter(default_state))
async def button_down_jacket(callback: CallbackQuery, state: FSMContext):
    try:
        user = callback.from_user.username
        logger.info(f"Пользователь {user} нажал на кнопку пуховиков")
        await bot.send_photo(
            chat_id=callback.message.chat.id,
            caption=LEXICON_RU["Ввести стоимость"],
            photo=photo_rate_1,
            parse_mode='MarkdownV2'
        )
        await bot.send_photo(
            chat_id=callback.message.chat.id,
            caption=LEXICON_RU["Выкуп"],
            photo=photo_rate_2,
            parse_mode='MarkdownV2',
            allow_sending_without_reply=True
        )
        await callback.answer(show_alert=True)
        await state.set_state(FSMDownJacket.rate_down_jacket)
    except:
        logger.critical("Ошибка в кнопке пуховиков ")


# Хендлер по цене пуховики
@router.message(StateFilter(FSMDownJacket.rate_down_jacket))
async def calculator_down_jacket(message: Message, state: FSMContext):
    try:
        user = message.from_user.username
        logger.info(f"Пользователь {user} посчитал цену пуховиков")
        try:
            text = float(message.text)
            value = await course_today()
            if value is not None:
                value_markup = text * value + 1200
                round_value = round(value_markup)
                formatted_num = "{}\\.{}".format(
                    int(value), int(value * 100) % 100)
                await message.answer(text=str(
                    f"""Итого *{round_value}* руб\. с учетом всех расходов до Пензы❤️\n\nДля информации\:\nСтоимость доставки составила\: *1200 рублей\! \(уже учтено в цене\)*\nКурс юаня *{formatted_num}*\nКатегория\: Пуховики🥼"""),
                    parse_mode='MarkdownV2',
                    reply_markup=update_calculator
                )
                await state.clear()
            else:
                await message.reply(text=LEXICON_RU["Данные о валюте"])
        except ValueError:
            await message.answer(text=LEXICON_RU["Стоимость в юанях"],
                                parse_mode='MarkdownV2')
    except:
        logger.critical("Ошибка в калькуляторе пуховиков ")


# Кнопка Одежды
@router.callback_query(F.data == 'button_clothes', StateFilter(default_state))
async def button_clothes(callback: CallbackQuery, state: FSMContext):
    try:
        user = callback.from_user.username
        logger.info(f"Пользователь {user} нажал на кнопку одежды")
        await bot.send_photo(
            chat_id=callback.message.chat.id,
            caption=LEXICON_RU["Ввести стоимость"],
            photo=photo_rate_1,
            parse_mode='MarkdownV2'
        )
        await bot.send_photo(
            chat_id=callback.message.chat.id,
            caption=LEXICON_RU["Выкуп"],
            photo=photo_rate_2,
            parse_mode='MarkdownV2',
            allow_sending_without_reply=True
        )
        await callback.answer(show_alert=True)
        await state.set_state(FSMClothes.rate_clothes)
    except:
        logger.critical("Ошибка в кнопке одежды")


# Хендлер по цене одежды
@router.message(StateFilter(FSMClothes.rate_clothes))
async def calculator_clothes(message: Message, state: FSMContext):
    try:
        user = message.from_user.username
        logger.info(f"Пользователь {user} посчитал цену одежды")
        try:
            text = float(message.text)
            value = await course_today()
            if value is not None:
                value_markup = text * value + 1000
                round_value = round(value_markup)
                formatted_num = "{}\\.{}".format(
                    int(value), int(value * 100) % 100)
                await message.answer(text=str(
                    f"""Итого *{round_value}* руб\. с учетом всех расходов до Пензы❤️\n\nДля информации\:\nСтоимость доставки составила\: *1000 рублей\! \(уже учтено в цене\)*\nКурс юаня *{formatted_num}*\nКатегория\: Одежда🩳"""),
                    parse_mode='MarkdownV2',
                    reply_markup=update_calculator,
                )
                await state.clear()
            else:
                await message.reply(text=LEXICON_RU["Данные о валюте"])
        except ValueError:
            await message.answer(text=LEXICON_RU["Стоимость в юанях"],
                                parse_mode='MarkdownV2')
    except:
        logger.critical("Ошибка калькуляторе одежды")


# Кнопка Украшения/духи/ковры
@router.callback_query(F.data == 'button_care', StateFilter(default_state))
async def button_care(callback: CallbackQuery, state: FSMContext):
    try:
        user = callback.from_user.username
        logger.info(f"Пользователь {user} нажал на кнопку украшений")
        await bot.send_photo(
            chat_id=callback.message.chat.id,
            caption=LEXICON_RU["Ввести стоимость"],
            photo=photo_rate_1,
            parse_mode='MarkdownV2'
        )
        await bot.send_photo(
            chat_id=callback.message.chat.id,
            caption=LEXICON_RU["Выкуп"],
            photo=photo_rate_2,
            parse_mode='MarkdownV2',
            allow_sending_without_reply=True
        )
        await callback.answer(show_alert=True)
        await state.set_state(FSMCare.rate_сare)
    except:
        logger.critical("Ошибка кнопке украшений")


# Хендлер по цене Украшения/духи/ковры
@router.message(StateFilter(FSMCare.rate_сare))
async def calculator_rate_care(message: Message, state: FSMContext):
    try:
        user = message.from_user.username
        logger.info(f"Пользователь {user} посчитал цену украшений")
        try:
            text = float(message.text)
            value = await course_today()
            print(value)
            if value is not None:
                value_markup = text * value + 1000
                round_value = round(value_markup)
                formatted_num = "{}\\.{}".format(
                    int(value), int(value * 100) % 100)
                await message.answer(text=str(
                    f"""Итого *{round_value}* руб\. с учетом всех расходов до Пензы❤️\n\nДля информации\:\nСтоимость доставки составила\: *1000 рублей\! \(уже учтено в цене\)*\nКурс юаня *{formatted_num}*\nКатегория\: Украшения/духи/ковры💍"""),
                    parse_mode='MarkdownV2',
                    reply_markup=update_calculator,)
                await state.clear()
            else:
                await message.reply(text=LEXICON_RU["Данные о валюте"])
        except ValueError:
            await message.answer(text=LEXICON_RU["Стоимость в юанях"],
                            parse_mode='MarkdownV2')
    except:
        logger.critical("Ошибка калькуляторе украшений")


# Кнопка аксессуары
@router.callback_query(F.data == 'button_jewelry')
async def button_jewelry(callback: CallbackQuery, state: FSMContext):
    try:
        user = callback.from_user.username
        logger.info(f"Пользователь {user} зешел в кнопку украшений")
        await callback.message.edit_text(
            text=LEXICON_RU["Заказ аксессуаров"],
            parse_mode='MarkdownV2',
            reply_markup=update_calculator,)
        await callback.answer(show_alert=True)
    except:
        logger.critical("Ошибка кнопке аксессуары")
