from aiogram import Bot, Router, types
from aiogram.types import Message, InputFile
from config.config import settings
from src.filters.filters import *
from src.models.users.dao import add_user
from src.keyboards.keyboards import meny, calculator_rate
from aiogram.types import URLInputFile

from aiogram import F
from aiogram.types import CallbackQuery


bot = Bot(token=settings.BOT_TOKEN)
router = Router()

@router.message(my_start_filter)
async def start(message: types.Message):
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    user_id = message.from_user.id
    await add_user(first_name, last_name, username, user_id)
    photo_url = 'https://bytepix.ru/ib/Bqs4K601d2.png'  # URL-адрес вашей фотографии
    photo = URLInputFile(photo_url)  # создаем объект InputFile из URL-адреса фотографии
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=photo,
        caption="Приветствую тут ты можешь заказать товары из китая!",
    )
    await message.answer(text="Посчитай цену в калькуляторе!",
                        reply_markup=meny)

@router.callback_query(F.data == 'big_button_1_pressed')
async def process_button_1_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Выбери категория товара',
        reply_markup=calculator_rate 
    )
    await callback.answer(show_alert=True)


@router.callback_query(F.data == 'Кросовки')
async def process_button_1_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Введи стоимость товара в юанях",
        reply_markup=None
    )
    await callback.answer(show_alert=True)
