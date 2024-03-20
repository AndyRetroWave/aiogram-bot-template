import logging
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from app.lexicon.lexicon_ru import LEXICON_RU
from app.keyboards.keyboards import next, next_and_poizon, menu_one, android_poizon
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from app.states.states import FSMGuide
from aiogram.fsm.state import default_state
from config.config import bot
from aiogram.utils.media_group import MediaGroupBuilder
router = Router()


# Кнопка Гайда основа
@router.callback_query(F.data == 'button_guide', StateFilter(default_state))
async def guide_poizon_1(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=LEXICON_RU["Гайд по пойзон"],
        reply_markup=next,
        parse_mode='MarkdownV2'
    )
    await state.set_state(FSMGuide.install_1)
    await callback.answer(show_alert=True)

# Кнопка скачивания POIZON
@router.callback_query(F.data == 'button_next', StateFilter(FSMGuide.install_1))
async def poizon(callback: CallbackQuery, state: FSMContext):
    media_group = MediaGroupBuilder()
    # Для Теста
    media_group.add_photo(
        media="AgACAgIAAxkBAAIF0WX4QXGjXGClZFUMibdi6EDY2fa7AAKq2DEbqmHBS1HF-QsGuptdAQADAgADeAADNAQ")
    media_group.add_photo(
        media="AgACAgIAAxkBAAIF02X4QX8b5ZnIj0GTssP5wrign5WcAAKr2DEbqmHBS1FXs-L4SH4BAQADAgADeAADNAQ")
    media_group.add_photo(
        media="AgACAgIAAxkBAAIF1WX4QYihzlZAuuROs2ufNNoU9A_SAAKs2DEbqmHBS9e_z3SWAXV6AQADAgADeAADNAQ")
    media_group.add_photo(
        media="AgACAgIAAxkBAAIF12X4QZS6av8nogXwgXo3bULzYfu5AAKt2DEbqmHBS5SHlzp0NjoFAQADAgADeAADNAQ")
    media_group.add_photo(
        media="AgACAgIAAxkBAAIF2WX4QaCAYDPCsxnlRyeYgYKU7pP5AAKz2DEbqmHBSwnsyj0ak911AQADAgADeAADNAQ")
    media_group.add_photo(
        media="AgACAgIAAxkBAAIF22X4QiQeazLwa4v6J-OP_p76Jw_9AAK62DEbqmHBS2sEYMMRxwmfAQADAgADeAADNAQ")
    media_group.add_photo(
        media="AgACAgIAAxkBAAIF3WX4Qi-Y2kjwuz4j0yPj6ZAN028aAAK72DEbqmHBS68VhcwNLReIAQADAgADeAADNAQ")
    media_group.add_photo(
        media="AgACAgIAAxkBAAIF32X4QkBvRVCDiYnat_50PtoeVAgIAAK92DEbqmHBS_dy7dZahgIaAQADAgADeAADNAQ")
    media_group.add_photo(
        media="AgACAgIAAxkBAAIF4WX4QlK3YBIRcSUZw0RM49AX5JGCAALD2DEbqmHBS8FMOok-MMZEAQADAgADeAADNAQ")
    # Для Сервера
    # media_group.add_photo(
    #     media="AgACAgIAAxkBAAII1GX0MesrJHO8mL_H-QSrfc0RwXYKAAIH2DEbvlagS0qUe8WK0MttAQADAgADeAADNAQ")
    # media_group.add_photo(
    #     media="AgACAgIAAxkBAAII1mX0MfLvXlMQEn75grUDSRHxkQ9kAAId2DEbvlagS23cyonH1o8pAQADAgADeAADNAQ")
    # media_group.add_photo(
    #     media="AgACAgIAAxkBAAII2GX0MfbeifqYKj15dWWPK9jcmJdLAAIe2DEbvlagS6l_SugOyr5LAQADAgADeAADNAQ")
    # media_group.add_photo(
    #     media="AgACAgIAAxkBAAII2mX0Mfxy_BIp2mTs7ldfX6XJvXbUAAIf2DEbvlagS57cStXrdazOAQADAgADeAADNAQ")
    # media_group.add_photo(
    #     media="AgACAgIAAxkBAAII3GX0MgABBGw_2bmXv-zh15R1_ranaQACINgxG75WoEuVE2MQAAGt-PcBAAMCAAN4AAM0BA")
    # media_group.add_photo(
    #     media="AgACAgIAAxkBAAII3mX0MgSY2VPJPKGK1TXdqgcvsLU9AAIh2DEbvlagS2skqmQ3bWjbAQADAgADeAADNAQ")
    # media_group.add_photo(
    #     media="AgACAgIAAxkBAAII4GX0MglNa2FOOOgy1dVyHD7qTB-ZAAIi2DEbvlagS6uux6No-IYTAQADAgADeAADNAQ")
    # media_group.add_photo(
    #     media="AgACAgIAAxkBAAII4mX0Mg2BrpzXQi6laXcKi43HfJyRAAIj2DEbvlagS7tH_qxWmIZpAQADAgADeAADNAQ")
    # media_group.add_photo(
    #     media="AgACAgIAAxkBAAII5GX0MhE8xZRWYlksMlRjmhkGaQTKAAIk2DEbvlagS_HhVQeHkDiYAQADAgADeAADNAQ")
    await bot.send_media_group(chat_id=callback.message.chat.id, media=media_group.build())
    await bot.send_message(
        chat_id=callback.message.chat.id,
        text=LEXICON_RU["Скачивание"],
        reply_markup=android_poizon,
        parse_mode='MarkdownV2'
    )
    await callback.answer(show_alert=True)
    await state.set_state(FSMGuide.install_2)


# Кнопка далее(Регистрация в пойзон)
@router.callback_query(F.data == 'button_next', StateFilter(FSMGuide.install_2))
async def guide_poizon_1(callback: CallbackQuery, state: FSMContext):
    await bot.send_photo(
        chat_id=callback.message.chat.id,
        photo="AgACAgIAAxkBAAIGnGX5Q4KOoCMtcAHifOvqu9AItSnSAAIT2DEbqmHJS0BUzaSM8VVvAQADAgADeQADNAQ",
        caption=LEXICON_RU["Регистрация пойзон"],
        reply_markup=next,
        parse_mode='MarkdownV2'
    )
    await state.set_state(FSMGuide.install_3)
    await callback.answer(show_alert=True)


# Кнопка далее 2(Регистрация в пойзон)
@router.callback_query(F.data == 'button_next', StateFilter(FSMGuide.install_3))
async def guide_poizon_2(callback: CallbackQuery, state: FSMContext):
    media_group = MediaGroupBuilder()
    # Для Теста
    media_group.add_photo(
        media="AgACAgIAAxkBAAIEP2X3_2De7kr1o0-b9QmGitbZqmEzAAIF1DEbYA3AS9apwqfRgmQLAQADAgADeQADNAQ")
    media_group.add_photo(
        media="AgACAgIAAxkBAAIEO2X3_1cSZyZ-6FBKHmExuEOOnmChAAID1DEbYA3AS5MHY30bEBBiAQADAgADeQADNAQ")
    media_group.add_photo(
        media="AgACAgIAAxkBAAIEPWX3_10Fjin1XG2y8vuhlWkC6FBfAAIE1DEbYA3AS9s2FDkXDNA2AQADAgADeQADNAQ")
    # Для сервера
    # media_group.add_photo(
    #     media="AgACAgIAAxkBAAIKumX4NsDLBfOKOW2x9ntuk8LYQlopAALQ3jEb9HzAS2LeQ3ppIK1zAQADAgADeQADNAQ")
    # media_group.add_photo(
    #     media="AgACAgIAAxkBAAIKvGX4Ns1ySv7gsQ3ArNjpkAP_du4oAALR3jEb9HzAS3bsmAvjVhmMAQADAgADeQADNAQ")
    # media_group.add_photo(
    #     media="AgACAgIAAxkBAAIKvmX4Nt1e9ZC2WrW9zTPgb-se1_QBAALS3jEb9HzAS494kVWnDjnGAQADAgADeQADNAQ")
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

# Кнопка далее 3(Поиск модели)


@router.callback_query(F.data == 'button_next', StateFilter(FSMGuide.search_1))
async def guide_poizon_3(callback: CallbackQuery, state: FSMContext):
    media_group = MediaGroupBuilder()
    # Для Теста
    media_group.add_photo(
        media="AgACAgIAAxkBAAIElWX4GbV-b-HFiDyu0GdTYMeq7qARAAKl1DEbYA3AS0XbaPpbHVLeAQADAgADeQADNAQ")
    media_group.add_photo(
        media="AgACAgIAAxkBAAIEl2X4Gb1bIdEBKipO25XTBAt40WKZAAKm1DEbYA3AS5tw0opCUYQ1AQADAgADeQADNAQ")
    media_group.add_photo(
        media="AgACAgIAAxkBAAIEmWX4GcUG2LSlHU8z3e6fYcQ0a52QAAKn1DEbYA3AS3tOcY5JF45HAQADAgADeQADNAQ")
    media_group.add_photo(
        media="AgACAgIAAxkBAAIEm2X4Gc1ueSBMOt1ziS8SO5uBa2ZIAAKo1DEbYA3AS70ygdlnvMr0AQADAgADeQADNAQ")
    media_group.add_photo(
        media="AgACAgIAAxkBAAIEnWX4GdICLFRCHM7q7G0wO7JOoh0gAAKp1DEbYA3AS0nvlWJkmXMCAQADAgADeQADNAQ")
    # Для сервера
    # media_group.add_photo(
    #     media="AgACAgIAAxkBAAIKwGX4NxJ3svDuFu0VlRT5_9EhfEz8AAKl1DEbYA3AS48OJ_ngE9MAAQEAAwIAA3kAAzQE")
    # media_group.add_photo(
    #     media="AgACAgIAAxkBAAIKwmX4NyDhugrh_XzDEUKdV0DOjFPnAAKm1DEbYA3AS4LiikIM5RpTAQADAgADeQADNAQ")
    # media_group.add_photo(
    #     media="AgACAgIAAxkBAAIKxGX4NzCTAAGyzks68uhvmcMAAS0G49YAAqfUMRtgDcBLfcFliyhu7AQBAAMCAAN5AAM0BA")
    # media_group.add_photo(
    #     media="AgACAgIAAxkBAAIKxmX4N0HtF-FSVB28RHjwG4jAHablAAKo1DEbYA3AS4yfDR7ZcuiqAQADAgADeQADNAQ")
    # media_group.add_photo(
    #     media="AgACAgIAAxkBAAIKyGX4N06cIviK_aTaEdrdnjpU6VscAAKp1DEbYA3AS2S9FatVih6hAQADAgADeQADNAQ")
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


# Кнопка далее 4(Как подобрать размер обуви и одежды)
@router.callback_query(F.data == 'button_next', StateFilter(FSMGuide.size_1))
async def guide_poizon_4(callback: CallbackQuery, state: FSMContext):
    media_group = MediaGroupBuilder()
    # Для Теста
    media_group.add_photo(
        media="AgACAgIAAxkBAAIEm2X4Gc1ueSBMOt1ziS8SO5uBa2ZIAAKo1DEbYA3AS70ygdlnvMr0AQADAgADeQADNAQ")
    media_group.add_photo(
        media="AgACAgIAAxkBAAIFAAFl-CVjqtRgLFQN6CkhMa3jNSawnwAC6tQxG2ANwEtxAxwUsxI5_QEAAwIAA3kAAzQE")
    media_group.add_photo(
        media="AgACAgIAAxkBAAIFAmX4JWf-iJeFM9P_jbrXXFVmInD6AALr1DEbYA3ASzKjpP7Q-elbAQADAgADeQADNAQ")
    # Для сервера
    # media_group.add_photo(
    #     media="AgACAgIAAxkBAAIKxmX4N0HtF-FSVB28RHjwG4jAHablAAKo1DEbYA3AS4yfDR7ZcuiqAQADAgADeQADNAQ")
    # media_group.add_photo(
    #     media="AgACAgIAAxkBAAIKymX4N5Rm1QZSi3auGOtnzdbjChrSAALq1DEbYA3AS9mnqnG84b6mAQADAgADeQADNAQ")
    # media_group.add_photo(
    #     media="AgACAgIAAxkBAAIKzGX4N56DOujCiocgtL3WSt134-_pAALr1DEbYA3AS_wE3pW_dbGLAQADAgADeQADNAQ")
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


# Кнопка далее 5 (Как найти ссылку)
@router.callback_query(F.data == 'button_next', StateFilter(FSMGuide.reference))
async def guide_poizon_5(callback: CallbackQuery, state: FSMContext):
    media_group = MediaGroupBuilder()
    # Для теста
    media_group.add_photo(
        media="AgACAgIAAxkBAAIFWWX4NLPdzOeI5ifSuzJrBhzlSr0TAAI32DEbqmHBSw_W6hXsx-scAQADAgADeQADNAQ")
    media_group.add_photo(
        media="AgACAgIAAxkBAAIFW2X4NLcUAAG-JuRUMUlWhmtl16BHAgACONgxG6phwUtkfyLCRxI_5QEAAwIAA3kAAzQE")
    # Для сервера
    # media_group.add_photo(
    #     media="AgACAgIAAxkBAAIKzmX4N82PI6w54wHGTBfpeuRkJ44mAAI32DEbqmHBSwkV6ldJ4mDLAQADAgADeQADNAQ")
    # media_group.add_photo(
    #     media="AgACAgIAAxkBAAIK0GX4N9bMpLDhPeZh7_ymQ0x3XQTUAAI42DEbqmHBS0cdyE8mvgg8AQADAgADeQADNAQ")
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
