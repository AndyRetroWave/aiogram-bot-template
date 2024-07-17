import asyncio
import traceback
from aiogram import F, types, Router
from aiogram.types import CallbackQuery, Message
from app.dependence.dependence import logger_error_critical_send_message_admin
from app.filters.filters import photo, file
from app.lexicon.lexicon_ru import LEXICON_RU
from app.keyboards.keyboards import calculator_update, menu_one
from app.models.course.dao import course_today
from config.config import settings, logger
from app.states.states import FSMFile, FSMPhoto
from aiogram.fsm.state import default_state
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from config.config import bot
from app.static.images import static

router = Router()


# Кнопка отзывы
@router.callback_query(F.data == 'button_feedback')
async def recall(callback: CallbackQuery):
    try:
        await callback.answer(show_alert=True)
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Кнопка инструкция
@router.callback_query(F.data == 'instruction')
async def instruction(callback: CallbackQuery):
    try:
        await bot.send_video(
            chat_id=callback.message.chat.id,
            video=static.video,
            reply_markup=menu_one
        )
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Кнопка курска юаня
@router.callback_query(F.data == 'button_rate')
async def course_yan(callback: CallbackQuery):
    try:
        value = await course_today()
        formatted_num = "{}\\.{}".format(
            int(value), int(value * 100) % 100)
        logger.debug('Вошли в курс юаня')
        await callback.message.edit_text(
            text=LEXICON_RU['Курс юаня'].format(formatted_num),
            reply_markup=calculator_update,
            parse_mode='MarkdownV2',
            disable_web_page_preview=True
        )
        await callback.answer(show_alert=True)
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Кнопка по создателю
@router.callback_query(F.data == 'bot_botton')
async def create_bot(callback: CallbackQuery):
    try:
        user = callback.from_user.username
        await callback.message.edit_text(
            text=LEXICON_RU["Заказ бота"],
            reply_markup=calculator_update,
            parse_mode='MarkdownV2'
        )
        await bot.send_message(
            chat_id=settings.ADMIN_ID2,
            text=f"Кобанчик, тобой поинтересовался этот [челик](https://t.me/{user})\!",
            parse_mode='MarkdownV2')
    except:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Кнопка по вопросу
@router.callback_query(F.data == 'question_client_botton')
async def create_bot(callback: CallbackQuery):
    try:
        await callback.message.edit_text(
            text=LEXICON_RU["Вопрос"],
            reply_markup=calculator_update,
            parse_mode='MarkdownV2'
        )
    except:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# # ехо файл
@router.message(file, StateFilter(default_state))
async def echo_file(message: Message, state: FSMContext):
    await message.answer(
        text="Пришли мне файл"
    )
    await state.set_state(FSMFile.file)


# файл id
@router.message(FSMFile.file)
async def file_id(message: Message, state: FSMContext):
    try:
        file_id = message.document.file_id
        await message.answer(
            text=file_id
        )
    except:
        file_id = message.video.file_id
        await message.answer(
            text=file_id
        )


# # ехо фото
@router.message(photo, StateFilter(default_state))
async def echo_photo(message: Message, state: FSMContext):
    await message.answer(
        text="Пришли мне фото"
    )
    await state.set_state(FSMPhoto.photo)


# фото id
@router.message(FSMPhoto.photo)
async def photo_id(message: Message):
    file_id = message.photo[-1].file_id
    await message.answer(
        text=file_id
    )
