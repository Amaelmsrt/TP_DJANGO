from django.test import TestCase
from monapp.models import OrderItem, Order, Product, Supplier

class OrderItemModelTest(TestCase):

    def setUp(self):
        self.supplier = Supplier.objects.create(name="Fournisseur 1")
        self.order = Order.objects.create(supplier=self.supplier)
        self.product = Product.objects.create(name="Chaise", code="CH001", price_ht=50, price_ttc=60, status=0)
        self.order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=2)

    def test_order_item_creation(self):
        """
        Tester si un article de commande est bien créé
        """
        self.assertEqual(self.order_item.order.supplier.name, "Fournisseur 1")
        self.assertEqual(self.order_item.product.name, "Chaise")
        self.assertEqual(self.order_item.quantity, 2)

    def test_string_representation(self):
        """
        Tester la méthode __str__ du modèle OrderItem
        """
        self.assertEqual(str(self.order_item), "Chaise (2)")

    def test_update_order_item(self):
        """
        Tester la mise à jour d'un article de commande
        """
        self.order_item.quantity = 3
        self.order_item.save()
        updated_order_item = OrderItem.objects.get(id=self.order_item.id)
        self.assertEqual(updated_order_item.quantity, 3)

    def test_delete_order_item(self):
        """
        Tester la suppression d'un article de commande
        """
        self.order_item.delete()
        self.assertEqual(OrderItem.objects.count(), 0)