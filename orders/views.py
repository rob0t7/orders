from rest_framework import viewsets

from .models import Product, Customer
from .serializers import ProductSerializer, CustomerSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.order_by("name")
    serializer_class = ProductSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.order_by("last_name")
    serializer_class = CustomerSerializer
