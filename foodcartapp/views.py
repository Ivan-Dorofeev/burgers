import traceback

from django.db import transaction
from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product, Order, OrderElements
from .serializers import OrderDeSerializer, OrderSerializer


def banners_list_api(request):
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


@api_view(['POST'])
def register_order(request):
    try:
        with transaction.atomic():
            get_orders = request.data

            """Десериализация"""
            deserializer = OrderSerializer(data=get_orders)
            deserializer.is_valid(raise_exception=True)

            """Запись в БД"""
            order = Order.objects.create(
                firstname=get_orders['firstname'],
                lastname=get_orders['lastname'],
                phonenumber=get_orders['phonenumber'],
                address=get_orders['address'],
            )
            for product in get_orders['products']:
                product_by_id = Product.objects.get(id=int(product['product']))
                product_quantity = product['quantity']

                OrderElements.objects.create(order=order, product=product_by_id,
                                                           quantity=product_quantity)

            deserializered_order = deserializer.data
            deserializered_order['id'] = order.id

            """Сериализация"""
            serializer = OrderSerializer(data=deserializered_order)
            serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Exception as exc:
        print(traceback.format_exc())
        return Response(f'error: {exc}', status=status.HTTP_400_BAD_REQUEST)
