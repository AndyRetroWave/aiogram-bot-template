import logging
import traceback
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from app.lexicon.lexicon_ru import LEXICON_RU
from app.keyboards.keyboards import calculator_rate, update_calculator, meny
from app.api.response_rate import formatted_num
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from app.models.course.dao import course_today
from app.states.states import FSMCare, FSMClothes, FSMSneakers, FSMDownJacket
from app.static.images import static
from aiogram.fsm.state import default_state
from config.config import settings, bot, logger

router = Router()


# Кнопка категория
@router.callback_query(F.data == 'big_button_1_pressed')
async def category_botton(callback: CallbackQuery):
    try:
        await callback.message.edit_text(
            text=LEXICON_RU["Категория"],
            reply_markup=calculator_rate,
            parse_mode='MarkdownV2'
        )
        await callback.answer(show_alert=True)
    except Exception as e:
        logger.critical('Ошибка в кнопке категория для калькулятара', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'кнопке категория для калькулятара:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


# Кнопка повтора
@router.callback_query(F.data == 'big_button_1_pressed')
async def repetition_buttons(callback: CallbackQuery):
    try:
        await callback.message.edit_text(
            text=LEXICON_RU["Категория"],
            reply_markup=calculator_rate,
            parse_mode='MarkdownV2'
        )
        await callback.answer(show_alert=True)
    except Exception as e:
        logger.critical('Ошибка в кнопке повтора для калькулятара', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'кнопке повтора для калькулятара:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


# Кнопка кросовка
@router.callback_query(F.data == 'button_snecers', StateFilter(default_state))
async def sneaks_button(callback: CallbackQuery, state: FSMContext):
    try:
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
        await state.set_state(FSMSneakers.rate_sneakers)
    except Exception as e:
        logger.critical('Ошибка в кнопке кросовка в калькуляторе', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'кнопке кросовка в калькуляторе:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


# Хендлер по цене кросовок
@router.message(StateFilter(FSMSneakers.rate_sneakers))
async def calculator_rate_value(message: Message, state: FSMContext):
    try:
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
    except Exception as e:
        logger.critical('Ошибка в хендлере кросовок в калькулятореа', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'хендлере кросовок в калькуляторе:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


# Кнопка пуховики
@router.callback_query(F.data == 'button_down_jacket', StateFilter(default_state))
async def button_down_jacket(callback: CallbackQuery, state: FSMContext):
    try:
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
        await state.set_state(FSMDownJacket.rate_down_jacket)
    except Exception as e:
        logger.critical('Ошибка в кнопке пуховики в калькуляторе', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'кнопке пуховики в калькуляторе:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


# Хендлер по цене пуховики
@router.message(StateFilter(FSMDownJacket.rate_down_jacket))
async def calculator_down_jacket(message: Message, state: FSMContext):
    try:
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
    except Exception as e:
        logger.critical('Ошибка в хендлере цены пуховиков в калькуляторе', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'хендлере цены пуховиков в калькуляторе:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


# Кнопка Одежды
@router.callback_query(F.data == 'button_clothes', StateFilter(default_state))
async def button_clothes(callback: CallbackQuery, state: FSMContext):
    try:
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
        await state.set_state(FSMClothes.rate_clothes)
    except Exception as e:
        logger.critical('Ошибка в кнопке одежды для калькулятора', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'кнопке одежды для калькулятора:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)



# Хендлер по цене одежды
@router.message(StateFilter(FSMClothes.rate_clothes))
async def calculator_clothes(message: Message, state: FSMContext):
    try:
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
    except Exception as e:
        logger.critical('Ошибка хендлере одежды для калькулятора', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'хендлере одежды для калькулятора:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)

# Кнопка Украшения/духи/ковры
@router.callback_query(F.data == 'button_care', StateFilter(default_state))
async def button_care(callback: CallbackQuery, state: FSMContext):
    try:
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
        await state.set_state(FSMCare.rate_сare)
    except Exception as e:
        logger.critical('Ошибка кнопке украшений для калькулятора', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'кнопке украшений для калькулятора:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)

# Хендлер по цене Украшения/духи/ковры
@router.message(StateFilter(FSMCare.rate_сare))
async def calculator_rate_care(message: Message, state: FSMContext):
    try:
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
    except Exception as e:
        logger.critical('Ошибка кнопке украшений для калькулятора', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'кнопке украшений для калькулятора:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)



# Кнопка аксессуары
@router.callback_query(F.data == 'button_jewelry')
async def button_jewelry(callback: CallbackQuery, state: FSMContext):
    try:

        await callback.message.edit_text(
            text=LEXICON_RU["Заказ аксессуаров"],
            parse_mode='MarkdownV2',
            reply_markup=update_calculator,)
        await callback.answer(show_alert=True)
    except Exception as e:
        logger.critical('Ошибка кнопке аксессуары для калькулятора', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'кнопке аксессуары для калькулятора:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)
