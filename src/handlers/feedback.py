import logging
from aiogram import F, types, Router, Bot
from aiogram.types import CallbackQuery
from src.lexicon.lexicon_ru import LEXICON_RU
from src.keyboards.keyboards import calculator_update
from config.config import settings

bot = Bot(token=settings.BOT_TOKEN)

router = Router()
logger = logging.getLogger(__name__)

# Кнопка курска юаня
@router.callback_query(F.data == 'button_feedback')
async def process_button_1_press(callback: CallbackQuery):
    logger.debug('Вошли в отзывы')
    await callback.message.edit_text(
        text=LEXICON_RU["Отзывы"],
        reply_markup=calculator_update,
        parse_mode='MarkdownV2'
    )
    await callback.answer(show_alert=True)
    logger.debug('Вышли из отзывов')


# Кнопка инструкция
@router.callback_query(F.data == 'instruction')
async def process_button_1_press(callback: CallbackQuery):
    logger.debug('Вошли в инструкцию')
    await callback.message.edit_text(
        text=LEXICON_RU["Инструкция"],
        reply_markup=calculator_update,
        parse_mode='MarkdownV2'
    )
    await callback.answer(show_alert=True)
    logger.debug('Вышли из инструкции')


# Кнопка задать вопрос
@router.callback_query(F.data == 'question')
async def process_button_1_press(callback: CallbackQuery):
    logger.debug('Вошли в вопрос')
    await callback.message.edit_text(
        text=LEXICON_RU["Вопрос"],
        reply_markup=calculator_update,
        parse_mode='MarkdownV2'
    )
    await callback.answer(show_alert=True)
    logger.debug('Вышли из вопроса')