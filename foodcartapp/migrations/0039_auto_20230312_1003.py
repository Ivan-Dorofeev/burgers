# Generated by Django 3.2.15 on 2023-03-12 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0038_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='counts',
            field=models.IntegerField(default=1, verbose_name='Количество'),
        ),
        migrations.RemoveField(
            model_name='order',
            name='products',
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(related_name='order', to='foodcartapp.Product', verbose_name='Заказ'),
        ),
    ]