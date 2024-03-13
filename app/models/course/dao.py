from sqlalchemy import select, func
from config.database import async_session_maker
from app.models.course.models import CourseModel
import datetime

async def add_course(price):
    async with async_session_maker() as session:
        today=datetime.date.today()
        new_course = CourseModel(price=price, date=today)
        session.add(new_course)
        await session.commit()

async def course_today():
    async with async_session_maker() as session:
        subquery = await session.execute(select(func.max(CourseModel.id)))
        result = await session.execute(select(CourseModel).where(CourseModel.id == subquery.scalar()))
        price = result.scalar().price
        return price

