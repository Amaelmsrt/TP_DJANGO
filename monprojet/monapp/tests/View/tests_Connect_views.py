from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from monapp.models import Supplier

class ConnectViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.supplier = Supplier.objects.create(name='Test Supplier', password='12345')

    def test_post(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': '12345'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_post_supplier(self):
        response = self.client.post(reverse('login'), {'username': 'Test Supplier', 'password': '12345'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_post_fail(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': '1234'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
