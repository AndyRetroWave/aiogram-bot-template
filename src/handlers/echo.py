from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from src.models.users.dao import add_user


router: Router = Router()

@router.message(Command(commands=["start"]))
async def handle_message(message: Message):
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    user_id = message.from_user.id
    await add_user(first_name, last_name, username, user_id)
    await message.reply('Thanks for your message!')

@router.message()
async def process_any_message(message: Message):
    await message.reply(text=message.text)
