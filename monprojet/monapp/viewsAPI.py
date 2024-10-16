from rest_framework import viewsets, generics
from .models import Product, Status, Product , SupplierSellProduct, Supplier
from .serializers import ProductSerializer, StatusSerializer, SupplierSellProductSerializer, SupplierSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class SupplierSellProductViewSet(viewsets.ModelViewSet):
    queryset = SupplierSellProduct.objects.all()
    serializer_class = SupplierSellProductSerializer
