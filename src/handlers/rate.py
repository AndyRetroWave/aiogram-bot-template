import logging
from aiogram import F, types, Router
from aiogram.types import Message, CallbackQuery
from src.filters.filters import *
from src.keyboards.keyboards import upgrate_rate, calculator_rate
from src.api.response_rate import value
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

router = Router()
logger = logging.getLogger(__name__)


class FSMneakers(StatesGroup):
    rate_steakers = State()   


@router.callback_query(F.data == 'big_button_1_pressed')
async def process_button_1_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Выбери категория товара',
        reply_markup=calculator_rate 
    )
    await callback.answer(show_alert=True)


@router.callback_query(F.data == 'Кросовки', StateFilter(default_state))
async def process_button_1_press(callback: CallbackQuery, state: FSMContext):
    logger.debug('Вошли в кнопку кросовки')
    await callback.message.edit_text(
        text="Введи стоимость товара в юанях",
        reply_markup=None
    )
    await callback.answer(show_alert=True)
    await state.set_state(FSMneakers.rate_steakers)
    logger.debug('Вышли из кнопки кросовки')


@router.message(StateFilter(FSMneakers.rate_steakers))
async def calculator_rate_value(message: Message, state: FSMContext):
    logger.debug('Вошли в ценовой-хэндлер')
    try:
        text = float(message.text)
        if value is not None:
            value_markup = text * (value + value * 0.2) + 1200
            round_value = round(value_markup)
            await message.answer(text=str(
            f"""Стоимость данного товара будет составлять {round_value} рублей
            """),
            )
            await state.clear()
        else:
            await message.reply(text="Извините, не удалось получить данные о валюте")
    except ValueError:
        await message.reply(text="Пожалуйста, введите стоимость в Юанях.")
    logger.debug('Вышли из ценового-хэндлера')


