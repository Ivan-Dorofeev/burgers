from django.db import transaction
from rest_framework.serializers import ModelSerializer

from foodcartapp.models import Order, Product

from rest_framework.serializers import ValidationError, ModelSerializer
from phonenumber_field.phonenumber import PhoneNumber
from rest_framework import serializers


# class OrderDeSerializer(ModelSerializer):
#     class Meta:
#         model = Order
#         fields = ['firstname', 'lastname', 'phonenumber', 'address']
#
#     def validate_phonenumber(self, value):
#         if not PhoneNumber.from_string(value).is_valid():
#             raise ValidationError('Введен некорректный номер телефона.')
#         return value
#
#     def validate_products(self, values):
#         if not values:
#             raise ValidationError(f'Этот список не может быть пустым.')
#
#         order_product_ids = Product.objects.all()
#         for value in values:
#             if not value in order_product_ids:
#                 raise ValidationError(f'Недопустимый первичный ключ {value["product"]}')
#         return values


class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=1)
    firstname = serializers.CharField(required=True, allow_blank=True, max_length=100)
    lastname = serializers.CharField(required=True, allow_blank=True, max_length=100)
    phonenumber = serializers.CharField(required=True)
    address = serializers.CharField(required=True, allow_blank=True, max_length=100)

    @transaction.atomic
    def create(self, validated_data):
        return Order.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.title)
        instance.firstname = validated_data.get('firstname', instance.title)
        instance.lastname = validated_data.get('lastname', instance.code)
        instance.phonenumber = validated_data.get('phonenumber', instance.linenos)
        instance.address = validated_data.get('address', instance.language)
        instance.save()
