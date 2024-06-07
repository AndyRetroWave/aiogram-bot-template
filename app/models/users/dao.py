import traceback
from sqlalchemy import select
from app.lexicon.lexicon_ru import LEXICON_RU
from config.database import async_session_maker
from app.models.users.models import UserModel
from config.config import logger
from config.config import bot
from config.config import settings


async def add_user(first_name, last_name, username, user_id):
    try:
        async with async_session_maker() as session:
            existing_user = await session.execute(select(UserModel).filter_by(user_id=user_id))
            if existing_user.scalar() is not None:
                return
            new_user = UserModel(
                first_name=first_name, last_name=last_name, username=username, user_id=user_id)
            session.add(new_user)
            await session.commit()
    except Exception as e:
        logger.critical(
            'Ошибка добавление данных в таблицу с юзерами', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'добавление данных в таблицу с юзерами:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


async def all_user():
    try:
        async with async_session_maker() as session:
            result = await session.execute(select(UserModel.user_id))
            users = result.scalars().all()
            return users
    except Exception as e:
        logger.critical(
            'Ошибка получения данных с юзерами', exc_info=True)
        error_message = LEXICON_RU["Ошибка"] + \
            f'получения данных с юзерами:\n{traceback.format_exc()}'
        await bot.send_message(chat_id=settings.ADMIN_ID2, text=error_message)


async def get_user(id):
    async with async_session_maker() as session:
        result = await session.execute(select(UserModel).where(UserModel.user_id == id))
        try:
            user = result.scalar().user_id
            return user
        except:
            return None
