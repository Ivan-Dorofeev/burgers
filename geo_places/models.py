from django.db import models


class Address(models.Model):
    name = models.CharField('Название адреса', max_length=500, unique=True)
    lon = models.FloatField('Долгота', blank=True, null=True)
    lat = models.FloatField('Широта', blank=True, null=True)
    date = models.DateTimeField('Дата обновления данных', auto_created=True, auto_now_add=True)

    class Meta:
        db_table = 'address'

    def __str__(self):
        return '%s (%s | %s) ' % (self.name, self.lon, self.lat)
