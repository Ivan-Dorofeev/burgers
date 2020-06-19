# Generated by Django 3.0.7 on 2020-06-19 09:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0007_auto_20200619_0849'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hotels', to='foodcartapp.City', verbose_name='город'),
        ),
    ]