from django.test import TestCase, Client
from django.urls import reverse

class DisconnectViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'logout.html')

    def test_get_supplier(self):
        response = self.client.get(reverse('logout'), {'supplier': 1})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'logout.html')

    def test_get_fail(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'logout.html')