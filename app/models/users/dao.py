from sqlalchemy import insert, select
from config.database import async_session_maker
from app.models.users.models import UserModel


async def add_user(first_name, last_name, username, user_id):
    async with async_session_maker() as session:
        # Проверяем, существует ли уже пользователь с таким user_id
        existing_user = await session.execute(select(UserModel).filter_by(user_id=user_id))
        if existing_user.scalar() is not None:
            # Если пользователь уже существует, выводим сообщение и не производим запись
            print(
                f"Пользователь с user_id={user_id} уже существует в базе данных.")
            return

        # Если пользователь не существует, добавляем его в базу данных
        new_user = UserModel(
            first_name=first_name, last_name=last_name, username=username, user_id=user_id)
        session.add(new_user)
        await session.commit()
