from fastapi import FastAPI
from sqladmin import Admin, ModelView
from app.models.order.models import OrderGivenModel, OrderModelSave
from config import engine
from markupsafe import Markup

app = FastAPI()

admin =Admin(app,engine)

class UsersAdmin(ModelView, model=OrderGivenModel):
    column_list = [OrderGivenModel.name, OrderGivenModel.phone]
    name = "Данные пользователя"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"
    can_edit = True
    can_delete = True

class OrderAdmin(ModelView, model=OrderModelSave):
    column_list = [OrderModelSave.user_link, OrderModelSave.price, OrderModelSave.addres, OrderModelSave.color, OrderModelSave.url, OrderModelSave.data]
    icon = "fa-solid fa-wallet"
    name = "Данные о заказах"
    name_plural= "Заказы"
    can_edit = True
    can_delete = True

admin.add_view(UsersAdmin)
admin.add_view(OrderAdmin)

@app.get('/')
def index():
    return {'message': 'Hello, world!'}