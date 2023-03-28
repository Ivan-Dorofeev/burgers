import decimal

from django.db import models
from django.core.validators import MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


def validate_even(value):
    if not isinstance(value, decimal.Decimal):
        raise ValidationError(f'Не верный тип данных: {value}/ Верный пример: 1235.66')
    elif value < 0:
        raise ValidationError(f'Значение не может быть отрицательным: {value}')


class Order(models.Model):
    firstname = models.CharField('Имя клиента', max_length=50, blank=False)
    lastname = models.CharField('Фамилия клиента', max_length=50, blank=False)
    phonenumber = PhoneNumberField(region='RU', blank=False)
    address = models.CharField('Андрес доставки', max_length=100, blank=False)

    class OrderChoise(models.TextChoices):
        NOT_READY = 'Не обработанный'
        READY = 'Обработан менеджером'

    order_status = models.CharField(max_length=20, choices=OrderChoise.choices, default=OrderChoise.NOT_READY)

    class Meta:
        db_table = 'orders'

    def __str__(self):
        return '%s ' % self.firstname


class OrderElements(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ', related_name='order_elements',
                              on_delete=models.CASCADE)

    product = models.ForeignKey(Product, verbose_name='Продукты', related_name='orders',
                                on_delete=models.CASCADE)
    quantity = models.IntegerField('Количество', default=1)
    coast = models.DecimalField('Стоимость заказа', decimal_places=2, validators=[validate_even],
                                max_digits=10000, blank=True, null=True)

    class Meta:
        db_table = 'order_elements'

    def __str__(self):
        return '%s - %s шт. ' % (self.product, self.quantity)
