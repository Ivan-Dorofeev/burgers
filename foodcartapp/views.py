import json
import traceback

from django.db import transaction
from django.http import JsonResponse
from django.templatetags.static import static
from phonenumber_field.phonenumber import PhoneNumber
from rest_framework import status, serializers
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.fields import ListField
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.serializers import ValidationError, Serializer, ModelSerializer
from rest_framework.renderers import JSONRenderer

from .models import Product, Order, OrderElements


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


class OrderDeSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ['firstname', 'lastname', 'phonenumber', 'address']

    def validate_phonenumber(self, value):
        if not PhoneNumber.from_string(value).is_valid():
            raise ValidationError('Введен некорректный номер телефона.')
        return value

    def validate_products(self, values):
        if not values:
            raise ValidationError(f'Этот список не может быть пустым.')

        order_product_ids = Product.objects.all()
        for value in values:
            if not value in order_product_ids:
                raise ValidationError(f'Недопустимый первичный ключ {value["product"]}')
        return values


class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=1)
    firstname = serializers.CharField(required=True, allow_blank=True, max_length=100)
    lastname = serializers.CharField(required=True, allow_blank=True, max_length=100)
    phonenumber = serializers.CharField(required=True)
    address = serializers.CharField(required=True, allow_blank=True, max_length=100)

    def create(self, validated_data):
        return Order.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.title)
        instance.firstname = validated_data.get('firstname', instance.title)
        instance.lastname = validated_data.get('lastname', instance.code)
        instance.phonenumber = validated_data.get('phonenumber', instance.linenos)
        instance.address = validated_data.get('address', instance.language)
        instance.save()


@api_view(['POST'])
# @transaction.atomic
def register_order(request):
    try:
        with transaction.atomic():
            get_orders = request.data
            print('orders = ', get_orders)

            """Десериализация"""
            deserializer = OrderDeSerializer(data=get_orders)
            deserializer.is_valid(raise_exception=True)
            print('deserializer = ', deserializer)
            print('deserializer.data = ', deserializer.data)

            """Запись в БД"""
            order = Order.objects.create(
                firstname=get_orders['firstname'],
                lastname=get_orders['lastname'],
                phonenumber=get_orders['phonenumber'],
                address=get_orders['address'],
            )
            print('order = ', order)
            print('order.id = ', order.id)
            for product in get_orders['products']:
                product_by_id = Product.objects.get(id=int(product['product']))
                product_quantity = product['quantity']

                new_product = OrderElements.objects.create(order=order, product=product_by_id, quantity=product_quantity)
                print('new_product = ', new_product)

            deserializered_order = deserializer.data
            deserializered_order['id'] = order.id

            """Сериализация"""
            serializer = OrderSerializer(data=deserializered_order)
            serializer.is_valid(raise_exception=True)
            print('serializer.data =', serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as exc:
        print(traceback.format_exc())
        return Response(f'error: {exc}', status=status.HTTP_400_BAD_REQUEST)
