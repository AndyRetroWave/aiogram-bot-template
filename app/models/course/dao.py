from asyncio.log import logger
import traceback
from sqlalchemy import delete, desc, select, func, update
from app.dependence.dependence import *
from config.database import async_session_maker
from app.models.course.models import BankModel, CourseModel
import datetime
from config.config import bot


# Добовление курса юаня
async def add_course(price: int | float) -> None:
    """
    Эта функция используется для добавления нового курса юаня с текущей датой в базу данных.

    Параметры:
    price (int | float): Курс юаня.

    Возвращает:
    None

    SQL запрос:
    INSERT INTO CourseModel (price, date)
    VALUES (:price, :today);
    """
    async with async_session_maker() as session:
        try:
            today = datetime.date.today()
            new_course = CourseModel(price=price, date=today)
            session.add(new_course)
            await session.commit()
        except Exception as e:
            await logger_error_critical_send_message_admin(
                bot=bot, logger=logger, traceback=traceback
            )


# Удаление курса юаня
async def delete_course():
    """
    Эта функция используется для удаления самого старого курса юаня из базы данных.

    Параметры:
    None

    Возвращает:
    None

    SQL запрос:
    DELETE FROM CourseModel
    WHERE id = (SELECT id FROM CourseModel ORDER BY date ASC LIMIT 1);
    """
    async with async_session_maker() as session:
        try:
            subquery = select(CourseModel.id).order_by(
                CourseModel.date.asc()).limit(1)
            delete_query = delete(CourseModel).where(
                CourseModel.id.in_(subquery))
            await session.execute(delete_query)
            await session.commit()
        except Exception as e:
            await logger_error_critical_send_message_admin(
                bot=bot, logger=logger, traceback=traceback
            )


# Получение текущего курса юаня
async def course_today():
    """
    Эта функция используется для получения текущего курса юаня из базы данных.

    Параметры:
    None

    Возвращает:
    price (float): Текущий курс юаня, если он существует.
    None: Если текущий курс юаня не найден.

    SQL запрос:
    SELECT price FROM CourseModel
    WHERE id = (SELECT MAX(id) FROM CourseModel);
    """
    async with async_session_maker() as session:
        try:
            subquery = await session.execute(select(func.max(CourseModel.id)))
            result = await session.execute(select(CourseModel).
                                           where(CourseModel.id == subquery.scalar()))
            try:
                price = result.scalar().price
                return price
            except:
                return None
        except Exception as e:
            await logger_error_critical_send_message_admin(
                bot=bot, logger=logger, traceback=traceback
            )


# Добавление нового банка получателя
async def add_bank(bank):
    """
    Эта функция используется для добавления нового банка в базу данных.

    Параметры:
    bank (str): Название банка.

    Возвращает:
    None

    SQL запрос:
    INSERT INTO BankModel (bank)
    VALUES (:bank);
    """
    async with async_session_maker() as session:
        try:
            new_bank = BankModel(bank=bank)
            session.add(new_bank)
            await session.commit()
        except Exception as e:
            await logger_error_critical_send_message_admin(
                bot=bot, logger=logger, traceback=traceback
            )


# Изменение банка получателя
async def modify_bank(bank):
    """
    Эта функция используется для изменения названия банка в базе данных.

    Параметры:
    bank (str): Новое название банка.

    Возвращает:
    None

    SQL запрос:
    UPDATE BankModel
    SET bank = :bank
    WHERE id = 1;
    """
    async with async_session_maker() as session:
        try:
            stmt = update(BankModel).where(BankModel.id == 1).values(bank=bank)
            await session.execute(stmt)
            await session.commit()
        except Exception as e:
            await logger_error_critical_send_message_admin(
                bot=bot, logger=logger, traceback=traceback
            )


# Получение банка получателя
async def get_bank():
    """
    Эта функция используется для получения названия банка из базы данных.

    Параметры:
    None

    Возвращает:
    bank (str): Название банка, если оно существует.
    None: Если название банка не найдено.

    SQL запрос:
    SELECT bank FROM BankModel;
    """
    async with async_session_maker() as session:
        try:
            result = await session.execute(select(BankModel))
            try:
                bank = result.scalar().bank
                return bank
            except:
                return None
        except Exception as e:
            await logger_error_critical_send_message_admin(
                bot=bot, logger=logger, traceback=traceback
            )


# Изменение номера телефона получателя
async def modify_phone_bank(phone):
    """
    Эта функция используется для изменения номера телефона банка в базе данных.

    Параметры:
    phone (str): Новый номер телефона банка.

    Возвращает:
    None

    SQL запрос:
    UPDATE BankModel
    SET phone = :phone
    WHERE id = 1;
    """
    async with async_session_maker() as session:
        try:
            stmt = update(BankModel).where(
                BankModel.id == 1).values(phone=phone)
            await session.execute(stmt)
            await session.commit()
        except Exception as e:
            await logger_error_critical_send_message_admin(
                bot=bot, logger=logger, traceback=traceback
            )


# Получение номера телефона получателя
async def get_phone_bank():
    """
    Эта функция используется для получения номера телефона банка из базы данных.

    Параметры:
    None

    Возвращает:
    phone (str): Номер телефона банка, если он существует.
    None: Если номер телефона банка не найден.

    SQL запрос:
    SELECT phone FROM BankModel;
    """
    async with async_session_maker() as session:
        try:
            result = await session.execute(select(BankModel))
            try:
                phone = result.scalar().phone
                return phone
            except:
                return None
        except Exception as e:
            await logger_error_critical_send_message_admin(
                bot=bot, logger=logger, traceback=traceback
            )
