from sqlalchemy import insert, select
from config.database import async_session_maker
from src.models.users.models import UserModel

async def add_user(first_name, last_name, username):
    async with async_session_maker() as session:
        user = UserModel(first_name=first_name, last_name=last_name, username=username)
        session.add(user)
        await session.commit()

        #     add_booking = (
        # insert(Bookings)
        # .values(
        #     room_id=room_id,
        #     user_id=user_id,
        #     date_from=date_from,
        #     date_to=date_to,
        #     price=get_price.scalar(),
        # )
        # .returning(Bookings)
        # )

        # new_booking = await session.execute(add_booking)
        # print(new_booking)
        # await session.commit()
        # return new_booking.scalar()