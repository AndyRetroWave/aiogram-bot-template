from sqlalchemy import Column, Integer, Date, Float, ForeignKey, BIGINT, String, DATE
from config.database import Base


class OrderModel(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True)
    user_id = Column(BIGINT, ForeignKey('users.user_id'))
    price = Column(BIGINT)
    addres = Column(String)
    name = Column(String)
    phone = Column(String)
    color = Column(String)
    url = Column(String)
    order = Column(BIGINT)
    data = Column(DATE)
    shipping_cost = Column(BIGINT)


class OrderGivenModel(Base):
    __tablename__ = "given_order"
    id = Column(Integer, primary_key=True)
    user_id = Column(BIGINT, ForeignKey('users.user_id'))
    phone = Column(String)
    addres = Column(String)
    name = Column(String)