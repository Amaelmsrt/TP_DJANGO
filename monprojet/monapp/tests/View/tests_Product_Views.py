from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from monapp.models import Product, Supplier
from monapp.forms import ProductForm

class ProductViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.product = Product.objects.create(name='Test Product')

    def test_list_view(self):
        response = self.client.get(reverse('produits'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list_products.html')
        self.assertContains(response, 'Test Product')

    def test_detail_view(self):
        response = self.client.get(reverse('detail_product', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'detail_product.html')
        self.assertContains(response, 'Test Product')

    def test_create_view_get(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('new_product'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'new_product.html')

    def test_update_view_get(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('update_product', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_product.html')

    def test_delete_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('delete_product', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('produits'))
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())

    def test_search_view(self):
        response = self.client.get(reverse('produits'), {'search': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list_products.html')
        self.assertContains(response, 'Test Product')
