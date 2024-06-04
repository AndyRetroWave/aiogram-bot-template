from sqlalchemy import delete, desc, select, func
from config.database import async_session_maker
from app.models.images.models import ImageModel
import datetime


async def save_image(photo_id):
    async with async_session_maker() as session:
        today = datetime.date.today()
        new_photo_id = ImageModel(file_id=photo_id, data=today)
        session.add(new_photo_id)
        await session.commit()


async def get_image():
    async with async_session_maker() as session:
        subquery = await session.execute(select(func.max(ImageModel.id)))
        result = await session.execute(select(ImageModel).where(ImageModel.id == subquery.scalar()))
        try:
            image = result.scalar().file_id
            return image
        except:
            return None


async def delete_image():
    async with async_session_maker() as session:
        subquery = select(ImageModel.id).order_by(
            ImageModel.data.asc()).limit(1)
        delete_query = delete(ImageModel).where(ImageModel.id.in_(subquery))
        await session.execute(delete_query)
        await session.commit()
