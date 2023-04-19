# Generated by Django 3.2.15 on 2023-04-19 05:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0062_rename_order_coast_orderelements_cost'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='order_register_at',
            new_name='order_registered_at',
        ),
        migrations.AlterField(
            model_name='orderelements',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10000, validators=[django.core.validators.MinValueValidator(limit_value=0)], verbose_name='Стоимость заказа'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='orderelements',
            name='quantity',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Количество'),
        ),
    ]
