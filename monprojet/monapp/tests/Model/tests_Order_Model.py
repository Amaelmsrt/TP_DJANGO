from django.test import TestCase
from monapp.models import Order, Supplier, Product

class OrderModelTest(TestCase):
    def setUp(self):
        self.supplier = Supplier.objects.create(name="Fournisseur 1")
        self.product = Product.objects.create(name="Produit 1")
        self.order = Order.objects.create(supplier=self.supplier, product=self.product)

    def test_order_creation(self):
        """
        Tester si une commande est bien créée
        """
        self.assertEqual(self.order.supplier.name, "Fournisseur 1")
        self.assertEqual(self.order.status, 0)

    def test_string_representation(self):
        """
        Tester la méthode __str__ du modèle Order
        """
        self.assertEqual(str(self.order), "Fournisseur 1")

    def test_update_order(self):
        """
        Tester la mise à jour d'une commande
        """
        self.order.status = 1
        self.order.save()
        updated_order = Order.objects.get(id=self.order.id)
        self.assertEqual(updated_order.status, 1)

    def test_delete_order(self):
        """
        Tester la suppression d'une commande
        """
        self.order.delete()
        self.assertEqual(Order.objects.count(), 0)