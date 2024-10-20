from django.test import TestCase, Client
from django.urls import reverse


class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_post(self):
        response = self.client.post(reverse('register'), {'username': 'testuser', 'password': '12345'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_post_fail(self):
        response = self.client.post(reverse('register'), {'username': 'testuser', 'password': '12345'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')