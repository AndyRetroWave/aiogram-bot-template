from datetime import datetime
from sqlalchemy import delete, select, update, and_
from app.models.order.models import OrderModel
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

# получение заказа по юзеру
async def order_user_id_all(
    user_id: int
):
    async with async_session_maker() as session:
        result = await session.execute(select(OrderModel).where(OrderModel.user_id == user_id))
        price = result.mappings().all()
        return [{'id': row['OrderModel'].id,
                'price': row['OrderModel'].price, 
                'addres': row['OrderModel'].addres, 
                'name': row['OrderModel'].name, 
                'phone': row['OrderModel'].phone, 
                'color': row['OrderModel'].color, 
                'url': row['OrderModel'].url, 
                'order': row['OrderModel'].order, 
                'date': row['OrderModel'].data,
                'shipping_cost': row['OrderModel'].shipping_cost,} for row in price]
    

# получение телефона юзера
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


# получение url юзера
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

# получение color юзера
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

# получение адреса юзера
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


# получение имени юзера
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


# Изменение телефона юзера
async def modify_phone_user_id(
        user_id: int,
        new_phone: str,
    ):
    async with async_session_maker() as session:
        new_phone = {'phone': new_phone}
        stmt = update(OrderModel).where(OrderModel.user_id == user_id).values(new_phone)
        result = await session.execute(stmt)
        await session.commit()


# Изменение Имени юзера
async def modify_username_user_id(
        user_id: int,
        new_name: str,
    ):
    async with async_session_maker() as session:
        new_name = {'name': new_name}
        stmt = update(OrderModel).where(OrderModel.user_id == user_id).values(new_name)
        result = await session.execute(stmt)
        await session.commit()


# Изменение адреса юзера
async def modify_addres_user_id(
        user_id: int,
        new_addres: str,
    ):
    async with async_session_maker() as session:
        new_addres = {'addres': new_addres}
        stmt = update(OrderModel).where(OrderModel.user_id == user_id).values(new_addres)
        result = await session.execute(stmt)
        await session.commit()


# Удалить заказ
async def delete_order_user_id(
        user_id: int,
        order: int
    ):
    async with async_session_maker() as session:
        stmt = delete(OrderModel).where(and_(OrderModel.user_id == user_id, OrderModel.order == order))
        await session.execute(stmt)
        await session.commit()