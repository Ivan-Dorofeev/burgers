# Generated by Django 3.2.15 on 2023-04-11 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0059_alter_order_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment',
            field=models.CharField(choices=[('Наличкой', 'Cash'), ('Картой', 'Card')], db_index=True, max_length=10),
        ),
    ]
