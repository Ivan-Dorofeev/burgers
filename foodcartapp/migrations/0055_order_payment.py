# Generated by Django 3.2.15 on 2023-03-29 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0054_auto_20230329_0414'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.CharField(choices=[('Наличкой', 'Cash'), ('Картой', 'Card')], default='Наличкой', max_length=10),
        ),
    ]
