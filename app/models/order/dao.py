from datetime import datetime, timedelta
import traceback
from sqlalchemy import delete, select, update, and_
from app.lexicon.lexicon_ru import LEXICON_RU
from app.models.order.models import OrderGivenModel, OrderModel, OrderModelSave
from config.database import async_session_maker
from config.config import bot
from config.config import settings

from config.config import logger

# добавление заказа в корзину


async def add_order(
    addres: str,
    url: str,
    color: str,
    round_value: int,
    phone: str,
    username: str,
    order: int,
    user_id: int,
    shipping_cost: int
):
    try:
        async with async_session_maker() as session:
            new_order = OrderModel(
                user_id=user_id,
                price=round_value,
                addres=addres,
                name=username,
                phone=phone,
                color=color,
                url=url,
                order=order,
                data=datetime.now(),
                shipping_cost=shipping_cost,
            )
            session.add(new_order)
            await session.commit()
    except Exception as e:
        logger.critical(
            'Ошибка в dao добавление заказа в корзину', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'dao добавление заказа в корзину:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


# Запись данных человека
async def add_diven_user(
    addres: str,
    phone: str,
    username: str,
    user_id: int,
):
    try:
        async with async_session_maker() as session:
            new_user = OrderGivenModel(
                user_id=user_id,
                addres=addres,
                name=username,
                phone=phone,
            )
            session.add(new_user)
            await session.commit()
    except Exception as e:
        logger.critical(
            'Ошибка в записи данных человека по адресу', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'записи данных человека по адресу:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


# получение заказа по юзеру
async def order_user_id_all(
    user_id: int
):
    try:
        async with async_session_maker() as session:
            result = await session.execute(select(OrderModel).
                                           where(OrderModel.user_id == user_id))
            price = result.mappings().all()
            return [{'id': row['OrderModel'].id,
                    'user_id': row['OrderModel'].user_id,
                     'price': row['OrderModel'].price,
                     'addres': row['OrderModel'].addres,
                     'name': row['OrderModel'].name,
                     'phone': row['OrderModel'].phone,
                     'color': row['OrderModel'].color,
                     'url': row['OrderModel'].url,
                     'order': row['OrderModel'].order,
                     'date': row['OrderModel'].data,
                     'shipping_cost': row['OrderModel'].shipping_cost} for row in price]
    except Exception as e:
        logger.critical(
            'Ошибка получение заказа по юзеру', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'получение заказа по юзеру:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


async def order_user_id_all_2(
    user_id: int
):
    try:
        async with async_session_maker() as session:
            result = await session.execute(select(OrderModel).
                                           where(OrderModel.user_id == user_id))
            price = result.mappings().all()
            order_models = [d['OrderModel'] for d in price]
            return order_models
    except Exception as e:
        logger.critical(
            'Ошибка получение заказа по юзеру', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'получение заказа по юзеру:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


# Получение данных клиента
async def get_clien_data(
        user_id: int,
):
    try:
        async with async_session_maker() as session:
            result = await session.execute(select(OrderGivenModel).
                                           where(OrderGivenModel.user_id == user_id))
        user_phone = result.scalar()
        return user_phone
    except Exception as e:
        logger.critical(
            'Ошибка Получение телефона юзера по таблице given ', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'Получение телефона юзера по таблице given:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


# Получение телефона юзера по таблице given
async def phone_user_id_given(
        user_id: int,
):
    try:
        async with async_session_maker() as session:
            result = await session.execute(select(OrderGivenModel).
                                           where(OrderGivenModel.user_id == user_id))
        user_phone = result.scalar()
        if user_phone is not None:
            phone = user_phone.phone
            return phone
        else:
            pass
    except Exception as e:
        logger.critical(
            'Ошибка Получение телефона юзера по таблице given ', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'Получение телефона юзера по таблице given:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


# получение адреса юзера по таблице given
async def addres_user_id_given(
    user_id: int
):
    try:
        async with async_session_maker() as session:
            result = await session.execute(select(OrderGivenModel).
                                           where(OrderGivenModel.user_id == user_id))
            addres_user = result.scalar()
            if addres_user is not None:
                addres = addres_user.addres
                return addres
            else:
                pass
    except Exception as e:
        logger.critical(
            'Ошибка получение адреса юзера по таблице given ', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'получение адреса юзера по таблице given:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


# получение имени юзера по заказу по таблицу given
async def username_user_id_given(
    user_id: int
):
    try:
        async with async_session_maker() as session:
            result = await session.execute(select(OrderGivenModel).
                                           where(OrderGivenModel.user_id == user_id))
            username_user = result.scalar()
            if username_user is not None:
                username = username_user.name
                return username
            else:
                pass
    except Exception as e:
        logger.critical(
            'Ошибка получение имени юзера по заказу по таблицу given', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'получение имени юзера по заказу по таблицу given:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


# получение телефона юзера по заказу
async def order_user_id_phone(
    user_id: int
):
    try:
        async with async_session_maker() as session:
            result = await session.execute(select(OrderModel).
                                           where(OrderModel.user_id == user_id))
        user_phone = result.scalar()
        if user_phone is not None:
            phone = user_phone.phone
            return phone
        else:
            pass
    except Exception as e:
        logger.critical(
            'Ошибка получение телефона юзера по заказу', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'получение телефона юзера по заказу:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


# получение даты заказа по заказу
async def order_user_id_date(
    user_id: int
):
    try:
        async with async_session_maker() as session:
            result = await session.execute(select(OrderModel).
                                           where(OrderModel.user_id == user_id))
        user_data = result.scalar()
        if user_data is not None:
            data = user_data.data
            return data
        else:
            pass
    except Exception as e:
        logger.critical(
            'Ошибка получение даты заказа по заказу', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'получение даты заказа по заказу:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


# Изменение даты по карзины для обновления
async def modify_date_order_id(user_id: int):
    try:
        async with async_session_maker() as session:
            stmt = update(OrderModel).where(OrderModel.user_id ==
                                            user_id).values({'data': datetime.now()})
            await session.execute(stmt)
            await session.commit()
    except Exception as e:
        logger.critical(
            f'Ошибка при изменении даты заказа для пользователя с ID {user_id}', exc_info=True)
        error_message = LEXICON_RU['Ошибка'] + \
            f'При изменении даты заказа для пользователя с ID {user_id}:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


# получение url юзера по заказу
async def order_user_id_url(
    user_id: int
):
    try:
        async with async_session_maker() as session:
            result = await session.execute(select(OrderModel).
                                           where(OrderModel.user_id == user_id))
        user_url = result.scalar()
        if user_url is not None:
            url = user_url.url
            return url
        else:
            pass
    except Exception as e:
        logger.critical(
            'Ошибка получение url юзера по заказу', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'получение url юзера по заказу:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


# получение color юзера по заказу
async def order_url_id_color(
    user_id: int
):
    try:
        async with async_session_maker() as session:
            result = await session.execute(select(OrderModel).
                                           where(OrderModel.user_id == user_id))
        user_color = result.scalar()
        if user_color is not None:
            color = user_color.color
            return color
        else:
            pass
    except Exception as e:
        logger.critical(
            'Ошибка получение color юзера по заказу', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'получение color юзера по заказу:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)

# получение адреса юзера по заказу


async def order_user_id_addres(
    user_id: int
):
    try:
        async with async_session_maker() as session:
            result = await session.execute(select(OrderModel).
                                           where(OrderModel.user_id == user_id))
            addres_user = result.scalar()
            if addres_user is not None:
                addres = addres_user.addres
                return addres
            else:
                pass
    except Exception as e:
        logger.critical(
            'Ошибка получение адреса юзера по заказу', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'получение адреса юзера по заказу:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


# получение имени юзера по заказу
async def order_user_id_username(
    user_id: int
):
    try:
        async with async_session_maker() as session:
            result = await session.execute(select(OrderModel).
                                           where(OrderModel.user_id == user_id))
            username_user = result.scalar()
            if username_user is not None:
                username = username_user.name
                return username
            else:
                pass
    except Exception as e:
        logger.critical(
            'Ошибка получение имени юзера по заказу', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'получение имени юзера по заказу:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


# получение стоимости доставки заказа
async def order_user_id_shipping_cost(
    user_id: int
):
    try:
        async with async_session_maker() as session:
            result = await session.execute(select(OrderModel).
                                           where(OrderModel.user_id == user_id))
            shipping_cost_user = result.scalar()
            if shipping_cost_user is not None:
                shipping_cost = shipping_cost_user.shipping_cost
                return shipping_cost
            else:
                pass
    except Exception as e:
        logger.critical(
            'Ошибка получение стоимости доставки заказа', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'получение стоимости доставки заказа:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


# Изменение телефона юзера по заказу по таблице Юзера
async def modify_phone_user_id(
    user_id: int,
    new_phone: str,
):
    try:
        async with async_session_maker() as session:
            new_phone = {'phone': new_phone}
            stmt = update(OrderGivenModel).where(
                OrderGivenModel.user_id == user_id).values(new_phone)
            await session.execute(stmt)
            await session.commit()
    except Exception as e:
        logger.critical(
            'Ошибка Изменение телефона юзера по заказу по таблице Юзера', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'Изменение телефона юзера по заказу по таблице Юзера:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


# Изменение Имени юзера по заказу по таблице Юзера
async def modify_username_user_id(
    user_id: int,
    new_name: str,
):
    try:
        async with async_session_maker() as session:
            new_name = {'name': new_name}
            stmt = update(OrderGivenModel).where(
                OrderGivenModel.user_id == user_id).values(new_name)
            await session.execute(stmt)
            await session.commit()
    except Exception as e:
        logger.critical(
            'Ошибка Изменение Имени юзера по заказу по таблице Юзера', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'Изменение Имени юзера по заказу по таблице Юзера:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


# Изменение адреса юзера по заказу по таблице Юзера
async def modify_addres_user_id(
    user_id: int,
    new_addres: str,
):
    try:
        async with async_session_maker() as session:
            new_addres = {'addres': new_addres}
            stmt = update(OrderGivenModel).where(
                OrderGivenModel.user_id == user_id).values(new_addres)
            await session.execute(stmt)
            await session.commit()
    except Exception as e:
        logger.critical(
            'Ошибка Изменение адреса юзера по заказу по таблице Юзера', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'Изменение Изменение адреса юзера по заказу по таблице Юзера:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


# Изменение телефона юзера по заказу по таблице Заказа
async def modify_phone_user_id_order(
    user_id: int,
    new_phone: str,
):
    try:
        async with async_session_maker() as session:
            new_phone = {'phone': new_phone}
            stmt = update(OrderModel).where(
                OrderModel.user_id == user_id).values(new_phone)
            await session.execute(stmt)
            await session.commit()
    except Exception as e:
        logger.critical(
            'Ошибка Изменение телефона юзера по заказу по таблице Заказа', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'Изменение телефона юзера по заказу по таблице Заказа:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


# Изменение Имени юзера по заказу по таблице Заказа
async def modify_username_user_id_order(
    user_id: int,
    new_name: str,
):
    try:
        async with async_session_maker() as session:
            new_name = {'name': new_name}
            stmt = update(OrderModel).where(
                OrderModel.user_id == user_id).values(new_name)
            await session.execute(stmt)
            await session.commit()
    except Exception as e:
        logger.critical(
            'Ошибка Изменение Имени юзера по заказу по таблице Заказаа', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'Изменение Имени юзера по заказу по таблице Заказа:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


# Изменение адреса юзера по заказу по таблице Заказа
async def modify_addres_user_id_order(
    user_id: int,
    new_addres: str,
):
    try:
        async with async_session_maker() as session:
            new_addres = {'addres': new_addres}
            stmt = update(OrderModel).where(
                OrderModel.user_id == user_id).values(new_addres)
            await session.execute(stmt)
            await session.commit()
    except Exception as e:
        logger.critical(
            'Ошибка Изменение адреса юзера по заказу по таблице Заказа', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'Изменение адреса юзера по заказу по таблице Заказа:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


# Удалить заказ
async def delete_order_user_id(
    user_id: int,
    order: int
):
    try:
        async with async_session_maker() as session:
            stmt = delete(OrderModel).where(
                and_(OrderModel.user_id == user_id, OrderModel.order == order))
            await session.execute(stmt)
            await session.commit()
    except Exception as e:
        logger.critical(
            'Ошибка Удалить заказ', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'Удалить заказ:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


# Сохранение заказа по номеру заказа
async def add_order_save(
    addres: str,
    url: str,
    color: str,
    round_value: int,
    phone: str,
    username: str,
    order: int,
    user_id: int,
    shipping_cost: int,
    user_link: int,
    price_rub: int,
):
    try:
        async with async_session_maker() as session:
            new_order = OrderModelSave(
                user_id=user_id,
                price=round_value,
                addres=addres,
                name=username,
                phone=phone,
                color=color,
                url=url,
                order=order,
                data=datetime.now(),
                shipping_cost=shipping_cost,
                user_link=user_link,
                price_rub=price_rub
            )
            session.add(new_order)
            await session.commit()
    except Exception as e:
        logger.critical(
            'Ошибка Сохранение заказа по номеру заказа', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'Сохранение заказа по номеру заказа:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


# Удалить заказ после формирования заказа
async def delete_order(
    user_id: int
):
    try:
        async with async_session_maker() as session:
            stmt = delete(OrderModel).where(
                and_(OrderModel.user_id == user_id))
            await session.execute(stmt)
            await session.commit()
    except Exception as e:
        logger.critical(
            'Ошибка Удалить заказ после формирования заказа', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'Удалить заказ после формирования заказа:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


# Получение заказа из сохраненой базы
async def add_save_order(
        user_id: int
):
    try:
        async with async_session_maker() as session:
            order = await session.execute(select(OrderModelSave).
                                          where(OrderModelSave.user_id == user_id))
            stmt = order.scalar()
            if stmt is not None:
                result = stmt.order
                return result
            else:
                pass
    except Exception as e:
        logger.critical(
            'Ошибка Получение заказа из сохраненой базы', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'Получение заказа из сохраненой базы:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


# получение заказа по сохраненым заказам
async def order_user_id_all_save(
    user_id: int
):
    try:
        async with async_session_maker() as session:
            result = await session.execute(select(OrderModelSave).
                                           where(OrderModelSave.user_id == user_id))
            price = result.mappings().all()
            return [{'id': row['OrderModelSave'].id,
                    'user_id': row['OrderModelSave'].user_id,
                     'price': row['OrderModelSave'].price,
                     'addres': row['OrderModelSave'].addres,
                     'name': row['OrderModelSave'].name,
                     'phone': row['OrderModelSave'].phone,
                     'color': row['OrderModelSave'].color,
                     'url': row['OrderModelSave'].url,
                     'order': row['OrderModelSave'].order,
                     'date': row['OrderModelSave'].data,
                     'shipping_cost': row['OrderModelSave'].shipping_cost, } for row in price]
    except Exception as e:
        logger.critical(
            'Ошибка получение заказа по сохраненым заказам', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'получение заказа по сохраненым заказам:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


# получение даты с сохраненных заказов
async def date_order_save(
        user_id: int
):
    try:
        async with async_session_maker() as session:
            result = await session.execute(select(OrderModelSave).
                                           where(OrderModelSave.user_id == user_id))
            stmt = result.scalar()
            if stmt is not None:
                result = stmt.data
                return result
            else:
                pass
    except Exception as e:
        logger.critical(
            'Ошибка получение даты с сохраненных заказов', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'получение даты с сохраненных заказов:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


# получение даты с корзины
async def date_order(
        user_id: int
):
    try:
        async with async_session_maker() as session:
            result = await session.execute(select(OrderModel).
                                           where(OrderModel.user_id == user_id))
            stmt = result.scalar()
            if stmt is not None:
                result = stmt.data
                return result
            else:
                pass
    except Exception as e:
        logger.critical(
            'Ошибка получение даты с корзины', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'получение даты с корзины:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


# Удаление месячных заказов
async def delete_old_order():
    async with async_session_maker() as session:
        date_now = datetime.now().date()
        date_old = date_now - timedelta(days=45)
        delete_order = delete(OrderModelSave).where(
            OrderModelSave.data < date_old)
        await session.execute(delete_order)
        await session.commit()
