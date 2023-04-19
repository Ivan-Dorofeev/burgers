# Generated by Django 3.2.15 on 2023-03-12 09:21

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0037_auto_20210125_1833'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(max_length=50, verbose_name='Имя клиента')),
                ('client_surname', models.CharField(max_length=50, verbose_name='Фамилия клиента')),
                ('client_phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region='RU')),
                ('client_address', models.CharField(max_length=100, verbose_name='Андрес доставки')),
                ('products', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='foodcartapp.product', verbose_name='Заказ')),
            ],
            options={
                'db_table': 'orders',
            },
        ),
    ]
