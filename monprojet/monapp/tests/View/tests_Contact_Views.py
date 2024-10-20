from django.test import TestCase, Client
from django.urls import reverse

class ContactViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_contact_view(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')

    def test_contact_view_post(self):
        response = self.client.post(reverse('contact'), {'name': 'Test User', 'email': 'user.u@gmail.com', 'message': 'Test message'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))