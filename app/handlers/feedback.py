import logging
from aiogram import F, types, Router
from aiogram.types import CallbackQuery, Message
from app.lexicon.lexicon_ru import LEXICON_RU
from app.keyboards.keyboards import calculator_update
from app.models.course.dao import add_course, course_today
from config.config import logger
from app.states.states import FSMCourse
from aiogram.fsm.state import default_state
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext


router = Router()


# Кнопка добовления курса юаня
@router.callback_query(F.data == 'add_course_botton', StateFilter(default_state))
async def add_course_yan(callback: CallbackQuery, state: FSMContext):
    logger.debug('Вошли в кнопку добавления курса юаня')
    # value = await course_today()
    # formatted_num = "{}\\.{}".format(
    #     int(value), int(value * 100) % 100)
    await callback.message.edit_text(
        text=f"""Привет хозяин\!\nВведи курс на сегодняшний день\n\n❗*ВНИМАНИЕ* надо добавлять курс с точкой\!\nНапример: 12\.34\n12,32 такое значение не принимаеться\!\n\nКурс на данный момент: """,
        parse_mode='MarkdownV2')
    await callback.answer(show_alert=True)
    await state.set_state(FSMCourse.course)
    logger.debug('Вышли из кнопки добавления курса юаня')


#Хендлер по добавлению курса юаня
@router.message(StateFilter(FSMCourse.course))
async def calculator_rate_value(message: Message, state: FSMContext):
    logger.debug('Вошли в хендлер добавления курса юаня')
    try:
        course = float(message.text)
        await add_course(course)
        await state.clear()
        await message.answer(
            text="Курс юаня успешно установлен")
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

