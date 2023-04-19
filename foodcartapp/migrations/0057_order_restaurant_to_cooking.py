# Generated by Django 3.2.15 on 2023-03-29 04:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0056_alter_order_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='restaurant_to_cooking',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order', to='foodcartapp.restaurant', verbose_name='Будет готовить ресторан'),
        ),
    ]
