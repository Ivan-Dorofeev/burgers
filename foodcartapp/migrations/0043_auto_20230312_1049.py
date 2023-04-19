# Generated by Django 3.2.15 on 2023-03-12 10:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0042_auto_20230312_1035'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderelements',
            old_name='count',
            new_name='quantity',
        ),
        migrations.RemoveField(
            model_name='orderelements',
            name='products',
        ),
        migrations.AddField(
            model_name='orderelements',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='order_elements', to='foodcartapp.product', verbose_name='Заказ'),
            preserve_default=False,
        ),
        migrations.AlterModelTable(
            name='orderelements',
            table='order_elements',
        ),
    ]
