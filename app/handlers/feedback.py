import asyncio
import traceback
from aiogram import F, types, Router
from aiogram.types import CallbackQuery, Message
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
        logger.critical(
            'Ошибка кнопке отзывы', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'кнопке далее(Регистрация в пойзон):\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


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
        logger.critical(
            'Ошибка кнопке инструкция', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'кнопке инструкция:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


# Кнопка курска юаня
@router.callback_query(F.data == 'button_rate')
async def course_yan(callback: CallbackQuery):
    try:
        value = await course_today()
        formatted_num = "{}\\.{}".format(
            int(value), int(value * 100) % 100)
        logger.debug('Вошли в курс юаня')
        await callback.message.edit_text(
            text=f"""Курс юаня к рублю на сегодня : *{formatted_num}*\n\n
*Почему у нас такой большой курс юаня?*🇨🇳 Если вы задались таким вопросом, значит вы зашли на сайт [Центробанка РФ](http://cbr.ru/) и справа снизу посмотрели официальный курс и увидели, что он отличается от нашего примерно на 2 рубля\(специально не приводим точных цифр, т\.к\. ситуация меняется каждый день\)\n\n
Самый простой ответ на вопрос о высоком курсе:\n
❗️В текущих реалиях нельзя купить валюту даже близко к курсу ЦБ Например, можно посмотреть по какой цене [Сбербанк](http://www.sberbank.ru/ru/quotes/currencies?currency=CNY) продает *юань*\n\n
Обычно это плюс 3,5 рубля к официальному курсу ЦБ\n\n
Но даже если предположить, что у вас есть юань в физическом\(фиатном\) виде \-дальше его нужно отправить в Китай\.Тут также в игру вступают посредники и курс сильно вырастет\. 💴\n\n
Если у вас есть юань на брокерском счете \(например, тинькоф\) \- попробуйте их вывести без потери хотябы 20%\.📈\n\n
Мы совершаем деньги с валютой *"день в день"* \- вы перевели нам рубли, мы сразу оплатили заказ в юанях "из своих", сразу же поменяли ваши рубли на юань\. Мы не занимаемся накоплением рублей в ожидании падения курса, чтобы на этом заработать\- это не наш бизнес\. \(темболее, чаще всего происходит обратное\)\n\n
Мы стараемся закупать валюту максимально дешево и оперативно\.Сверьте наш курс с курсом у конкурентов и вы поймете, что мы молодцы, даже без учета комиссий\n\n
*Какой будет курс завтра?*💴🇨🇳💴
Мы не знаем также как и не знаете вы\. Всем клиентам\(хоть на 100юаней, хоть на 100 000 юане\) мы советуем не ждать завтра, потому что завтра в большинстве случаев хуже\. В таком мире живем\.\n\n
*Мы готовы купить неограниченное количество юаней по курсу ЦБ*""",
            reply_markup=calculator_update,
            parse_mode='MarkdownV2',
            disable_web_page_preview=True
        )
        await callback.answer(show_alert=True)
    except Exception as e:
        logger.critical(
            'Ошибка кнопке курса юаня', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'кнопке курса юаня:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


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
        await bot.send_message(chat_id=settings.ADMIN_ID2,
                               text=f"Кобанчик, тобой поинтересовался этот [челик](https://t.me/{user})\!",
                               parse_mode='MarkdownV2')
    except:
        logger.critical("Ошибка в кнопке создатель", exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'кнопке создатель:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


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
        logger.critical("Ошибка в кнопке вопрос", exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'кнопке вопрос:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


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
