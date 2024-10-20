from django.test import TestCase
from django.contrib.auth.models import User
from monapp.models import Cart, ProductSupplier, Supplier, Product, ValidatedCart, CartItem, ValidatedCartItem

class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.product = Product.objects.create(name="Chaise", code="CH001", status=0)
        self.supplier = Supplier.objects.create(name="Fournisseur 1")
        self.product_supplier = ProductSupplier.objects.create(product=self.product, supplier=self.supplier, price=10)
        # Créer un panier pour l'utilisateur
        self.cart = Cart.objects.create(user=self.user)

    def test_cart_creation(self):
        """
        Tester si un panier est bien créé
        """
        self.assertEqual(self.cart.user, self.user)
        self.assertEqual(self.cart.total_price, 0)

    def test_string_representation(self):
        """
        Tester la méthode __str__ du modèle Cart
        """
        self.assertEqual(str(self.cart), f"Panier de {self.user.username}")

    def test_add_product(self):
        """
        Tester l'ajout d'un produit dans le panier
        """
        self.cart.add_product(product_supplier=self.product_supplier)
        self.assertEqual(self.cart.total_price, 10)
        self.cart.add_product(product_supplier=self.product_supplier)
        self.assertEqual(self.cart.total_price, 20)

    def test_update_quantity(self):
        """
        Tester la mise à jour de la quantité d'un produit dans le panier
        """
        self.cart.add_product(product_supplier=self.product_supplier)
        self.cart.update_quantity(product_supplier=self.product_supplier, quantity=2)
        self.assertEqual(self.cart.total_price, 20)

    def test_remove_product(self):
        """
        Tester la suppression d'un produit du panier
        """
        self.cart.add_product(product_supplier=self.product_supplier)
        self.cart.remove_product(product_supplier=self.product_supplier)
        self.assertEqual(self.cart.total_price, 0)

    def test_clear_cart(self):
        """
        Tester la suppression de tous les produits du panier
        """
        self.cart.add_product(product_supplier=self.product_supplier)
        self.cart.clear_cart()
        self.assertEqual(self.cart.total_price, 0)
        self.assertEqual(self.cart.items.count(), 0)


class CartItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.product = Product.objects.create(name="Chaise", code="CH001", status=0)
        self.supplier = Supplier.objects.create(name="Fournisseur 1")
        self.product_supplier = ProductSupplier.objects.create(product=self.product, supplier=self.supplier, price=10)
        self.cart = Cart.objects.create(user=self.user)

    def test_cart_item_creation(self):
        """
        Tester si un article de panier est bien créé
        """
        cart_item = CartItem.objects.create(cart=self.cart, product_supplier=self.product_supplier, quantity=2)
        self.assertEqual(cart_item.cart, self.cart)
        self.assertEqual(cart_item.product_supplier, self.product_supplier)
        self.assertEqual(cart_item.quantity, 2)

    def test_string_representation(self):
        """
        Tester la méthode __str__ du modèle CartItem
        """
        cart_item = CartItem.objects.create(cart=self.cart, product_supplier=self.product_supplier, quantity=2)
        self.assertEqual(str(cart_item), "2 x Chaise")

    def test_total_price(self):
        """
        Tester la propriété total_price du modèle CartItem
        """
        cart_item = CartItem.objects.create(cart=self.cart, product_supplier=self.product_supplier, quantity=2)
        self.assertEqual(cart_item.total_price, 20)

    def test_total_price_update(self):
        """
        Tester la mise à jour de la propriété total_price du modèle CartItem
        """
        cart_item = CartItem.objects.create(cart=self.cart, product_supplier=self.product_supplier, quantity=2)
        self.assertEqual(cart_item.total_price, 20)
        cart_item.quantity = 3
        self.assertEqual(cart_item.total_price, 30)

class ValidatedCartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.product = Product.objects.create(name="Chaise", code="CH001", status=0)
        self.supplier = Supplier.objects.create(name="Fournisseur 1")
        self.product_supplier = ProductSupplier.objects.create(product=self.product, supplier=self.supplier, price=10)
        self.validated_cart = ValidatedCart.objects.create(user=self.user)

    def test_validated_cart_creation(self):
        """
        Tester si un panier validé est bien créé
        """
        self.assertEqual(self.validated_cart.user, self.user)
        self.assertEqual(self.validated_cart.total_price, 0)

    def test_string_representation(self):
        """
        Tester la méthode __str__ du modèle ValidatedCart
        """
        self.assertEqual(str(self.validated_cart), f"Panier validé de {self.user.username}")

class ValidatedCartItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.product = Product.objects.create(name="Chaise", code="CH001", status=0)
        self.supplier = Supplier.objects.create(name="Fournisseur 1")
        self.product_supplier = ProductSupplier.objects.create(product=self.product, supplier=self.supplier, price=10)
        self.validated_cart = ValidatedCart.objects.create(user=self.user)

    def test_validated_cart_item_creation(self):
        """
        Tester si un article de panier validé est bien créé
        """
        validated_cart_item = ValidatedCartItem.objects.create(validated_cart=self.validated_cart, product_supplier=self.product_supplier, quantity=2)
        self.assertEqual(validated_cart_item.validated_cart, self.validated_cart)
        self.assertEqual(validated_cart_item.product_supplier, self.product_supplier)
        self.assertEqual(validated_cart_item.quantity, 2)

    def test_string_representation(self):
        """
        Tester la méthode __str__ du modèle ValidatedCartItem
        """
        validated_cart_item = ValidatedCartItem.objects.create(validated_cart=self.validated_cart, product_supplier=self.product_supplier, quantity=2)
        self.assertEqual(str(validated_cart_item), "2 x Chaise")

    def test_total_price(self):
        """
        Tester la propriété total_price du modèle ValidatedCartItem
        """
        validated_cart_item = ValidatedCartItem.objects.create(validated_cart=self.validated_cart, product_supplier=self.product_supplier, quantity=2)
        self.assertEqual(validated_cart_item.total_price, 20)

    def test_total_price_update(self):
        """
        Tester la mise à jour de la propriété total_price du modèle ValidatedCartItem
        """
        validated_cart_item = ValidatedCartItem.objects.create(validated_cart=self.validated_cart, product_supplier=self.product_supplier, quantity=2)
        self.assertEqual(validated_cart_item.total_price, 20)
        validated_cart_item.quantity = 3
        self.assertEqual(validated_cart_item.total_price, 30)
