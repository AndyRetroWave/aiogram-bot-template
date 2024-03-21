import logging
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from app.lexicon.lexicon_ru import LEXICON_RU
from app.keyboards.keyboards import order, update_calculator, meny
from app.api.response_rate import formatted_num
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from app.models.course.dao import course_today
from app.states.states import FSMCare, FSMClothes, FSMSneakers, FSMDownJacket
from aiogram.fsm.state import default_state
from config.config import bot, logger

router = Router()

# Кнопка заказ
@router.callback_query(F.data == 'botton_orders')
async def category_botton(callback: CallbackQuery):
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
