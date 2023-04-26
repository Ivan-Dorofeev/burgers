# Generated by Django 3.2.15 on 2023-03-25 05:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0044_auto_20230321_1728'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='products',
        ),
        migrations.AddField(
            model_name='orderelements',
            name='order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='order', to='foodcartapp.order', verbose_name='Заказ'),
            preserve_default=False,
        ),
    ]