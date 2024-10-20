from rest_framework import serializers
from .models import Product, Status, SupplierSellProduct, Supplier, ProductSupplier, Order
class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class SupplierSellProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierSellProduct
        fields = '__all__'

class ProductSupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSupplier
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'