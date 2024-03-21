from aiogram import Router, types, F
from aiogram.types import CallbackQuery
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
    try:
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        username = message.from_user.username
        user_id = message.from_user.id
        logger.info(f"Пользователь {username} стартовал в боте")
        await add_user(first_name, last_name, username, user_id)
        if message.from_user.id == settings.ADMIN_ID or message.from_user.id == settings.ADMIN_ID2:
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
    except:
        logger.critical("Ошибка в старте проекта")


# Кнопка меню всплывающая
@router.callback_query(F.data == 'menu_booton_basic')
async def start(callback: CallbackQuery, state: FSMContext):
    try: 
        first_name = callback.from_user.first_name
        last_name = callback.from_user.last_name
        username = callback.from_user.username
        user_id = callback.from_user.id
        logger.info(f'Пользователь {username} нажал на меню')
        await add_user(first_name, last_name, username, user_id)
        if callback.from_user.id == settings.ADMIN_ID or callback.from_user.id == settings.ADMIN_ID2:
            await callback.message.edit_text(
                text=LEXICON_RU["Привет"],
                reply_markup=meny_admin,
                parse_mode='MarkdownV2')
            await state.clear()
        else:
            await callback.message.edit_text(
                text=LEXICON_RU["Привет"],
                reply_markup=meny,
                parse_mode='MarkdownV2')
            await callback.answer(show_alert=True)
            await state.clear()
    except:
        logger.critical('Ошибка в кнопке меню')


# Кнопка меню оснв
@router.callback_query(F.data == 'menu_booton')
async def start(callback: CallbackQuery, state: FSMContext):
    try:
        first_name = callback.from_user.first_name
        last_name = callback.from_user.last_name
        username = callback.from_user.username
        user_id = callback.from_user.id
        logger.info(f'Пользователь {username} нажал на меню')
        await add_user(first_name, last_name, username, user_id)
        if callback.from_user.id == settings.ADMIN_ID or callback.from_user.id == settings.ADMIN_ID2:
            await bot.send_message(
                chat_id=callback.message.chat.id,
                text=LEXICON_RU["Привет"],
                reply_markup=meny_admin,
                parse_mode='MarkdownV2')
            await state.clear()
        else:
            await bot.send_message(
                chat_id=callback.message.chat.id,
                text=LEXICON_RU["Привет"],
                reply_markup=meny,
                parse_mode='MarkdownV2')
            await callback.answer(show_alert=True)
            await state.clear()
    except:
        logger.critical("Ошибка в кнопке меню")
