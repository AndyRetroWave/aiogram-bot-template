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
@router.callback_query(F.data == 'botton_orders')
async def category_botton(callback: CallbackQuery):
    logger.debug('Вошли в оформления заказа')
    await callback.message.edit_text(
        text=LEXICON_RU["Категория"],
        reply_markup=calculator_rate,
        parse_mode='MarkdownV2'
    )
    await callback.answer(show_alert=True)
