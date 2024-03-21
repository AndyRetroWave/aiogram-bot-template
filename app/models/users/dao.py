from sqlalchemy import select
from config.database import async_session_maker
from app.models.users.models import UserModel
from config.config import logger


async def add_user(first_name, last_name, username, user_id):
    async with async_session_maker() as session:
        # Проверяем, существует ли уже пользователь с таким user_id
        existing_user = await session.execute(select(UserModel).filter_by(user_id=user_id))
        if existing_user.scalar() is not None:
            return

        # Если пользователь не существует, добавляем его в базу данных
        new_user = UserModel(
            first_name=first_name, last_name=last_name, username=username, user_id=user_id)
        session.add(new_user)
        logger.info(f"Пользователь {username} зарегестрировался в боте")
        await session.commit()

async def all_user():
    async with async_session_maker() as session:
        result = await session.execute(select(UserModel.user_id))
        users = result.scalars().all()
        return users

