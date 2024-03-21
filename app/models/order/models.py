from sqlalchemy import Column, Integer, Date, Float, ForeignKey, BIGINT, String
from config.database import Base


class OrderModel(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True)
    user_id = Column(BIGINT, ForeignKey('users.id'))
    price = Column(BIGINT)
    addres = Column(String)
    name = Column(String)
    phone = Column(String)
    color = Column(String)
    url = Column(String)