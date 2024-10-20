from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from monapp.models import Supplier, Product

class SupplierDetailViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.supplier = Supplier.objects.create(name='Test Supplier')
        self.product = Product.objects.create(name='Test Product')
        self.supplier.products.add(self.product)

    def test_detail_view(self):
        response = self.client.get(reverse('detail_supplier', args=[self.supplier.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'detail_supplier.html')
        self.assertContains(response, 'Test Supplier')

    def test_context_data(self):
        response = self.client.get(reverse('detail_supplier', args=[self.supplier.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'detail_supplier.html')
        self.assertContains(response, 'Test Supplier')
        self.assertTrue('products' in response.context)
        self.assertTrue('supplier' in response.context)
        self.assertEqual(response.context['supplier'], self.supplier)
        self.assertEqual(len(response.context['products']), 1)

    def test_search_view(self):
        response = self.client.get(reverse('detail_supplier', args=[self.supplier.id]), {'search': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'detail_supplier.html')
        self.assertContains(response, 'Test Product')
