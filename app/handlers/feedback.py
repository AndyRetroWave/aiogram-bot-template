from aiogram import F, types, Router
from aiogram.types import CallbackQuery, Message
from app.filters.filters import photo, file
from app.lexicon.lexicon_ru import LEXICON_RU
from app.keyboards.keyboards import calculator_update, meny_admin, android_poizon
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
        text=f"""Введи курс на сегодняшний день\n\n❗*ВНИМАНИЕ* надо добавлять курс с точкой\!\n\nКурс на данный момент: *{formatted_num}* """,
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


# Кнопка курска юаня
@router.callback_query(F.data == 'button_rate')
async def course_yan(callback: CallbackQuery):
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
        reply_markup=android_poizon,
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
@router.callback_query(F.data == 'android_poizon_botton')
async def calculator_rate_value(callback: CallbackQuery):
    logger.debug('Вошли в хендлер добавления курса юаня')
    await bot.send_document(
        chat_id=callback.message.chat.id,
        document="BQACAgIAAxkBAAIJF2X0Q25XzC9d3Scln9zmao5kjw4zAALPRAACvlagS-VCxk9phw4TNAQ",
    )
    logger.debug('Не получилось добавить курс')
    logger.debug('Вышли из хендлера добавления курса юаня')


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
    logger.debug('Вошли в хендлер добавления курса юаня')
    file_id = message.document.file_id
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

