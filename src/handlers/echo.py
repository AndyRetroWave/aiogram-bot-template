from aiogram import Router
from aiogram.types import Message

from src.models.users.router import add_user


router: Router = Router()


# @router.message()
# async def process_any_message(message: Message):
#     await message.reply(text=message.text)

@router.message()
async def handle_message(message: Message):
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    await add_user(first_name, last_name, username)
    await message.reply('Thanks for your message!')