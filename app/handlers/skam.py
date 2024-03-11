import logging
from aiogram import F, types, Router, Bot
from aiogram.types import CallbackQuery, Message
from app.lexicon.lexicon_ru import LEXICON_RU
from app.keyboards.keyboards import calculator_update
from config.config import settings

bot = Bot(token=settings.BOT_TOKEN)

router = Router()
logger = logging.getLogger(__name__)

# Кнопка курска юаня


@router.callback_query(F.data == 'button_skam')
async def process_button_1_press(callback: CallbackQuery):
    user_name = callback.from_user.first_name
    logger.debug(f'Пользователь {user_name} вошел в скам')
    await callback.message.edit_text(
        text=LEXICON_RU["Скам"],
        reply_markup=calculator_update,
        parse_mode='MarkdownV2'
    )
    await callback.answer(show_alert=True)
    logger.debug(f'Пользователь {user_name} вышел из скама')