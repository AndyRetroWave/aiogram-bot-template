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
@router.callback_query(F.data == 'button_skam')
async def process_button_1_press(callback: CallbackQuery):
    logger.debug('Вошли в скам')
    await callback.message.edit_text(
        text=LEXICON_RU["Скам"],
        reply_markup=calculator_update,
        parse_mode='MarkdownV2'
    )
    await callback.answer(show_alert=True)
    logger.debug('Вышли из скама')