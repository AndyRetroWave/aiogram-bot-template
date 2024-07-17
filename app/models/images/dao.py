from sqlalchemy import delete, desc, select, func
from config.database import async_session_maker
from app.models.images.models import ImageModel
import datetime


async def save_image(photo_id):
    """
    Эта функция используется для сохранения идентификатора изображения и текущей даты в базу данных.

    Параметры:
    photo_id: Идентификатор изображения.

    Возвращает:
    None

    SQL запрос:
    INSERT INTO ImageModel (file_id, data)
    VALUES (:photo_id, :today);
    """
    async with async_session_maker() as session:
        today = datetime.date.today()
        new_photo_id = ImageModel(file_id=photo_id, data=today)
        session.add(new_photo_id)
        await session.commit()


async def get_image():
    """
    Эта функция используется для получения последнего сохраненного идентификатора изображения из базы данных.

    Параметры:
    None

    Возвращает:
    image (str): Идентификатор изображения, если он существует.
    None: Если идентификатор изображения не найден.

    SQL запрос:
    SELECT file_id FROM ImageModel
    WHERE id = (SELECT MAX(id) FROM ImageModel);
    """
    async with async_session_maker() as session:
        subquery = await session.execute(select(func.max(ImageModel.id)))
        result = await session.execute(select(ImageModel).where(ImageModel.id == subquery.scalar()))
        try:
            image = result.scalar().file_id
            return image
        except:
            return None


async def delete_image():
    """
    Эта функция используется для удаления самого старого сохраненного идентификатора изображения из базы данных.

    Параметры:
    None

    Возвращает:
    None

    SQL запрос:
    DELETE FROM ImageModel
    WHERE id = (SELECT id FROM ImageModel ORDER BY data ASC LIMIT 1);
    """
    async with async_session_maker() as session:
        subquery = select(ImageModel.id).order_by(
            ImageModel.data.asc()).limit(1)
        delete_query = delete(ImageModel).where(ImageModel.id.in_(subquery))
        await session.execute(delete_query)
        await session.commit()
