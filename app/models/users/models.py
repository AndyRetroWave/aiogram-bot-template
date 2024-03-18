from sqlalchemy import Column, Integer, String, BIGINT
from config.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_id = Column(BIGINT, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)