# Generated by Django 5.0.3 on 2024-03-28 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrderModel',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('user_id', models.BigIntegerField()),
                ('price', models.FloatField()),
                ('addres', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('color', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=255)),
                ('order', models.BigIntegerField()),
                ('data', models.DateField()),
                ('shipping_cost', models.FloatField()),
            ],
            options={
                'db_table': 'save_order',
                'managed': False,
            },
        ),
    ]
