import json

from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

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


# def register_order(request):
#     try:
#         get_orders = json.loads(request.body.decode())
#         print('orders = ', get_orders)
#
#         order = Order.objects.create(
#             client_name=get_orders['firstname'],
#             client_surname=get_orders['lastname'],
#             client_phone=get_orders['phonenumber'],
#             client_address=get_orders['address'],
#         )
#         for product_element in get_orders['products']:
#             product_by_id = Product.objects.get(id=product_element['product'])
#             print('product_by_id = ', product_by_id)
#
#             new_product = OrderElements.objects.create(product=product_by_id, quantity=product_element['quantity'])
#             print('new_product = ', new_product)
#
#             order.order_elements.add(new_product)
#         return JsonResponse({})
#     except ValueError:
#         return JsonResponse({
#             'error': 'Error order register',
#         })

@api_view(['POST'])
def register_order(request):
    try:
        get_orders = request.data
        print('orders = ', get_orders)
        print('orders.type = ', type(get_orders))

        if not isinstance(get_orders['products'], list):
            return Response('products: Ожидался list со значениями, но был получен "str"', status=status.HTTP_400_BAD_REQUEST)
        elif get_orders['products'] == 'null':
            return Response('products: Это поле не может быть пустым',status=status.HTTP_400_BAD_REQUEST)
        elif not get_orders['products']:
            return Response('products: Этот список не может быть пустым', status=status.HTTP_400_BAD_REQUEST)
        elif not 'products' in get_orders.keys():
            return Response('products: Обязательное поле', status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(
            client_name=get_orders['firstname'],
            client_surname=get_orders['lastname'],
            client_phone=get_orders['phonenumber'],
            client_address=get_orders['address'],
        )
        print('order = ', order)
        for product_element in get_orders['products']:
            product_by_id = Product.objects.get(id=product_element['product'])
            product_quantity = product_element['quantity']

            new_product = OrderElements.objects.create(product=product_by_id, quantity=product_quantity)
            print('new_product = ', new_product)

            order.order_elements.add(new_product)
        return Response()

    except Exception as exc:
        return Response(f'error: {exc}', status=status.HTTP_400_BAD_REQUEST)
