from rest_framework import serializers
from foodcartapp.models import Order


class SnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    firstname = serializers.CharField(required=False, allow_blank=True, max_length=100)
    lastname = serializers.CharField(required=False, allow_blank=True, max_length=100)
    phonenumber = serializers.CharField(required=False, allow_blank=True, max_length=100)
    address = serializers.ChoiceField(required=False, allow_blank=True, max_length=100)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Order.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.firstname = validated_data.get('firstname', instance.title)
        instance.lastname = validated_data.get('lastname', instance.code)
        instance.phonenumber = validated_data.get('phonenumber', instance.linenos)
        instance.address = validated_data.get('address', instance.language)
        instance.save()
        return instance
