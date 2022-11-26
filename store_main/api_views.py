from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from store_main.serializers import ProductSerializer
from store_main.models import Product


@api_view(['GET', 'POST'])
def api_product_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
