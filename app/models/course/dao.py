from asyncio.log import logger
from sqlalchemy import delete, desc, select, func, update
from config.database import async_session_maker
from app.models.course.models import BankModel, CourseModel
import datetime


async def add_course(price):
    async with async_session_maker() as session:
        today = datetime.date.today()
        new_course = CourseModel(price=price, date=today)
        session.add(new_course)
        await session.commit()


async def delete_course():
    async with async_session_maker() as session:
        subquery = select(CourseModel.id).order_by(
            CourseModel.date.asc()).limit(1)
        delete_query = delete(CourseModel).where(CourseModel.id.in_(subquery))
        await session.execute(delete_query)
        await session.commit()


async def course_today():
    async with async_session_maker() as session:
        subquery = await session.execute(select(func.max(CourseModel.id)))
        result = await session.execute(select(CourseModel).where(CourseModel.id == subquery.scalar()))
        try:
            price = result.scalar().price
            return price
        except:
            return None


async def add_bank(bank):
    async with async_session_maker() as session:
        new_bank = BankModel(bank=bank)
        session.add(new_bank)
        await session.commit()


async def modify_bank(bank):
    async with async_session_maker() as session:
        stmt = update(BankModel).where(BankModel.id == 1).values(bank=bank)
        await session.execute(stmt)
        await session.commit()


async def get_bank():
    async with async_session_maker() as session:
        result = await session.execute(select(BankModel))
        try:
            bank = result.scalar().bank
            return bank
        except:
            return None


async def modify_phone_bank(phone):
    async with async_session_maker() as session:
        stmt = update(BankModel).where(BankModel.id == 1).values(phone=phone)
        await session.execute(stmt)
        await session.commit()


async def get_phone_bank():
    async with async_session_maker() as session:
        result = await session.execute(select(BankModel))
        try:
            phone = result.scalar().phone
            return phone
        except:
            return None
