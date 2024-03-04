from aiogram import Bot, Router, types
from config.config import settings
from src.lexicon.lexicon_ru import LEXICON_RU
from src.filters.filters import my_start_filter
from src.models.users.dao import add_user
from src.keyboards.keyboards import meny
from aiogram.types import URLInputFile


bot = Bot(token=settings.BOT_TOKEN)
router = Router()


@router.message(my_start_filter)
async def start(message: types.Message):
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    user_id = message.from_user.id
    await add_user(first_name, last_name, username, user_id)
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
