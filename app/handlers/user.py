import traceback
from aiogram import Router, types, F
from aiogram.types import CallbackQuery
from app.lexicon.lexicon_ru import LEXICON_RU
from app.filters.filters import my_start_filter
from app.models.order.dao import add_save_order
from app.models.users.dao import add_user
from app.keyboards.keyboards import meny, meny_admin, meny_order
from aiogram.fsm.context import FSMContext
from config.config import bot, logger, settings
from app.static.images import static


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
                photo=static.photo_url_start,
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
                photo=static.photo_url_start,
                caption=LEXICON_RU["/start"],
                parse_mode='MarkdownV2'
            )
            order = await add_save_order(user_id)
            print(order)
            if order:
                await message.answer(text=LEXICON_RU["Привет"],
                                    reply_markup=meny_order,
                                    parse_mode='MarkdownV2')
                await state.clear()
            else:
                await message.answer(text=LEXICON_RU["Привет"],
                                    reply_markup=meny,
                                    parse_mode='MarkdownV2')
                await state.clear()
    except Exception as e:
        logger.critical('Ошибка в старте проекта', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'старта проекта:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


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
            order = await add_save_order(user_id)
            if order:
                await callback.message.edit_text(text=LEXICON_RU["Привет"],
                                    reply_markup=meny_order,
                                    parse_mode='MarkdownV2')
                await state.clear()
            else:
                await callback.message.edit_text(text=LEXICON_RU["Привет"],
                                    reply_markup=meny,
                                    parse_mode='MarkdownV2')
                await state.clear()
    except Exception as e:
        logger.critical('Ошибка в кнопке меню всплывающая', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'кнопке меню всплывающая:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


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
            order = await add_save_order(user_id)
            if order:
                await bot.send_message(
                    chat_id=user_id,
                    text=LEXICON_RU["Привет"],
                    reply_markup=meny_order,
                    parse_mode='MarkdownV2')
                await state.clear()
            else:
                await bot.send_message(
                    chat_id=user_id,
                    text=LEXICON_RU["Привет"],
                    reply_markup=meny,
                    parse_mode='MarkdownV2')
                await state.clear()
    except Exception as e:
        logger.critical('Ошибка в кнопке меню основная', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'кнопке меню основная:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)
