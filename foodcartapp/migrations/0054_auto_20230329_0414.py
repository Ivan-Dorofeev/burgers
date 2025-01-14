# Generated by Django 3.2.15 on 2023-03-29 04:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0053_alter_order_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='called_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Время уточнения заказа'),
        ),
        migrations.AddField(
            model_name='order',
            name='delivered_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Время доставки заказа'),
        ),
        migrations.AddField(
            model_name='order',
            name='register_at',
            field=models.DateTimeField(auto_created=True, db_index=True, default=django.utils.timezone.now, verbose_name='Время регистрации заказа'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('Не обработанный', 'Not Ready'), ('Обработан менеджером', 'Ready')], db_index=True, default='Не обработанный', max_length=20),
        ),
    ]
