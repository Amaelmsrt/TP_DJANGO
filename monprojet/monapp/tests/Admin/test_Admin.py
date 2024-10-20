from django.test import TestCase
from unittest.mock import Mock
from monapp.admin import ProductAdmin, ProductFilter, set_product_online, set_product_offline
from monapp.models import Product
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.contrib.admin.sites import AdminSite

class MockRequest(HttpRequest):
    def __init__(self, user):
        super().__init__()
        self.user = user

class ProductAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = ProductAdmin(Product, self.site)
        self.user = User.objects.create_superuser(username='admin', password='password', email='admin@example.com')
        self.request = MockRequest(self.user)
        self.product = Product.objects.create(code='P001', name='Product 1')

    def test_set_product_online(self):
        """
        Teste que le produit est mis en ligne
        """
        queryset = Product.objects.filter(id=self.product.id)
        set_product_online(None, self.request, queryset)
        self.product.refresh_from_db()
        self.assertEqual(self.product.status, 1)

    def test_set_product_offline(self):
        """
        Teste que le produit est mis hors ligne
        """
        self.product.status = 1
        self.product.save()
        queryset = Product.objects.filter(id=self.product.id)
        set_product_offline(None, self.request, queryset)
        self.product.refresh_from_db()
        self.assertEqual(self.product.status, 0)

class ProductFilterTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='admin', password='password', email='admin@example.com')
        self.request = MockRequest(self.user)
        self.filter = ProductFilter(self.request, {}, Product, ProductAdmin)
        self.product_online = Product.objects.create(code='P001', name='Product 1', status=1)
        self.product_offline = Product.objects.create(code='P002', name='Product 2', status=0)

    def test_queryset_online(self):
        """
        Teste que le filtre retourne les produits en ligne
        """
        self.filter.value = Mock(return_value='online')
        queryset = Product.objects.all()
        filtered_queryset = self.filter.queryset(self.request, queryset)
        self.assertEqual(filtered_queryset.count(), 1)
        self.assertEqual(filtered_queryset.first(), self.product_online)

    def test_queryset_offline(self):
        """
        Teste que le filtre retourne les produits hors ligne
        """
        self.filter.value = Mock(return_value='offline')
        queryset = Product.objects.all()
        filtered_queryset = self.filter.queryset(self.request, queryset)
        self.assertEqual(filtered_queryset.count(), 1)
        self.assertEqual(filtered_queryset.first(), self.product_offline)