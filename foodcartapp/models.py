import decimal

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator


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


class Order(models.Model):
    class OrderChoise(models.TextChoices):
        NOT_READY = 'Не обработанный'
        READY = 'Обработан менеджером'

    class PaymentChoise(models.TextChoices):
        CASH = 'Наличкой'
        CARD = 'Картой'

    order_status = models.CharField(max_length=20, choices=OrderChoise.choices, default=OrderChoise.NOT_READY,
                                    db_index=True)
    firstname = models.CharField('Имя клиента', max_length=50)
    lastname = models.CharField('Фамилия клиента', max_length=50)
    phonenumber = PhoneNumberField(region='RU')
    address = models.CharField('Андрес доставки', max_length=100)
    comments = models.TextField('Комментарий к заказу', max_length=300, blank=True)
    order_registered_at = models.DateTimeField('Время регистрации заказа', auto_created=True, db_index=True)
    called_at = models.DateTimeField('Время уточнения заказа', blank=True, null=True)
    delivered_at = models.DateTimeField('Время доставки заказа', blank=True, null=True)
    payment = models.CharField(max_length=10, choices=PaymentChoise.choices, db_index=True)

    restaurant_that_cooks = models.ForeignKey(Restaurant, verbose_name='Будет готовить ресторан', related_name='order',
                                              on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'orders'

    def __str__(self):
        return '%s ' % self.firstname


class OrderElements(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ', related_name='order_elements',
                              on_delete=models.CASCADE)

    product = models.ForeignKey(Product, verbose_name='Продукты', related_name='orders',
                                on_delete=models.CASCADE)
    quantity = models.IntegerField('Количество', validators=[MinValueValidator(1)])
    cost = models.DecimalField('Стоимость заказа', decimal_places=2, validators=[MinValueValidator(limit_value=0)],
                               max_digits=4)

    class Meta:
        db_table = 'order_elements'

    def __str__(self):
        return '%s - %s шт. ' % (self.product, self.quantity)
