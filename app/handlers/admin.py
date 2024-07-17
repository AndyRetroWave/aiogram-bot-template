import traceback
from aiogram import F, types, Router
import aiogram
from aiogram.types import CallbackQuery, Message
from app.dependence.dependence import logger_error_critical_send_message_admin
from app.lexicon.lexicon_ru import LEXICON_RU
from app.keyboards.keyboards import meny_admin, admin, mailing_botton, shiping_cost
from app.models.course.dao import (add_bank, add_course, course_today,
                                   delete_course, get_bank, get_phone_bank,
                                   modify_bank, modify_phone_bank
                                   )
from app.models.course.models import cost_ships
from app.models.images.dao import delete_image, get_image, save_image
from app.models.users.dao import all_user
from config.config import settings, logger
from app.states.states import (FSMBank, FSMCourse, FSMMailing, FSMImages, FSMPhone,
                               FSMShippingClother, FSMShippingJacket, FSMShippingSneaker
                               )
from aiogram.fsm.state import default_state
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from config.config import bot


router = Router()


# Кнопка Админ панель
@router.callback_query(F.data == 'add_course_admin')
async def admin_panel(callback: CallbackQuery):
    try:
        await callback.message.edit_text(
            text="Что будем делать?",
            reply_markup=admin
        )
        await callback.answer(show_alert=True)
    except:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Кнопка добовления курса юаня
@router.callback_query(F.data == 'add_course_botton', StateFilter(default_state))
async def add_course_yan(callback: CallbackQuery, state: FSMContext):
    try:
        try:
            value = await course_today()
            formatted_num = "{}\\.{}".format(
                int(value), int(value * 100) % 100)
            await callback.message.edit_text(
                text=f"""Введи курс на сегодняшний день❗\nКурс на данный момент: *{formatted_num}* """,
                parse_mode='MarkdownV2',
            )
            await callback.answer(show_alert=True)
            await state.set_state(FSMCourse.course)
        except:
            await callback.message.edit_text(
                text=f"""Введи курс на сегодняшний день\n\n""",
                parse_mode='MarkdownV2',
            )
            await callback.answer(show_alert=True)
            await state.set_state(FSMCourse.course)
    except:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Хендлер по добавлению курса юаня
@router.message(StateFilter(FSMCourse.course))
async def calculator_rate_value(message: Message, state: FSMContext):
    try:
        try:
            if await course_today():
                course = message.text
                new_course = float(course.replace(",", "."))
                await add_course(new_course)
                await delete_course()
                await state.clear()
                await message.answer(
                    text="Курс юаня успешно установлен",
                    reply_markup=meny_admin)
            else:
                course = message.text
                new_course = float(course.replace(",", "."))
                await add_course(new_course)
                await state.clear()
                await message.answer(
                    text="Курс юаня успешно установлен",
                    reply_markup=meny_admin)
        except ValueError:
            await message.answer(
                text="Введи пожалуйста курс числом а не словами")
    except:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Кнопка рассылки
@router.callback_query(F.data == 'mailing_botton', StateFilter(default_state))
async def botton_mailing(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.edit_text(
            text=LEXICON_RU["Рассылка"],
            parse_mode='MarkdownV2',
        )
        await callback.answer(show_alert=True)
        await state.set_state(FSMMailing.mailing)
    except:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Хендлер по рассылки
@router.message(StateFilter(FSMMailing.mailing))
async def handler_mailing(message: Message, state: FSMContext):
    try:
        try:
            text = message.text
            if message.content_type == 'photo':
                photo_id = message.photo[-1].file_id
                caption = message.caption
                await state.update_data({"photo_id": photo_id})
                await state.update_data({"caption": caption})
                await bot.send_photo(
                    chat_id=message.chat.id,
                    photo=photo_id,
                    caption=caption,
                    parse_mode='MarkdownV2')
                await message.answer(
                    text="Вот так будет выглядеть смс у людей Что будем белать",
                    reply_markup=mailing_botton
                )
                await state.set_state(FSMMailing.mailing2)
            else:
                text = message.text
                await state.update_data({"text": text})
                await bot.send_message(
                    chat_id=message.chat.id,
                    text=text,
                    parse_mode='MarkdownV2')
                await message.answer(
                    text="Вот так будет выглядеть смс у людей Что будем белать",
                    reply_markup=mailing_botton
                )
                await state.set_state(FSMMailing.mailing2)
        except:
            await message.answer(
                text="Ты не правильно экранизировал символы или допустил ошибку,"
                "повтори еще раз"
            )
    except:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Хендлер по рассылки
@router.callback_query(F.data == 'button_сonfirm_and_send',
                       StateFilter(FSMMailing.mailing2))
async def text_mailing(callback: CallbackQuery, state: FSMContext):
    try:
        user = await all_user()
        try:
            photo = (await state.get_data())['photo_id']
            caption = (await state.get_data())['caption']
            for users in user:
                try:
                    await callback.answer(text="Отправил")
                    await bot.send_photo(
                        chat_id=users,
                        photo=photo,
                        caption=caption,
                        parse_mode='MarkdownV2')
                except aiogram.exceptions.TelegramForbiddenError:
                    print(f"Bot is blocked by user {users}")
                await state.clear()
                await callback.answer(show_alert=True)
        except KeyError as e:
            print(f"KeyError: {e}")
            caption = (await state.get_data())['text']
            for users in user:
                try:
                    await callback.answer(text="Отправил")
                    await bot.send_message(
                        chat_id=users,
                        text=caption,
                        parse_mode='MarkdownV2')
                except aiogram.exceptions.TelegramForbiddenError:
                    print(f"Bot is blocked by user {users}")
                await state.clear()
                await callback.answer(show_alert=True)
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Кнопка изменения текста
@router.callback_query(F.data == 'button_modify')
async def botton_mailing_changes(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.edit_text(
            text=LEXICON_RU["Рассылка"],
            parse_mode='MarkdownV2',
        )
        await callback.answer(show_alert=True)
        await state.set_state(FSMMailing.mailing)
    except:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


async def notification():
    await bot.send_message(chat_id=538383620,
                           text='Доброе утро! Пора обновлять курс юаня!',
                           reply_markup=admin
                           )


# Кнопка изменение картинки на превью
@router.callback_query(F.data == "add_button_image", StateFilter(default_state))
async def modify_image_botton(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.edit_text(
            text="Закинь сюда фото которе хотел бы видеть на превьюхе",
        )
        await callback.answer(show_alert=True)
        await state.set_state(FSMImages.image)
    except:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Хендлер по изменению картинки
@router.message(StateFilter(FSMImages.image))
async def modify_image(message: Message, state: FSMContext):
    try:
        try:
            file_id = message.photo[-1].file_id
            if await get_image() == None:
                await save_image(file_id)
            else:
                await save_image(file_id)
                await delete_image()
            await message.answer(text="Ты успешно поменял картинку!",
                                 reply_markup=meny_admin)
            await state.clear()
        except:
            await message.answer(
                text="Ты засунул в меня что то иное друг, повтори попытку"
            )
    except:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Кнопка изменения банка получателя
@router.callback_query(F.data == "add_button_bank", StateFilter(default_state))
async def modify_image_botton(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.edit_text(
            text="Введи новый банк для получения денег от клиента\nВ таком"
            "формате: Тинькофф! Рябов.П\nОбязательно нужно указывать фамилию получателя",
        )
        await callback.answer(show_alert=True)
        await state.set_state(FSMBank.bank)
    except:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Хендлер для изменения банка получаетеля
@router.message(StateFilter(FSMBank.bank))
async def modify_image(message: Message, state: FSMContext):
    try:
        try:
            bank = message.text
            if await get_bank() == None:
                await add_bank(bank)
            else:
                await modify_bank(bank)
                await delete_image()
            await message.answer(text="Ты успешно поменял банк!",
                                 reply_markup=meny_admin)
            await state.clear()
        except:
            await message.answer(
                text="Ты засунул в меня что то иное друг, повтори попытку"
            )
    except:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Кнопка изменения номера телефона получателя
@router.callback_query(F.data == "add_button_bank_phone", StateFilter(default_state))
async def modify_image_botton(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.edit_text(
            text="Введи новый номер телефона для получателя",
        )
        await callback.answer(show_alert=True)
        await state.set_state(FSMPhone.phone)
    except:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Хендлер для изменения номера телефона получателя
@router.message(StateFilter(FSMPhone.phone))
async def modify_image(message: Message, state: FSMContext):
    try:
        try:
            phone = str(message.text)
            await modify_phone_bank(phone)
            await message.answer(text="Ты успешно поменял номер телефона!",
                                 reply_markup=meny_admin)
            await state.clear()
        except:
            await message.answer(
                text="Ты засунул в меня что то иное друг, повтори попытку"
            )
    except:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Кнопка изменения стоимости доставки для товаров
@router.callback_query(F.data == 'add_set_shipping_cost')
async def admin_panel(callback: CallbackQuery):
    try:
        await callback.message.edit_text(
            text="Что будем изменять?",
            reply_markup=shiping_cost
        )
        await callback.answer(show_alert=True)
    except:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Кнопка изменения стоимости доставки для кроссовка
@router.callback_query(F.data == 'button_set_button', StateFilter(default_state))
async def admin_panel(callback: CallbackQuery, state: FSMShippingSneaker):
    try:
        await callback.message.edit_text(
            text="Введи новую стоимость доставки"
        )
        await callback.answer(show_alert=True)
        await state.set_state(FSMShippingSneaker.cost)
    except:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Хендлер для изменения стоимости доставки для кроссовка
@router.message(StateFilter(FSMShippingSneaker.cost))
async def modify_image(message: Message, state: FSMContext):
    try:
        try:
            cost = int(message.text)
            cost_ships.sneaker = cost
            await message.answer(text="Ты успешно поменял стоимость доставки!",
                                 reply_markup=meny_admin)
            await state.clear()
        except:
            await message.answer(
                text="Ты засунул в меня что то иное друг, повтори попытку"
            )
    except:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Кнопка изменения стоимости доставки для одежды
@router.callback_query(F.data == 'button_set_clothes',
                       StateFilter(default_state)
                       )
async def admin_panel(callback: CallbackQuery, state: FSMShippingClother):
    try:
        await callback.message.edit_text(
            text="Введи новую стоимость доставки"
        )
        await callback.answer(show_alert=True)
        await state.set_state(FSMShippingClother.cost)
    except:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Хендлер для изменения стоимости доставки для одежды
@router.message(StateFilter(FSMShippingClother.cost))
async def modify_image(message: Message, state: FSMContext):
    try:
        try:
            cost = int(message.text)
            cost_ships.closer = cost
            await message.answer(text="Ты успешно поменял стоимость доставки!",
                                 reply_markup=meny_admin)
            await state.clear()
        except:
            await message.answer(
                text="Ты засунул в меня что то иное друг, повтори попытку"
            )
    except:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Кнопка изменения стоимости доставки для пуховиков
@router.callback_query(F.data == 'button_set_jacket',
                       StateFilter(default_state))
async def admin_panel(callback: CallbackQuery, state: FSMShippingJacket):
    try:
        await callback.message.edit_text(
            text="Введи новую стоимость доставки"
        )
        await callback.answer(show_alert=True)
        await state.set_state(FSMShippingJacket.cost)
    except:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Хендлер для изменения стоимости доставки для одежды
@router.message(StateFilter(FSMShippingJacket.cost))
async def modify_image(message: Message, state: FSMContext):
    try:
        try:
            cost = int(message.text)
            cost_ships.jacket = cost
            await message.answer(text="Ты успешно поменял стоимость доставки!",
                                 reply_markup=meny_admin)
            await state.clear()
        except:
            await message.answer(text="Ты засунул в меня что то иное друг,"
                                      "повтори попытку")
    except:
        logger.critical(
            "Ошибка в изменния стоимости доставки для пуховиков",
            exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'кнопке кнопке админ панель:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)
