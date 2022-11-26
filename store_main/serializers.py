from rest_framework import serializers
from store_main.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('code', 'name', 'amount', 'price',)
        read_only_fields = ('code', 'name', 'amount', 'price',)
