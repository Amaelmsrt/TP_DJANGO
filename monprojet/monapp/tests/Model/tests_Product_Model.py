from django.test import TestCase
from monapp.models import Product 

class ProductModelTest(TestCase):

    def setUp(self):
        self.product = Product.objects.create(name="Chaise", code="CH001", status=0)

    def test_product_creation(self): 
        """
        Tester si un produit est bien créé 
        """
        self.assertEqual(self.product.name, "Chaise") 
        self.assertEqual(self.product.code, "CH001") 
        self.assertEqual(self.product.status, 0)

    def test_string_representation(self):
        """
        Tester la méthode __str__ du modèle Product 
        """
        self.assertEqual(str(self.product), "Chaise")

    def test_update_product(self): 
        """
        Tester la mise à jour d'un produit 
        """
        self.product.name = "Table" 
        self.product.save( )
        updated_product = Product.objects.get(id=self.product.id) 
        self.assertEqual(updated_product.name, "Table")

    def test_delete_product(self):
        """
        Tester la suppression d'un produit 
        """
        self.product.delete( ) 
        self.assertEqual(Product.objects.count(), 0)