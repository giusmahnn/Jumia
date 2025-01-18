from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from products.models import Product
from products.serializers import ProductSerializer
from products.pagination import CustomPagination
from django.db.models import Q

# Create your views here.




class ProductView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        products = Product.objects.all()
        paginator = CustomPagination()
        paginated_products = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(paginated_products, many=True)
        return paginator.get_paginated_response(serializer.data)
        # return Response(serializer.data, status.HTTP_200_OK)




class ProductSearchView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        name = request.query_params.get('name')
        category = request.query_params.get('category')

        queryset = Product.objects.all()

        if name or category:
            query = Q()
            if name:
                query &= Q(name__icontains=name)
            if category:
                query &= Q(category__icontains=category)
            queryset = queryset.filter(query)
        paginator = CustomPagination()
        paginated_products = paginator.paginate_queryset(queryset, request)
        serializer = ProductSerializer(paginated_products, many=True)

        if not queryset.exists():
            return Response({"message": "No products found"}, status=status.HTTP_400_BAD_REQUEST)
        return paginator.get_paginated_response(serializer.data)
    
    

class ProductDetailView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pk):
        products = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(products)
        return Response(serializer.data, status.HTTP_200_OK)
        