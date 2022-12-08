from django.shortcuts import render
from rest_framework import viewsets
from store_main.models import Product
from apis.serializers import ProductSerializer


class ProductApiViewSet(viewsets.ModelViewSet):
    # Productオブジェクト取得
    queryset = Product.objects.all()
    # シリアライザーを取得
    serializer_class = ProductSerializer

    # https://kosuke-space.com/django-rest-framework-tutorial
