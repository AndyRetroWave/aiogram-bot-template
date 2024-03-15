import logging
import os
from aiogram import F, types, Router
from aiogram.types import CallbackQuery, Message
from app.filters.filters import photo, file
from app.lexicon.lexicon_ru import LEXICON_RU
from app.keyboards.keyboards import calculator_update, frequent_questions, meny_admin, menu_rare, android
from app.models.course.dao import add_course, course_today
from config.config import logger
from app.states.states import FSMCourse, FSMFile, FSMPhoto
from aiogram.fsm.state import default_state
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from config.config import bot
from aiogram.utils.media_group import MediaGroupBuilder

router = Router()


# Кнопка добовления курса юаня
@router.callback_query(F.data == 'add_course_botton', StateFilter(default_state))
async def add_course_yan(callback: CallbackQuery, state: FSMContext):
    logger.debug('Вошли в кнопку добавления курса юаня')
    value = await course_today()
    formatted_num = "{}\\.{}".format(
        int(value), int(value * 100) % 100)
    await callback.message.edit_text(
        text=f"""Привет хозяин\!\nВведи курс на сегодняшний день\n\n❗*ВНИМАНИЕ* надо добавлять курс с точкой\!\nНапример: 12\.34\n12,32 такое значение не принимаеться\!\n\nКурс на данный момент: *{formatted_num}* """,
        parse_mode='MarkdownV2',
    )
    await callback.answer(show_alert=True)
    await state.set_state(FSMCourse.course)
    logger.debug('Вышли из кнопки добавления курса юаня')


# Хендлер по добавлению курса юаня
@router.message(StateFilter(FSMCourse.course))
async def calculator_rate_value(message: Message, state: FSMContext):
    logger.debug('Вошли в хендлер добавления курса юаня')
    try:
        course = float(message.text)
        await add_course(course)
        await state.clear()
        await message.answer(
            text="Курс юаня успешно установлен",
            reply_markup=meny_admin)
    except ValueError:
        await message.answer(
            text="Введи пожалуйста курс числом а не словами")
        logger.debug('Не получилось добавить курс')
    logger.debug('Вышли из хендлера добавления курса юаня')

# Кнопка отзывы


@router.callback_query(F.data == 'button_feedback')
async def recall(callback: CallbackQuery):
    logger.debug('Вошли в отзывы')
    await callback.message.edit_text(
        text=LEXICON_RU["Отзывы"],
        reply_markup=calculator_update,
        parse_mode='MarkdownV2'
    )
    await callback.answer(show_alert=True)
    logger.debug('Вышли из отзывов')


# Кнопка инструкция
@router.callback_query(F.data == 'instruction')
async def instruction(callback: CallbackQuery):
    logger.debug('Вошли в инструкцию')
    await callback.message.edit_text(
        text=LEXICON_RU["Инструкция"],
        reply_markup=calculator_update,
        parse_mode='MarkdownV2'
    )
    await callback.answer(show_alert=True)
    logger.debug('Вышли из инструкции')


# Кнопка задать вопрос
@router.callback_query(F.data == 'question')
async def ask_a_question(callback: CallbackQuery):
    logger.debug('Вошли в вопрос')
    await callback.message.edit_text(
        text=LEXICON_RU["Вопрос"],
        reply_markup=calculator_update,
        parse_mode='MarkdownV2'
    )
    await callback.answer(show_alert=True)
    logger.debug('Вышли из вопроса')


# Кнопка курска юаня
@router.callback_query(F.data == 'button_rate')
async def course_yan(callback: CallbackQuery):
    logger.debug('Вошли в курс юаня')
    await callback.message.edit_text(
        text=LEXICON_RU["Курс юаня"],
        reply_markup=calculator_update,
        parse_mode='MarkdownV2'
    )
    await callback.answer(show_alert=True)
    logger.debug('Вышли из курс юаня')


# Кнопка скама
@router.callback_query(F.data == 'button_skam')
async def skam(callback: CallbackQuery):
    user_name = callback.from_user.first_name
    logger.debug(f'Пользователь {user_name} - вошел в скам')
    await callback.message.edit_text(
        text=LEXICON_RU["Скам"],
        reply_markup=calculator_update,
        parse_mode='MarkdownV2'
    )
    await callback.answer(show_alert=True)
    logger.debug(f'Пользователь {user_name} - вышел из скама')


# Кнопка ччастые вопросы
@router.callback_query(F.data == 'issue_botton')
async def issue(callback: CallbackQuery):
    user_name = callback.from_user.first_name
    logger.debug(f'Пользователь {user_name} - вошел в частые вопросы')
    await callback.message.edit_text(
        text=LEXICON_RU["Частые вопросы"],
        reply_markup=frequent_questions,
        parse_mode='MarkdownV2'
    )
    await callback.answer(show_alert=True)
    logger.debug(f'Пользователь {user_name} - вышел из частых вопросов')


# Кнопка скачивания POIZON
@router.callback_query(F.data == 'appendix_botton')
async def poizon(callback: CallbackQuery):
    user_name = callback.from_user.first_name
    logger.debug(f'Пользователь {user_name} - вошел в частые вопросы')
    media_group = MediaGroupBuilder()
    media_group.add_photo(
        media="AgACAgIAAxkBAAII1GX0MesrJHO8mL_H-QSrfc0RwXYKAAIH2DEbvlagS0qUe8WK0MttAQADAgADeAADNAQ")
    media_group.add_photo(
        media="AgACAgIAAxkBAAII1mX0MfLvXlMQEn75grUDSRHxkQ9kAAId2DEbvlagS23cyonH1o8pAQADAgADeAADNAQ")
    media_group.add_photo(
        media="AgACAgIAAxkBAAII2GX0MfbeifqYKj15dWWPK9jcmJdLAAIe2DEbvlagS6l_SugOyr5LAQADAgADeAADNAQ")
    media_group.add_photo(
        media="AgACAgIAAxkBAAII2mX0Mfxy_BIp2mTs7ldfX6XJvXbUAAIf2DEbvlagS57cStXrdazOAQADAgADeAADNAQ")
    media_group.add_photo(
        media="AgACAgIAAxkBAAII3GX0MgABBGw_2bmXv-zh15R1_ranaQACINgxG75WoEuVE2MQAAGt-PcBAAMCAAN4AAM0BA")
    media_group.add_photo(
        media="AgACAgIAAxkBAAII3mX0MgSY2VPJPKGK1TXdqgcvsLU9AAIh2DEbvlagS2skqmQ3bWjbAQADAgADeAADNAQ")
    media_group.add_photo(
        media="AgACAgIAAxkBAAII4GX0MglNa2FOOOgy1dVyHD7qTB-ZAAIi2DEbvlagS6uux6No-IYTAQADAgADeAADNAQ")
    media_group.add_photo(
        media="AgACAgIAAxkBAAII4mX0Mg2BrpzXQi6laXcKi43HfJyRAAIj2DEbvlagS7tH_qxWmIZpAQADAgADeAADNAQ")
    media_group.add_photo(
        media="AgACAgIAAxkBAAII5GX0MhE8xZRWYlksMlRjmhkGaQTKAAIk2DEbvlagS_HhVQeHkDiYAQADAgADeAADNAQ")
    await bot.send_media_group(chat_id=callback.message.chat.id, media=media_group.build())
    await bot.send_message(
        chat_id=callback.message.chat.id,
        text=LEXICON_RU["Скачивание"],
        reply_markup=android,
        parse_mode='MarkdownV2'
    )
    await callback.answer(show_alert=True)
    logger.debug(f'Пользователь {user_name} - вышел из частых вопросов')


# Кнопка по создателю
@router.callback_query(F.data == 'bot_botton')
async def create_bot(callback: CallbackQuery):
    logger.debug('Вошли в кнопки бота')
    await callback.message.edit_text(
        text=LEXICON_RU["Заказ бота"],
        reply_markup=calculator_update,
        parse_mode='MarkdownV2'
    )
    logger.debug('Вышли из кнопки бота')


# Хендлер по файлу POIZON
@router.callback_query(F.data == 'android_botton')
async def calculator_rate_value(callback: CallbackQuery):
    logger.debug('Вошли в хендлер добавления курса юаня')
    await bot.send_document(
        chat_id=callback.message.chat.id,
        document="BQACAgIAAxkBAAICNGXy96uCuCZvJeWjmC2ChhNSv5xUAAIcQAAC7xuYS1dZtAFjP5ErNAQ",
    )
    logger.debug('Не получилось добавить курс')
    logger.debug('Вышли из хендлера добавления курса юаня')


# # ехо файл
@router.message(file, StateFilter(default_state))
async def calculator_rate_value(message: Message, state: FSMContext):
    await message.answer(
        text="Пришли мне файл"
    )
    await state.set_state(FSMFile.file)
@router.message(FSMFile.file)
async def calculator_rate_value(message: Message, state: FSMContext):
    logger.debug('Вошли в хендлер добавления курса юаня')
    file_id = message.document.file_id
    await message.answer(
        text=file_id
    )


# # ехо фото
@router.message(photo, StateFilter(default_state))
async def calculator_rate_value(message: Message, state: FSMContext):
    await message.answer(
        text="Пришли мне фото"
    )
    await state.set_state(FSMPhoto.photo)
@router.message(FSMPhoto.photo)
async def calculator_rate_value(message: Message):
    logger.debug('Вошли в хендлер добавления курса юаня')
    # Get the file ID of the largest version of the photo
    file_id = message.photo[-1].file_id
    # Do something with the file ID, such as sending it to another user
    await message.answer(
        text=file_id
    )
    logger.debug('Вышли из хендлера добавления курса юаня')
