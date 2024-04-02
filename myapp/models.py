from django.db import models
from django.utils import timezone


class OrderModel(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name="ID Заказа")
    user_id = models.BigIntegerField(verbose_name="ID Пользователя")
    order = models.BigIntegerField(verbose_name="Номер заказа")
    price = models.FloatField(verbose_name="Цена заказа в юанях")
    price_rub = models.FloatField(verbose_name="Цена заказа в рублях с учётом доставки")
    addres = models.CharField(max_length=255, verbose_name="Адрес доставки")
    name = models.CharField(max_length=255, verbose_name="ФИО клиента")
    phone = models.CharField(max_length=255, verbose_name="Номер телефона")
    color = models.CharField(max_length=255, verbose_name="Цвет и размер товара")
    url = models.CharField(max_length=255, verbose_name="Ссылка на товар")
    data = models.DateField(verbose_name="Дата заказа")
    shipping_cost = models.FloatField(verbose_name="Стоиомсть доставки")
    user_link = models.CharField(max_length=255, verbose_name="Ссылка на клиента")

    class Meta:
        managed = False
        db_table = 'save_order'
        verbose_name_plural = 'Заказы'
        ordering = ['-data']



class UserModel(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.BigIntegerField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'users'
        verbose_name_plural = 'Пользователи'


class UserOrderGivenModel(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.BigIntegerField()
    phone = models.CharField(max_length=255)
    addres = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'given_order'
        verbose_name_plural = 'Данные пользователя сделавший заказ'
        
