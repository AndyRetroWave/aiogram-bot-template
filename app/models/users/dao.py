import traceback
from sqlalchemy import select
from app.dependence.dependence import logger_error_critical_send_message_admin
from app.lexicon.lexicon_ru import LEXICON_RU
from config.database import async_session_maker
from app.models.users.models import UserModel
from config.config import logger
from config.config import bot
from config.config import settings


async def add_user(first_name, last_name, username, user_id):
    """
    Эта функция используется для добавления нового пользователя в базу данных, если он еще не существует.

    Параметры:
    first_name (str): Имя пользователя.
    last_name (str): Фамилия пользователя.
    username (str): Имя пользователя в Telegram.
    user_id (int): Идентификатор пользователя в Telegram.

    Возвращает:
    None

    SQL запрос:
    INSERT INTO UserModel (first_name, last_name, username, user_id)
    VALUES (:first_name, :last_name, :username, :user_id);
    """
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
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


async def all_user():
    """
    Эта функция используется для получения списка всех идентификаторов пользователей из базы данных.

    Параметры:
    None

    Возвращает:
    users (list): Список идентификаторов пользователей.

    SQL запрос:
    SELECT user_id FROM UserModel;
    """
    try:
        async with async_session_maker() as session:
            result = await session.execute(select(UserModel.user_id))
            users = result.scalars().all()
            return users
    except Exception as e:
        await logger_error_critical_send_message_admin(
            bot=bot, logger=logger, traceback=traceback
        )


async def get_user(id):
    """
    Эта функция используется для получения идентификатора пользователя из базы данных по заданному идентификатору.

    Параметры:
    id (int): Идентификатор пользователя.

    Возвращает:
    user (int): Идентификатор пользователя, если он существует.
    None: Если идентификатор пользователя не найден.

    SQL запрос:
    SELECT user_id FROM UserModel WHERE user_id = :id;
    """
    async with async_session_maker() as session:
        result = await session.execute(select(UserModel).where(UserModel.user_id == id))
        try:
            try:
                user = result.scalar().user_id
                return user
            except:
                return None
        except Exception as e:
            await logger_error_critical_send_message_admin(
                bot=bot, logger=logger, traceback=traceback
            )
