from fastapi import FastAPI
from sqladmin import Admin, ModelView
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.models.users.models import UserModel
from config import engine, async_session_maker
import asyncio
import uvicorn

app = FastAPI()

admin =Admin(app,engine)

# Создаем объект администрирования
class UsersAdmin(ModelView, model=UserModel):
    column_list = [UserModel.first_name, UserModel.last_name]

class OrderAdmin(ModelView, model=UserModel):
    column_list = [UserModel.first_name, UserModel.last_name]


admin.add_view(UsersAdmin)

@app.get('/')
def index():
    return {'message': 'Hello, world!'}