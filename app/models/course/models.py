from sqlalchemy import Column, Integer, Date, Float
from config.database import Base


class CourseModel(Base):
    __tablename__ = "course"

    id = Column(Integer, primary_key=True)
    price = Column(Float)
    date = Column(Date)