from rest_framework import serializers
from .models import Product, Status, SupplierSellProduct, Supplier

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
