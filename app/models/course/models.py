from sqlalchemy import Column, Integer, Date, Float, String
from config.database import Base


class CourseModel(Base):
    __tablename__ = "course"

    id = Column(Integer, primary_key=True)
    price = Column(Float)
    date = Column(Date)


class BankModel(Base):
    __tablename__ = "bank"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    data = Column(Date)
