from django.db import models
from django.utils import timezone


class OrderModel(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.BigIntegerField()
    price = models.FloatField()
    addres = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    order = models.BigIntegerField()
    data = models.DateField()
    shipping_cost = models.FloatField()

    class Meta:
        managed = False
        db_table = 'save_order'


class UserModel(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.BigIntegerField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'users'


class UserOrderGivenModel(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.BigIntegerField()
    phone = models.CharField(max_length=255)
    addres = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'given_order'
