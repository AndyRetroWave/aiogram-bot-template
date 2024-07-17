import traceback
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from app.dependence.dependence import logger_error_critical_send_message_admin, send_photo_calculator, shipping_costing
from app.lexicon.lexicon_ru import LEXICON_RU
from app.keyboards.keyboards import calculator_rate, update_calculator
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from app.states.states import FSMCare, FSMClothes, FSMSneakers, FSMDownJacket
from app.static.images import static
from aiogram.fsm.state import default_state
from config.config import settings, bot, logger
from app.models.course.models import cost_ships

router = Router()


# Кнопка категория
@router.callback_query(F.data == 'big_button_1_pressed')
async def category_botton(callback: CallbackQuery):
    try:
        await callback.message.edit_text(
            text=LEXICON_RU["Категория"],
            reply_markup=calculator_rate,
            parse_mode='MarkdownV2'
        )
        await callback.answer(show_alert=True)
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Кнопка повтора
@router.callback_query(F.data == 'big_button_1_pressed')
async def repetition_buttons(callback: CallbackQuery):
    try:
        await callback.message.edit_text(
            text=LEXICON_RU["Категория"],
            reply_markup=calculator_rate,
            parse_mode='MarkdownV2'
        )
        await callback.answer(show_alert=True)
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Кнопка кросовка
@router.callback_query(F.data == 'button_snecers', StateFilter(default_state))
async def sneaks_button(callback: CallbackQuery, state: FSMContext):
    try:
        await send_photo_calculator(
            static=static, bot=bot, callback=callback)
        await state.set_state(FSMSneakers.rate_sneakers)
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Хендлер по цене кросовок
@router.message(StateFilter(FSMSneakers.rate_sneakers))
async def calculator_rate_value(message: Message, state: FSMContext):
    try:
        try:
            await shipping_costing(
                category="Кросовки👟", cost_ships=cost_ships.sneaker,
                message=message, state=state, reply_markup=update_calculator,
            )
        except ValueError:
            await message.answer(text=LEXICON_RU["Стоимость в юанях"],
                                 parse_mode='MarkdownV2')
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Кнопка пуховики
@router.callback_query(F.data == 'button_down_jacket', StateFilter(default_state))
async def button_down_jacket(callback: CallbackQuery, state: FSMContext):
    try:
        await send_photo_calculator(
            static=static, bot=bot, callback=callback
        )
        await state.set_state(FSMDownJacket.rate_down_jacket)
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Хендлер по цене пуховики
@router.message(StateFilter(FSMDownJacket.rate_down_jacket))
async def calculator_down_jacket(message: Message, state: FSMContext):
    try:
        try:
            await shipping_costing(
                category="Пуховики🥼", cost_ships=cost_ships.jacket,
                message=message, state=state, reply_markup=update_calculator,
            )
        except ValueError:
            await message.answer(text=LEXICON_RU["Стоимость в юанях"],
                                 parse_mode='MarkdownV2')
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Кнопка Одежды
@router.callback_query(F.data == 'button_clothes', StateFilter(default_state))
async def button_clothes(callback: CallbackQuery, state: FSMContext):
    try:
        await send_photo_calculator(
            static=static, bot=bot, callback=callback
        )
        await state.set_state(FSMClothes.rate_clothes)
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Хендлер по цене одежды
@router.message(StateFilter(FSMClothes.rate_clothes))
async def calculator_clothes(message: Message, state: FSMContext):
    try:
        try:
            await shipping_costing(
                category="Одежда🩳", cost_ships=cost_ships.closer,
                message=message, state=state, reply_markup=update_calculator,
            )

        except ValueError:
            await message.answer(text=LEXICON_RU["Стоимость в юанях"],
                                 parse_mode='MarkdownV2')
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Кнопка Украшения/духи/ковры
@router.callback_query(F.data == 'button_care', StateFilter(default_state))
async def button_care(callback: CallbackQuery, state: FSMContext):
    try:
        await send_photo_calculator(
            static=static, bot=bot, callback=callback
        )
        await state.set_state(FSMCare.rate_сare)
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Хендлер по цене Украшения/духи/ковры
@router.message(StateFilter(FSMCare.rate_сare))
async def calculator_rate_care(message: Message, state: FSMContext):
    try:
        try:
            await shipping_costing(
                category="Украшения/духи/ковры🕶", cost_ships=cost_ships.closer,
                message=message, state=state, reply_markup=update_calculator,
            )
        except ValueError:
            await message.answer(text=LEXICON_RU["Стоимость в юанях"],
                                 parse_mode='MarkdownV2')
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Кнопка аксессуары
@router.callback_query(F.data == 'button_jewelry')
async def button_jewelry(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.edit_text(
            text=LEXICON_RU["Заказ аксессуаров"],
            parse_mode='MarkdownV2',
            reply_markup=update_calculator,)
        await callback.answer(show_alert=True)
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )
