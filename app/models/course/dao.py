from asyncio.log import logger
from sqlalchemy import delete, desc, select, func, update
from config.database import async_session_maker
from app.models.course.models import BankModel, CourseModel
import datetime


# Добовление курса юаня
async def add_course(price: int | float) -> None:
    """
    Функция добавляет новый курс юаня с текущей датой
    """
    async with async_session_maker() as session:
        today = datetime.date.today()
        new_course = CourseModel(price=price, date=today)
        session.add(new_course)
        await session.commit()


# Удаление курса юаня
async def delete_course():
    """
    Удаляет текущий курс юаня
    * подсвечивает вставляемые значения 
    DELETE FROM course
    WHERE id = (
        SELECT id
        FROM course
        ORDER BY date asc
        LIMIT 1
        );
    """
    async with async_session_maker() as session:
        subquery = select(CourseModel.id).order_by(
            CourseModel.date.asc()).limit(1)
        delete_query = delete(CourseModel).where(CourseModel.id.in_(subquery))
        await session.execute(delete_query)
        await session.commit()


# Получение текущего курса юаня
async def course_today():
    """
    Получает текущий курс юаня
    * подсвечивает вставляемые значения 
    SELECT *
    FROM course
    WHERE id = (
        SELECT MAX(id)
        FROM course
        );
    """
    async with async_session_maker() as session:
        subquery = await session.execute(select(func.max(CourseModel.id)))
        result = await session.execute(select(CourseModel).
                                       where(CourseModel.id == subquery.scalar()))
        try:
            price = result.scalar().price
            return price
        except:
            return None


# Добавление нового банка получателя
async def add_bank(bank):
    """
    Добавляет новый курс юаня с текущей датой
    """
    async with async_session_maker() as session:
        new_bank = BankModel(bank=bank)
        session.add(new_bank)
        await session.commit()


# Изменение банка получателя
async def modify_bank(bank):
    """
    Изменяет банк получателя
    * подсвечивает вставляемые значения 
    SELECT *
    FROM bank
    WHERE id == bank*
    """
    async with async_session_maker() as session:
        stmt = update(BankModel).where(BankModel.id == 1).values(bank=bank)
        await session.execute(stmt)
        await session.commit()


# Получение банка получателя
async def get_bank():
    """
    Получает банк 
    * подсвечивает вставляемые значения 
    SELECT *
    FROM bank
    """
    async with async_session_maker() as session:
        result = await session.execute(select(BankModel))
        try:
            bank = result.scalar().bank
            return bank
        except:
            return None


# Изменение номера телефона получателя
async def modify_phone_bank(phone):
    """
    Получает банк 
    * подсвечивает вставляемые значения 
    SELECT *
    FROM bank
    """
    async with async_session_maker() as session:
        stmt = update(BankModel).where(BankModel.id == 1).values(phone=phone)
        await session.execute(stmt)
        await session.commit()


# Получение номера телефона получателя
async def get_phone_bank():
    async with async_session_maker() as session:
        result = await session.execute(select(BankModel))
        try:
            phone = result.scalar().phone
            return phone
        except:
            return None
