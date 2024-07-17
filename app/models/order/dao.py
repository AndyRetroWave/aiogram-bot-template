from datetime import datetime, timedelta
import traceback
from sqlalchemy import delete, select, update, and_
from app.dependence.dependence import *
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
    """
    Эта функция используется для добавления нового заказа в базу данных.

    Параметры:
    addres (str): Адрес для доставки.
    url (str): URL продукта.
    color (str): Цвет продукта.
    round_value (int): Округленная цена продукта.
    phone (str): Номер телефона клиента.
    username (str): Имя пользователя клиента.
    order (int): Номер заказа.
    user_id (int): Идентификатор пользователя клиента.
    shipping_cost (int): Стоимость доставки.

    Возвращает:
    None

    SQL запрос:
    INSERT INTO OrderModel (user_id, price, addres, name, phone, color, url, order, data, shipping_cost)
    VALUES (:user_id, :round_value, :addres, :username, :phone, :color, :url, :order, :data, :shipping_cost);
    """
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
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Запись данных человека
async def add_diven_user(
    addres: str,
    phone: str,
    username: str,
    user_id: int,
):
    """
    Эта функция используется для добавления нового пользователя в базу данных.

    Параметры:
    addres (str): Адрес пользователя.
    phone (str): Номер телефона пользователя.
    username (str): Имя пользователя.
    user_id (int): Идентификатор пользователя.

    Возвращает:
    None

    SQL запрос:
    INSERT INTO OrderGivenModel (user_id, addres, name, phone)
    VALUES (:user_id, :addres, :username, :phone);
    """
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
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


async def order_user_id_all(
    user_id: int
):
    """
    Эта функция используется для извлечения всех заказов для заданного идентификатора пользователя из базы данных.

    Параметры:
    user_id (int): Идентификатор пользователя.

    Возвращает:
    List[OrderModel]: Список объектов OrderModel, представляющих заказы для указанного идентификатора пользователя.

    SQL запрос:
    SELECT * FROM OrderModel WHERE user_id = :user_id;
    """
    try:
        async with async_session_maker() as session:
            result = await session.execute(select(OrderModel).
                                           where(OrderModel.user_id == user_id))
            price = result.mappings().all()
            order_models = [d['OrderModel'] for d in price]
            return order_models
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Получение данных клиента
async def get_clien_data(
        user_id: int,
):
    """
    Получает данные клиента из базы данных по его идентификатору.

    Аргументы:
    user_id (int): Идентификатор пользователя.

    Возвращает:
    user: Объект пользователя, содержащий данные о клиенте.

    SQL запрос:
    SELECT * FROM OrderGivenModel WHERE user_id = :user_id;
    """
    try:
        async with async_session_maker() as session:
            result = await session.execute(select(OrderGivenModel).
                                           where(OrderGivenModel.user_id == user_id))
        user = result.scalar()
        return user
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Изменение телефона юзера по заказу по таблице Юзера
async def modify_phone_user_id(
    user_id: int,
    new_phone: str,
):
    """
    Эта функция используется для изменения номера телефона заданного идентификатора пользователя в базе данных.

    Параметры:
    user_id (int): Идентификатор пользователя.
    new_phone (str): Новый номер телефона для обновления.

    Возвращает:
    None

    SQL запрос:
    UPDATE OrderGivenModel
    SET phone = :new_phone
    WHERE user_id = :user_id;
    """
    try:
        async with async_session_maker() as session:
            new_phone = {'phone': new_phone}
            stmt = update(OrderGivenModel).where(
                OrderGivenModel.user_id == user_id).values(new_phone)
            await session.execute(stmt)
            await session.commit()
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Изменение Имени юзера по заказу по таблице Юзера
async def modify_username_user_id(
    user_id: int,
    new_name: str,
):
    """
    Эта функция используется для изменения имени пользователя для заданного идентификатора пользователя в базе данных.

    Параметры:
    user_id (int): Идентификатор пользователя.
    new_name (str): Новое имя пользователя для обновления.

    Возвращает:
    None

    SQL запрос:
    UPDATE OrderGivenModel
    SET name = :new_name
    WHERE user_id = :user_id;
    """
    try:
        async with async_session_maker() as session:
            new_name = {'name': new_name}
            stmt = update(OrderGivenModel).where(
                OrderGivenModel.user_id == user_id).values(new_name)
            await session.execute(stmt)
            await session.commit()
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Изменение адреса юзера по заказу по таблице Юзера
async def modify_addres_user_id(
    user_id: int,
    new_addres: str,
):
    """
    Эта функция используется для изменения адреса для заданного идентификатора пользователя в базе данных.

    Параметры:
    user_id (int): Идентификатор пользователя.
    new_addres (str): Новый адрес для обновления.

    Возвращает:
    None

    SQL запрос:
    UPDATE OrderGivenModel
    SET addres = :new_addres
    WHERE user_id = :user_id;
    """
    try:
        async with async_session_maker() as session:
            new_addres = {'addres': new_addres}
            stmt = update(OrderGivenModel).where(
                OrderGivenModel.user_id == user_id).values(new_addres)
            await session.execute(stmt)
            await session.commit()
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Изменение телефона юзера по заказу по таблице Заказа
async def modify_phone_user_id_order(
    user_id: int,
    new_phone: str,
):
    """
    Эта функция используется для изменения номера телефона заказа для заданного идентификатора пользователя в базе данных.

    Параметры:
    user_id (int): Идентификатор пользователя.
    new_phone (str): Новый номер телефона для обновления.

    Возвращает:
    None

    SQL запрос:
    UPDATE OrderModel
    SET phone = :new_phone
    WHERE user_id = :user_id;
    """
    try:
        async with async_session_maker() as session:
            new_phone = {'phone': new_phone}
            stmt = update(OrderModel).where(
                OrderModel.user_id == user_id).values(new_phone)
            await session.execute(stmt)
            await session.commit()
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Изменение Имени юзера по заказу по таблице Заказа
async def modify_username_user_id_order(
    user_id: int,
    new_name: str,
):
    """
    Эта функция используется для изменения имени пользователя заказа для заданного идентификатора пользователя в базе данных.

    Параметры:
    user_id (int): Идентификатор пользователя.
    new_name (str): Новое имя пользователя для обновления.

    Возвращает:
    None

    SQL запрос:
    UPDATE OrderModel
    SET name = :new_name
    WHERE user_id = :user_id;
    """
    try:
        async with async_session_maker() as session:
            new_name = {'name': new_name}
            stmt = update(OrderModel).where(
                OrderModel.user_id == user_id).values(new_name)
            await session.execute(stmt)
            await session.commit()
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Изменение адреса юзера по заказу по таблице Заказа
async def modify_addres_user_id_order(
    user_id: int,
    new_addres: str,
):
    """
    Эта функция используется для изменения адреса заказа для заданного идентификатора пользователя в базе данных.

    Параметры:
    user_id (int): Идентификатор пользователя.
    new_addres (str): Новый адрес для обновления.

    Возвращает:
    None

    SQL запрос:
    UPDATE OrderModel
    SET addres = :new_addres
    WHERE user_id = :user_id;
    """
    try:
        async with async_session_maker() as session:
            new_addres = {'addres': new_addres}
            stmt = update(OrderModel).where(
                OrderModel.user_id == user_id).values(new_addres)
            await session.execute(stmt)
            await session.commit()
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Удалить заказ
async def delete_order_user_id(
    user_id: int,
    order: int
):
    """
    Эта функция используется для удаления заказа для заданного идентификатора пользователя и номера заказа из базы данных.

    Параметры:
    user_id (int): Идентификатор пользователя.
    order (int): Номер заказа.

    Возвращает:
    None

    SQL запрос:
    DELETE FROM OrderModel
    WHERE user_id = :user_id AND order = :order;
    """
    try:
        async with async_session_maker() as session:
            stmt = delete(OrderModel).where(
                and_(OrderModel.user_id == user_id, OrderModel.order == order))
            await session.execute(stmt)
            await session.commit()
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


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
    """
    Эта функция используется для добавления нового сохраненного заказа в базу данных.

    Параметры:
    addres (str): Адрес для доставки.
    url (str): URL продукта.
    color (str): Цвет продукта.
    round_value (int): Округленная цена продукта.
    phone (str): Номер телефона клиента.
    username (str): Имя пользователя клиента.
    order (int): Номер заказа.
    user_id (int): Идентификатор пользователя клиента.
    shipping_cost (int): Стоимость доставки.
    user_link (int): Ссылка на пользователя.
    price_rub (int): Цена в рублях.

    Возвращает:
    None

    SQL запрос:
    INSERT INTO OrderModelSave (user_id, price, addres, name, phone, color, url, order, data, shipping_cost, user_link, price_rub)
    VALUES (:user_id, :round_value, :addres, :username, :phone, :color, :url, :order, :data, :shipping_cost, :user_link, :price_rub);
    """
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
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Удалить заказ после формирования заказа
async def delete_order(
    user_id: int
):
    """
    Эта функция используется для удаления всех заказов для заданного идентификатора пользователя из базы данных.

    Параметры:
    user_id (int): Идентификатор пользователя.

    Возвращает:
    None

    SQL запрос:
    DELETE FROM OrderModel
    WHERE user_id = :user_id;
    """
    try:
        async with async_session_maker() as session:
            stmt = delete(OrderModel).where(
                and_(OrderModel.user_id == user_id))
            await session.execute(stmt)
            await session.commit()
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Получение заказа из сохраненой базы
async def add_save_order(
        user_id: int
):
    """
    Эта функция используется для получения сохраненного заказа для заданного идентификатора пользователя из базы данных.

    Параметры:
    user_id (int): Идентификатор пользователя.

    Возвращает:
    result (int): Номер сохраненного заказа, если он существует.
    None: Если сохраненный заказ не найден.

    SQL запрос:
    SELECT * FROM OrderModelSave
    WHERE user_id = :user_id;
    """
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
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# получение заказа по сохраненым заказам
async def get_user_id_all_save(
    user_id: int
):
    """
    Эта функция используется для удаления всех заказов для заданного идентификатора пользователя из базы данных.

    Параметры:
    user_id (int): Идентификатор пользователя.

    Возвращает:
    None

    SQL запрос:
    DELETE FROM OrderModel
    WHERE user_id = :user_id;
    """
    try:
        async with async_session_maker() as session:
            result = await session.execute(select(OrderModelSave).
                                           where(OrderModelSave.user_id == user_id))
            data = result.mappings().all()
            order_models = [d['OrderModelSave'] for d in data]
            return order_models
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


# Удаление месячных заказов
async def delete_old_order():
    """
    Эта функция используется для удаления всех сохраненных заказов, которые старше 45 дней, из базы данных.

    Параметры:
    None

    Возвращает:
    None

    SQL запрос:
    DELETE FROM OrderModelSave
    WHERE data < :date_old;
    """
    async with async_session_maker() as session:
        date_now = datetime.now().date()
        date_old = date_now - timedelta(days=45)
        delete_order = delete(OrderModelSave).where(
            OrderModelSave.data < date_old)
        await session.execute(delete_order)
        await session.commit()
