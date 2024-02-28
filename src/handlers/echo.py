from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from src.models.users.dao import add_user
from src.keyboards.keyboards import keyboard

router: Router = Router()

@router.message(Command(commands=["start"]))
async def start(message: Message):
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    user_id = message.from_user.id
    await add_user(first_name, last_name, username, user_id)
    await message.reply(
        text='Спасибо мы тебя внесли в список пидарасов, отправим этот список презеденту',
        reply_markup=keyboard
    )

@router.message()
async def echo_massege(message: Message):
    await message.reply(text=message.text)
