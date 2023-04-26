# Generated by Django 3.2.15 on 2023-03-28 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0050_auto_20230325_0940'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('Не обработанный', 'Not Ready'), ('Обработан менеджером', 'Ready')], default='Не обработанный', max_length=20),
        ),
    ]