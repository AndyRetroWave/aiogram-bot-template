import logging
import traceback
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from app.lexicon.lexicon_ru import LEXICON_RU
from app.keyboards.keyboards import next, next_and_poizon, menu_one, android_poizon
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from app.states.states import FSMGuide
from aiogram.fsm.state import default_state
from config.config import settings, bot, logger
from aiogram.utils.media_group import MediaGroupBuilder
from app.static.images import static
router = Router()


# Кнопка Гайда основа
@router.callback_query(F.data == 'button_guide', StateFilter(default_state))
async def guide_poizon_1(callback: CallbackQuery, state: FSMContext):
    try:
        user = callback.from_user.username
        logger.info(f"Пользователь {user} нажал на кнопку гайд")
        await callback.message.edit_text(
            text=LEXICON_RU["Гайд по пойзон"],
            reply_markup=next,
            parse_mode='MarkdownV2'
        )
        await state.set_state(FSMGuide.install_1)
        await callback.answer(show_alert=True)
    except Exception as e:
        logger.critical(
            'Ошибка кнопке гайда', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'кнопке гайда:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


# Гайд скачивания POIZON
@router.callback_query(F.data == 'button_next', StateFilter(FSMGuide.install_1))
async def poizon(callback: CallbackQuery, state: FSMContext):
    try:
        user = callback.from_user.username
        logger.info(f"Пользователь {user} зашел в гайд скачивания POIZON")
        media_group = MediaGroupBuilder()
        media_group.add_photo(
            media=static.poizon_1)
        media_group.add_photo(
            media=static.poizon_2)
        media_group.add_photo(
            media=static.poizon_3)
        media_group.add_photo(
            media=static.poizon_4)
        media_group.add_photo(
            media=static.poizon_5)
        media_group.add_photo(
            media=static.poizon_6)
        media_group.add_photo(
            media=static.poizon_7)
        media_group.add_photo(
            media=static.poizon_8)
        media_group.add_photo(
            media=static.poizon_9)
        await bot.send_media_group(chat_id=callback.message.chat.id, media=media_group.build())
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=LEXICON_RU["Скачивание"],
            reply_markup=android_poizon,
            parse_mode='MarkdownV2'
        )
        await callback.answer(show_alert=True)
        await state.set_state(FSMGuide.install_2)
    except Exception as e:
        logger.critical(
            'Ошибка гайде по скачиванию приложения', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'гайде по скачиванию приложения:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)

# Хендлер по файлу POIZON
@router.callback_query(F.data == 'android_poizon_botton')
async def calculator_rate_value(callback: CallbackQuery):
    try:
        user = callback.from_user.username
        logger.info(f"Пользователь {user} скачал файл POIZON")
        await bot.send_document(
            chat_id=callback.message.chat.id,
            document=static.file_1,
        )
    except Exception as e:
        logger.critical(
            'Ошибка кнопке далее(Регистрация в пойзон)', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'кнопке далее(Регистрация в пойзон):\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)

# Кнопка далее(Регистрация в пойзон)
@router.callback_query(F.data == 'button_next', StateFilter(FSMGuide.install_2))
async def guide_poizon_1(callback: CallbackQuery, state: FSMContext):
    try:
        user = callback.from_user.username
        logger.info(f"Пользователь {user} в гайде регистрации")
        await bot.send_photo(
            chat_id=callback.message.chat.id,
            photo=static.register_guide,
            caption=LEXICON_RU["Регистрация пойзон"],
            reply_markup=next,
            parse_mode='MarkdownV2'
        )
        await state.set_state(FSMGuide.install_3)
        await callback.answer(show_alert=True)
    except Exception as e:
        logger.critical(
            'Ошибка кнопке далее(Регистрация в пойзон)', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'кнопке далее(Регистрация в пойзон):\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


# Кнопка далее 2(Регистрация в пойзон)
@router.callback_query(F.data == 'button_next', StateFilter(FSMGuide.install_3))
async def guide_poizon_2(callback: CallbackQuery, state: FSMContext):
    try:
        user = callback.from_user.username
        logger.info(f"Пользователь {user} в гайде регистрации 2")
        media_group = MediaGroupBuilder()
        media_group.add_photo(
            media=static.register_guide_1)
        media_group.add_photo(
            media=static.register_guide_2)
        media_group.add_photo(
            media=static.register_guide_3)
        await bot.send_media_group(
            chat_id=callback.message.chat.id,
            media=media_group.build())
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=LEXICON_RU["Регистрация пойзон 2"],
            reply_markup=next,
            parse_mode='MarkdownV2'
        )
        await state.set_state(FSMGuide.search_1)
        await callback.answer(show_alert=True)
    except Exception as e:
        logger.critical(
            'Ошибка кнопке далее 2(Регистрация в пойзон)', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'кнопке далее 2(Регистрация в пойзон):\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


# Кнопка далее 3(Поиск модели)
@router.callback_query(F.data == 'button_next', StateFilter(FSMGuide.search_1))
async def guide_poizon_3(callback: CallbackQuery, state: FSMContext):
    try:
        user = callback.from_user.username
        logger.info(f"Пользователь {user} в гайде поиска модели")
        media_group = MediaGroupBuilder()
        media_group.add_photo(
            media=static.search_guide_1)
        media_group.add_photo(
            media=static.search_guide_2)
        media_group.add_photo(
            media=static.search_guide_3)
        media_group.add_photo(
            media=static.search_guide_4)
        media_group.add_photo(
            media=static.search_guide_5)
        await bot.send_media_group(
            chat_id=callback.message.chat.id,
            media=media_group.build())
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=LEXICON_RU["Как сделать заказ"],
            reply_markup=next,
            parse_mode='MarkdownV2'
        )
        await state.set_state(FSMGuide.size_1)
        await callback.answer(show_alert=True)
    except Exception as e:
        logger.critical(
            'Ошибка кнопке далее 3(Поиск модели)', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'кнопке далее 3(Поиск модели):\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


# Кнопка далее 4(Как подобрать размер обуви и одежды)
@router.callback_query(F.data == 'button_next', StateFilter(FSMGuide.size_1))
async def guide_poizon_4(callback: CallbackQuery, state: FSMContext):
    try:
        user = callback.from_user.username
        logger.info(f"Пользователь {user} в гайде подбора размера")
        media_group = MediaGroupBuilder()
        media_group.add_photo(
            media=static.size_guide_1)
        media_group.add_photo(
            media=static.size_guide_2)
        media_group.add_photo(
            media=static.size_guide_3)
        await bot.send_media_group(
            chat_id=callback.message.chat.id,
            media=media_group.build())
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=LEXICON_RU["Как подобрать размер"],
            reply_markup=next,
            parse_mode='MarkdownV2'
        )
        await state.set_state(FSMGuide.reference)
        await callback.answer(show_alert=True)
    except Exception as e:
        logger.critical(
            'Ошибка кнопке далее 4(Как подобрать размер обуви и одежды)', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'кнопке далее 4(Как подобрать размер обуви и одежды):\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


# Кнопка далее 5 (Как найти ссылку)
@router.callback_query(F.data == 'button_next', StateFilter(FSMGuide.reference))
async def guide_poizon_5(callback: CallbackQuery, state: FSMContext):
    try:
        user = callback.from_user.username
        logger.info(f"Пользователь {user} в гайде найти ссылку")
        media_group = MediaGroupBuilder()
        media_group.add_photo(
            media=static.url_guide_1)
        media_group.add_photo(
            media=static.url_guide_2)
        await bot.send_media_group(
            chat_id=callback.message.chat.id,
            media=media_group.build())
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=LEXICON_RU["Как найти ссылку"],
            reply_markup=menu_one,
            parse_mode='MarkdownV2'
        )
        await state.clear()
        await callback.answer(show_alert=True)
    except Exception as e:
        logger.critical(
            'Ошибка кнопке далее 5', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'кнопке далее 5:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)
