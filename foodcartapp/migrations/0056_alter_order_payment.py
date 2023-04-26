# Generated by Django 3.2.15 on 2023-03-29 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0055_order_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment',
            field=models.CharField(choices=[('Наличкой', 'Cash'), ('Картой', 'Card')], db_index=True, default='Наличкой', max_length=10),
        ),
    ]