from sqlalchemy import Column, Integer, BIGINT, DATE, String
from config.database import Base


class ImageModel(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    file_id = Column(String)
    data = Column(DATE)
