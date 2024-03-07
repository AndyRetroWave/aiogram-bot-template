import logging
from aiogram import Bot, Router, types
from config.config import settings
from app.lexicon.lexicon_ru import LEXICON_RU
from app.filters.filters import my_start_filter
from app.models.users.dao import add_user
from app.keyboards.keyboards import meny
from aiogram.types import URLInputFile
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext


bot = Bot(token=settings.BOT_TOKEN)
router = Router()
logger = logging.getLogger(__name__)

# Старт нашего проекта


@router.message(my_start_filter)
async def start(message: types.Message, state: FSMContext):
    # first_name = message.from_user.first_name
    # last_name = message.from_user.last_name
    # username = message.from_user.username
    # user_id = message.from_user.id
    # logger.debug(f'Пользователь {first_name } {last_name} Вошёл в меню')
    # await add_user(first_name, last_name, username, user_id)
    photo_url = 'https://bytepix.ru/ib/Bqs4K601d2.png'
    photo = URLInputFile(photo_url)
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=photo,
        caption=LEXICON_RU["/start"],
        parse_mode='MarkdownV2'
    )
    await message.answer(text=LEXICON_RU["Привет"],
                        reply_markup=meny,
                        parse_mode='MarkdownV2')
    await state.clear()
    # logger.debug(f'Пользователь {first_name } {last_name} вышел из меню')
