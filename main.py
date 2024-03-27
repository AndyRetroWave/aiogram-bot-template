from fastapi import FastAPI
from sqladmin import Admin, ModelView
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.models.users.models import UserModel
from app.models.order.models import OrderModel, OrderGivenModel, OrderModelSave
from config import engine, async_session_maker
import asyncio
import uvicorn

app = FastAPI()

admin =Admin(app,engine)

class UsersAdmin(ModelView, model=OrderGivenModel):
    column_list = [OrderGivenModel.name]

class OrderAdmin(ModelView, model=OrderModelSave):
    column_list = [OrderModelSave.name]

admin.add_view(UsersAdmin)
admin.add_view(OrderAdmin)

@app.get('/')
def index():
    return {'message': 'Hello, world!'}