from django.test import TestCase
from monapp.models import ProductAttributeValue, ProductAttribute
from django.urls import reverse
from django.contrib.auth.models import User

class ProductAttributeValueCreateViewTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='secret') 
        self.client.login(username='testuser', password='secret')
        # Créer un attribut produit de test pour l'utiliser dans le formulaire 
        self.product_attribute = ProductAttribute.objects.create(name="Couleur")

    def test_create_view_get(self):
        """
        Tester que la vue de création renvoie le bon template et s'affiche correctement 
        """
        response = self.client.get(reverse('new_value')) # Utilisation du nom de l'URL 
        self.assertEqual(response.status_code, 200) 
        self.assertTemplateUsed(response, 'new_value.html')

    def test_create_view_post_valid(self):
        """
        Tester que la vue de création crée un nouvel objet lorsque les données sont valides 
        """
        data = { 'value': 'Violet', 'product_attribute': self.product_attribute.id, 'position': 1 }
        response = self.client.post(reverse('new_value'), data)
        # Vérifie la redirection après la création 
        self.assertEqual(response.status_code, 302)
        # Vérifie qu'un objet a été créé 
        self.assertEqual(ProductAttributeValue.objects.count( ), 1)
        # Vérifie la valeur de l'objet créé 
        self.assertEqual(ProductAttributeValue.objects.first( ).value, 'Violet')

class ProductAttributeValueDetailViewTest(TestCase):
    def setUp(self):
        self.product_attribute = ProductAttribute.objects.create(name="Couleur") 
        self.product_attribute_value = ProductAttributeValue.objects.create( value='Violet', product_attribute=self.product_attribute, position=1)
    
    def test_detail_view(self):
        """
        Tester que la vue de détail renvoie le bon template et affiche les bonnes données 
        """
        response = self.client.get(reverse('detail_value', args=[self.product_attribute_value.id])) 
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'detail_value.html')
        # Vérifie que le nom de la valeur est affiché 
        self.assertContains(response, 'Violet')
        # Vérifie que l'attribut associé est affiché 
        self.assertContains(response, 'Couleur')

class ProductAttributeValueUpdateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='secret') 
        self.client.login(username='testuser', password='secret')
        self.product_attribute = ProductAttribute.objects.create(name="Couleur") 
        self.product_attribute_value = ProductAttributeValue.objects.create(
        value='Violet', product_attribute=self.product_attribute, position=1)

    def test_update_view_get(self):
        """
        Tester que la vue de mise à jour s'affiche correctement 
        """
        response = self.client.get(reverse('update_value', args=[self.product_attribute_value.id])) 
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_value.html')

    def test_update_view_post_valid(self):
        """
        Tester que la vue met à jour l'objet lorsque les données sont valides 
        """
        data = { 'value': 'Jaune', 'product_attribute': self.product_attribute.id, 'position': 2 }
        response = self.client.post(reverse('update_value', args=[self.product_attribute_value.id]), data)
        # Redirection après la mise à jour 
        self.assertEqual(response.status_code, 302)
        # Recharger l'objet depuis la base de données 
        self.product_attribute_value.refresh_from_db( )
        # Vérifier la mise à jour 
        self.assertEqual(self.product_attribute_value.value, 'Jaune')
        # Vérifier la mise à jour de la position 
        self.assertEqual(self.product_attribute_value.position, 2)

class ProductAttributeValueDeleteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='secret') 
        self.client.login(username='testuser', password='secret')
        self.product_attribute = ProductAttribute.objects.create(name="Couleur") 
        self.product_attribute_value = ProductAttributeValue.objects.create(
        value='Rouge', product_attribute=self.product_attribute, position=1)

    def test_delete_view_get(self):
        """
        Tester que la vue de suppression s'affiche correctement 
        """
        response = self.client.get(reverse('delete_value', args=[self.product_attribute_value.id])) 
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_value.html')

    def test_delete_view_post(self):
        """
        Tester que l'objet est supprimé lorsque le formulaire de suppression est soumis 
        """
        response = self.client.post(reverse('delete_value', args=[self.product_attribute_value.id]))
        # Redirection après suppression 
        self.assertEqual(response.status_code, 302)
        # Vérifier que l'objet est supprimé 
        self.assertEqual(ProductAttributeValue.objects.count(), 0)

class ProductAttributeValueListViewTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
        self.product_attribute = ProductAttribute.objects.create(name="Couleur")
        self.product_attribute_value = ProductAttributeValue.objects.create(value='Violet', product_attribute=self.product_attribute, position=1)

    def test_list_view(self):
        """
        Tester que la vue de liste renvoie le bon template et affiche les bonnes données 
        """
        response = self.client.get(reverse('values')) 
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list_values.html')
        # Vérifier que le nom de l'attribut est affiché 
        self.assertContains(response, 'Couleur')
        # Vérifier que le nom de la valeur est affiché 
        self.assertContains(response, 'Violet')
