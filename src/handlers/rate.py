import logging
from aiogram import F, types, Router, Bot
from aiogram.types import Message, CallbackQuery
from src.lexicon.lexicon_ru import LEXICON_RU
from src.keyboards.keyboards import calculator_rate, update_calculator, meny
from src.api.response_rate import value, formatted_num
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.types import URLInputFile
from config.config import settings


bot = Bot(token=settings.BOT_TOKEN)

router = Router()
logger = logging.getLogger(__name__)


# Состояние кросовок
class FSMSneakers(StatesGroup):
    rate_sneakers = State()


# Состояние одежды
class FSMClothes(StatesGroup):
    rate_clothes = State()


# Состояние уход
class FSMCare(StatesGroup):
    rate_сare = State()


# Кнопка категория
@router.callback_query(F.data == 'big_button_1_pressed')
async def process_button_1_press(callback: CallbackQuery):
    logger.debug('Вошли в кнопку категория')
    await callback.message.edit_text(
        text=LEXICON_RU["Категория"],
        reply_markup=calculator_rate,
        parse_mode='MarkdownV2'
    )
    await callback.answer(show_alert=True)
    logger.debug('Вышли из кнопки категория')


# Кнопка повтора
@router.callback_query(F.data == 'big_button_1_pressed')
async def process_button_1_press(callback: CallbackQuery):
    logger.debug('Вошли в кнопку повтора')
    await callback.message.edit_text(
        text=LEXICON_RU["Категория"],
        reply_markup=calculator_rate,
        parse_mode='MarkdownV2'
    )
    await callback.answer(show_alert=True)
    logger.debug('Вышли из кнопки повтора')


# Кнопка кросовка
@router.callback_query(F.data == 'button_snecers', StateFilter(default_state))
async def process_button_1_press(callback: CallbackQuery, state: FSMContext):
    logger.debug('Вошли в кнопку кросовки')
    photo_url_1 = 'https://bytepix.ru/ib/OghwDLiWhu.jpg'
    photo_1 = URLInputFile(photo_url_1)
    await bot.send_photo(
        chat_id=callback.message.chat.id,
        caption=LEXICON_RU["Ввести стоимость"],
        photo=photo_1,
        parse_mode='MarkdownV2'
    )
    photo_url_2 = 'https://bytepix.ru/ib/AHeko931wt.jpg'
    photo_2 = URLInputFile(photo_url_2)
    await bot.send_photo(
        chat_id=callback.message.chat.id,
        caption=LEXICON_RU["Выкуп"],
        photo=photo_2,
        parse_mode='MarkdownV2',
        allow_sending_without_reply=True
    )
    await callback.answer(show_alert=True)
    await state.set_state(FSMSneakers.rate_sneakers)
    logger.debug('Вышли из кнопки кросовки')


# Хендлер по цене кросовок
@router.message(StateFilter(FSMSneakers.rate_sneakers))
async def calculator_rate_value(message: Message, state: FSMContext):
    logger.debug('Вошли в ценовой-хэндлер кросовок')
    try:
        text = float(message.text)
        if value is not None:
            value_markup = text * (value + value * 0.1) + 1200
            round_value = round(value_markup)
            await message.answer(text=str(
                f"""Итого *{round_value}* руб\. с учетом всех расходов до Пензы❤️\n\nДля информации\:\nСтоимость доставки составила\: *1200 рублей\! \(уже учтено в цене\)*\nКурс юаня *{formatted_num}*\nКатегория\: Кросовки👟"""),
                parse_mode='MarkdownV2',
                reply_markup=update_calculator
            )
            await state.clear()
        else:
            await message.reply(text="Извините, не удалось получить данные о валюте")
    except ValueError:
        await message.answer(text="Пожалуйста, введите стоимость в *Юанях*\.", parse_mode='MarkdownV2')
    logger.debug('Вышли из ценового-хэндлера кросовок')


# Кнопка Одежды
@router.callback_query(F.data == 'button_clothes', StateFilter(default_state))
async def process_button_1_press(callback: CallbackQuery, state: FSMContext):
    logger.debug('Вошли в кнопку кросовки')
    photo_url_1 = 'https://bytepix.ru/ib/OghwDLiWhu.jpg'
    photo_1 = URLInputFile(photo_url_1)
    await bot.send_photo(
        chat_id=callback.message.chat.id,
        caption=LEXICON_RU["Ввести стоимость"],
        photo=photo_1,
        parse_mode='MarkdownV2'
    )
    photo_url_2 = 'https://bytepix.ru/ib/AHeko931wt.jpg'
    photo_2 = URLInputFile(photo_url_2)
    await bot.send_photo(
        chat_id=callback.message.chat.id,
        caption=LEXICON_RU["Выкуп"],
        photo=photo_2,
        parse_mode='MarkdownV2',
        allow_sending_without_reply=True
    )
    await callback.answer(show_alert=True)
    await state.set_state(FSMClothes.rate_clothes)
    logger.debug('Вышли из кнопки кросовки')


# Хендлер по цене одежды
@router.message(StateFilter(FSMClothes.rate_clothes))
async def calculator_rate_value(message: Message, state: FSMContext):
    logger.debug('Вошли в ценовой-хэндлер одежды')
    try:
        text = float(message.text)
        if value is not None:
            value_markup = text * (value + value * 0.1) + 1000
            round_value = round(value_markup)
            await message.answer(text=str(
                f"""Итого *{round_value}* руб\. с учетом всех расходов до Пензы❤️\n\nДля информации\:\nСтоимость доставки составила\: *1000 рублей\! \(уже учтено в цене\)*\nКурс юаня *{formatted_num}*\nКатегория\: Одежда🩳"""),
                parse_mode='MarkdownV2',
                reply_markup=update_calculator,
            )
            await state.clear()
        else:
            await message.reply(text="Извините, не удалось получить данные о валюте")
    except ValueError:
        await message.answer(text="Пожалуйста, введите стоимость в *Юанях*\.", parse_mode='MarkdownV2')
    logger.debug('Вышли из ценового-хэндлера одежды')


# Кнопка Уход
@router.callback_query(F.data == 'button_care', StateFilter(default_state))
async def process_button_1_press(callback: CallbackQuery, state: FSMContext):
    logger.debug('Вошли в кнопку уход')
    photo_url_1 = 'https://bytepix.ru/ib/OghwDLiWhu.jpg'
    photo_1 = URLInputFile(photo_url_1)
    await bot.send_photo(
        chat_id=callback.message.chat.id,
        caption=LEXICON_RU["Ввести стоимость"],
        photo=photo_1,
        parse_mode='MarkdownV2'
    )
    photo_url_2 = 'https://bytepix.ru/ib/AHeko931wt.jpg'
    photo_2 = URLInputFile(photo_url_2)
    await bot.send_photo(
        chat_id=callback.message.chat.id,
        caption=LEXICON_RU["Выкуп"],
        photo=photo_2,
        parse_mode='MarkdownV2',
        allow_sending_without_reply=True
    )
    await callback.answer(show_alert=True)
    await state.set_state(FSMCare.rate_сare)
    logger.debug('Вышли из кнопки уход')


# Хендлер по цене уход
@router.message(StateFilter(FSMCare.rate_сare))
async def calculator_rate_value(message: Message, state: FSMContext):
    logger.debug('Вошли в ценовой-хэндлер уход')
    try:
        text = float(message.text)
        if value is not None:
            value_markup = text * (value + value * 0.1) + 700
            round_value = round(value_markup)
            await message.answer(text=str(
                f"""Итого *{round_value}* руб\. с учетом всех расходов до Пензы❤️\n\nДля информации\:\nСтоимость доставки составила\: *700 рублей\! \(уже учтено в цене\)*\nКурс юаня *{formatted_num}*\nКатегория\: Одежда🩳"""),
                parse_mode='MarkdownV2',
                reply_markup=update_calculator,)
            await state.clear()
        else:
            await message.reply(text="Извините, не удалось получить данные о валюте")
    except ValueError:
        await message.answer(text="Пожалуйста, введите стоимость в *Юанях*\.", parse_mode='MarkdownV2')
    logger.debug('Вышли из ценового-хэндлера уход')
