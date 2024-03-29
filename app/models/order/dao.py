from datetime import datetime
from sqlalchemy import delete, select, update, and_
from app.models.order.models import OrderGivenModel, OrderModel, OrderModelSave
from config.database import async_session_maker

from config.config import logger

# добавление заказа
async def add_order(
    addres: str,
    url: str,
    color: str,
    round_value: int,
    phone: str,
    username: str,
    order: int,
    user_id: int,
    shipping_cost: int,
):
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
            shipping_cost=shipping_cost
        )
        session.add(new_order)
        logger.info(f"Пользователь {username} сохранил заказ в базе данных")
        await session.commit()


# Запись данных человека
async def add_diven_user(
    addres: str,
    phone: str,
    username: str,
    user_id: int,
):
    async with async_session_maker() as session:
        new_user = OrderGivenModel(
            user_id=user_id,
            addres=addres,
            name=username,
            phone=phone,
        )
        session.add(new_user)
        await session.commit()


# получение заказа по юзеру
async def order_user_id_all(
    user_id: int
):
    async with async_session_maker() as session:
        result = await session.execute(select(OrderModel).where(OrderModel.user_id == user_id))
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
                'shipping_cost': row['OrderModel'].shipping_cost, } for row in price]


# Получение телефона юзера по таблице given 
async def phone_user_id_given(
        user_id: int,
        ):
    async with async_session_maker() as session:
        result = await session.execute(select(OrderGivenModel).where(OrderGivenModel.user_id == user_id))
    user_phone = result.scalar()
    if user_phone is not None:
        phone = user_phone.phone
        return phone
    else:
        pass


# получение адреса юзера по таблице given
async def addres_user_id_given(
    user_id: int
):
    async with async_session_maker() as session:
        result = await session.execute(select(OrderGivenModel).where(OrderGivenModel.user_id == user_id))
        addres_user = result.scalar()
        if addres_user is not None:
            addres = addres_user.addres
            return addres
        else:
            pass


# получение имени юзера по заказу по таблицу given 
async def username_user_id_given(
    user_id: int
):
    async with async_session_maker() as session:
        result = await session.execute(select(OrderGivenModel).where(OrderGivenModel.user_id == user_id))
        username_user = result.scalar()
        if username_user is not None:
            username = username_user.name
            return username
        else:
            pass


# получение телефона юзера по заказу
async def order_user_id_phone(
    user_id: int
):
    async with async_session_maker() as session:
        result = await session.execute(select(OrderModel).where(OrderModel.user_id == user_id))
    user_phone = result.scalar()
    if user_phone is not None:
        phone = user_phone.phone
        return phone
    else:
        pass


# получение url юзера по заказу
async def order_user_id_url(
    user_id: int
):
    async with async_session_maker() as session:
        result = await session.execute(select(OrderModel).where(OrderModel.user_id == user_id))
    user_url = result.scalar()
    if user_url is not None:
        url = user_url.url
        return url
    else:
        pass


# получение color юзера по заказу
async def order_url_id_color(
    user_id: int
):
    async with async_session_maker() as session:
        result = await session.execute(select(OrderModel).where(OrderModel.user_id == user_id))
    user_color = result.scalar()
    if user_color is not None:
        color = user_color.color
        return color
    else:
        pass


# получение адреса юзера по заказу
async def order_user_id_addres(
    user_id: int
):
    async with async_session_maker() as session:
        result = await session.execute(select(OrderModel).where(OrderModel.user_id == user_id))
        addres_user = result.scalar()
        if addres_user is not None:
            addres = addres_user.addres
            return addres
        else:
            pass


# получение имени юзера по заказу
async def order_user_id_username(
    user_id: int
):
    async with async_session_maker() as session:
        result = await session.execute(select(OrderModel).where(OrderModel.user_id == user_id))
        username_user = result.scalar()
        if username_user is not None:
            username = username_user.name
            return username
        else:
            pass


# получение стоимости доставки заказа
async def order_user_id_shipping_cost(
    user_id: int
):
    async with async_session_maker() as session:
        result = await session.execute(select(OrderModel).where(OrderModel.user_id == user_id))
        shipping_cost_user = result.scalar()
        if shipping_cost_user is not None:
            shipping_cost = shipping_cost_user.shipping_cost
            return shipping_cost
        else:
            pass


# Изменение телефона юзера по заказу по таблице Юзера 
async def modify_phone_user_id(
    user_id: int,
    new_phone: str,
):
    async with async_session_maker() as session:
        new_phone = {'phone': new_phone}
        stmt = update(OrderGivenModel).where(
            OrderGivenModel.user_id == user_id).values(new_phone)
        result = await session.execute(stmt)
        await session.commit()


# Изменение Имени юзера по заказу по таблице Юзера
async def modify_username_user_id(
    user_id: int,
    new_name: str,
):
    async with async_session_maker() as session:
        new_name = {'name': new_name}
        stmt = update(OrderGivenModel).where(
            OrderGivenModel.user_id == user_id).values(new_name)
        result = await session.execute(stmt)
        await session.commit()


# Изменение адреса юзера по заказу по таблице Юзера
async def modify_addres_user_id(
    user_id: int,
    new_addres: str,
):
    async with async_session_maker() as session:
        new_addres = {'addres': new_addres}
        stmt = update(OrderGivenModel).where(
            OrderGivenModel.user_id == user_id).values(new_addres)
        result = await session.execute(stmt)
        await session.commit()


# Изменение телефона юзера по заказу по таблице Заказа
async def modify_phone_user_id_order(
    user_id: int,
    new_phone: str,
):
    async with async_session_maker() as session:
        new_phone = {'phone': new_phone}
        stmt = update(OrderModel).where(
            OrderModel.user_id == user_id).values(new_phone)
        result = await session.execute(stmt)
        await session.commit()


# Изменение Имени юзера по заказу по таблице Заказа
async def modify_username_user_id_order(
    user_id: int,
    new_name: str,
):
    async with async_session_maker() as session:
        new_name = {'name': new_name}
        stmt = update(OrderModel).where(
            OrderModel.user_id == user_id).values(new_name)
        result = await session.execute(stmt)
        await session.commit()


# Изменение адреса юзера по заказу по таблице Заказа
async def modify_addres_user_id_order(
    user_id: int,
    new_addres: str,
):
    async with async_session_maker() as session:
        new_addres = {'addres': new_addres}
        stmt = update(OrderModel).where(
            OrderModel.user_id == user_id).values(new_addres)
        result = await session.execute(stmt)
        await session.commit()


# Удалить заказ
async def delete_order_user_id(
    user_id: int,
    order: int
):
    async with async_session_maker() as session:
        stmt = delete(OrderModel).where(
            and_(OrderModel.user_id == user_id, OrderModel.order == order))
        await session.execute(stmt)
        await session.commit()


# Сохранение заказа по номеру заказа
async def add_order_save(
    addres: str,
    url: str,
    color: str,
    round_value: int,
    phone: str,
    username: str,
    order: int,
    date: datetime,
    user_id: int,
    shipping_cost: int,
    user_link: int,
):
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
            data=date,
            shipping_cost=shipping_cost,
            user_link=user_link
        )
        session.add(new_order)
        logger.info(f"Пользователь {username} сохранил заказ в базе данных")
        await session.commit()


# Удалить заказ после формирования заказа
async def delete_order(
    user_id: int
):
    async with async_session_maker() as session:
        stmt = delete(OrderModel).where(
            and_(OrderModel.user_id == user_id))
        await session.execute(stmt)
        await session.commit()

# Получение заказа из сохраненой базы
async def add_save_order(
        user_id: int
        ):
    async with async_session_maker() as session:
        order = await session.execute(select(OrderModelSave).where(OrderModelSave.user_id == user_id))
        stmt = order.scalar()
        if stmt is not None:
            result = stmt.order
            return result
        else:
            pass


# получение заказа по сохраненым заказам
async def order_user_id_all_save(
    user_id: int
):
    async with async_session_maker() as session:
        result = await session.execute(select(OrderModelSave).where(OrderModelSave.user_id == user_id))
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