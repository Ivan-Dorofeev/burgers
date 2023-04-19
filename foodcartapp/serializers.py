from django.db import transaction
from phonenumber_field.modelfields import PhoneNumberField

from foodcartapp.models import Order, Product, OrderElements
from rest_framework import serializers


class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=1)
    firstname = serializers.CharField(required=True, max_length=100)
    lastname = serializers.CharField(required=True, max_length=100)
    phonenumber = PhoneNumberField(region='RU')
    address = serializers.CharField(required=True, allow_blank=True, max_length=100)

    @transaction.atomic
    def create(self, validated_data):
        order = Order.objects.create(
            firstname=validated_data['firstname'],
            lastname=validated_data['lastname'],
            phonenumber=validated_data['phonenumber'],
            address=validated_data['address'],
        )

        product_by_id_and_product_quantity = [(Product.objects.get(id=int(product['product'])), product['quantity']) for
                                              product in validated_data['products']]
        bulk = []
        for i in product_by_id_and_product_quantity:
            bulk.append(OrderElements(order=order, product=i[0], quantity=i[1]))
        print('********************** bulk = ', bulk)
        OrderElements.objects.bulk_create(bulk)

        # for product in validated_data['products']:
        #     product_by_id = Product.objects.get(id=int(product['product']))
        #     product_quantity = product['quantity']
        #
        #     OrderElements.objects.create(order=order, product=product_by_id,
        #                                  quantity=product_quantity)
        return order

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.title)
        instance.firstname = validated_data.get('firstname', instance.title)
        instance.lastname = validated_data.get('lastname', instance.code)
        instance.phonenumber = validated_data.get('phonenumber', instance.linenos)
        instance.address = validated_data.get('address', instance.language)
        instance.save()
