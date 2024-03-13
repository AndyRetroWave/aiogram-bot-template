from aiogram import Router, types
from app.lexicon.lexicon_ru import LEXICON_RU
from app.filters.filters import my_start_filter
from app.models.users.dao import add_user
from app.keyboards.keyboards import meny, meny_admin
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from config.config import bot, logger, settings
from app.static.images import photo_start


router = Router()


# Старт нашего проекта
@router.message(my_start_filter)
async def start(message: types.Message, state: FSMContext):
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    user_id = message.from_user.id
    logger.debug(f'Пользователь {first_name } - {last_name} - Вошёл в меню')
    await add_user(first_name, last_name, username, user_id)
    if message.from_user.id == settings.ADMIN_ID:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo_start,
            caption=LEXICON_RU["/start"],
            parse_mode='MarkdownV2'
        )
        await message.answer(text=LEXICON_RU["Привет"],
                            reply_markup=meny_admin,
                            parse_mode='MarkdownV2')
        await state.clear()
    else:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo_start,
            caption=LEXICON_RU["/start"],
            parse_mode='MarkdownV2'
        )
        await message.answer(text=LEXICON_RU["Привет"],
                            reply_markup=meny,
                            parse_mode='MarkdownV2')
        await state.clear()
    logger.debug(f'Пользователь {first_name } - {last_name} - вышел из меню')
