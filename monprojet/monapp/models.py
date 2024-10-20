from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

PRODUCT_STATUS = (
    (0, 'Offline'),
    (1, 'Online'),
    (2, 'Out of stock')              
)

class Status(models.Model):
    """
    Modèle représentant le statut d'un produit.
    """
    numero  = models.IntegerField()
    libelle = models.CharField(max_length=100)

    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères du statut.
        """
        return "{0} {1}".format(self.numero, self.libelle)
    
class Product(models.Model):
    """
    Modèle représentant un produit.
    """
    class Meta:
        verbose_name = "Produit"

    name          = models.CharField(max_length=100)
    code          = models.CharField(max_length=10, null=True, blank=True, unique=True)
    status        = models.SmallIntegerField(choices=PRODUCT_STATUS, default=0)
    date_creation = models.DateTimeField(blank=True, verbose_name="Date création", default=timezone.now)
    image         = models.FileField(upload_to='img/', blank=True, verbose_name="Image du produit", default='img/images.jpeg')

    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères du produit.
        """
        return "{0}".format(self.name)

class ProductSupplier(models.Model):
    """
    Modèle représentant la relation entre un produit et un fournisseur.
    """
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2,  null=True, blank=True, verbose_name="Prix unitaire TTC")
    quantity = models.PositiveIntegerField(null=True, blank=True, verbose_name="Quantité en stock")

    class Meta:
        unique_together = ('product', 'supplier')

class SupplierSellProduct(models.Model):
    """
    Modèle représentant la relation entre un fournisseur et un produit, c'est à dire les produits vendus par un fournisseur.
    """
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2,  null=True, blank=True, verbose_name="Prix unitaire TTC")

    class Meta:
        unique_together = ('product', 'supplier')

class Order(models.Model):
    """
    Modèle représentant une commande.
    """
    STATUS = (
        (0, 'En préparation'),
        (1, 'Passée'),
        (2, 'Reçue'),
    )

    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE)
    status = models.SmallIntegerField(choices=STATUS, default=0)
    date_creation = models.DateTimeField(blank=True, verbose_name="Date création", default=timezone.now)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, default=1)
    quantity = models.PositiveIntegerField(default=1)
    mis_en_stock = models.BooleanField(default=False)

    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères de la commande.
        """
        return "{0}".format(self.supplier)

class ProductItem(models.Model):
    """
    Modèle représentant une déclinaison de produit.
    """
    class Meta:
        verbose_name = "Déclinaison Produit"

    code    = models.CharField(max_length=10, null=True, blank=True, unique=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    attributes  = models.ManyToManyField("ProductAttributeValue", related_name="product_item", blank=True)

    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères de la déclinaison de produit.
        """
        return "{0} {1}".format(self.product, self.code)

class ProductAttribute(models.Model):
    """
    Modèle représentant un attribut de produit.
    """
    class Meta:
        verbose_name = "Attribut"
        
    name = models.CharField(max_length=100)
    
    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères de l'attribut de produit.
        """
        return self.name
    
class ProductAttributeValue(models.Model):
    """
    Modèle représentant une valeur d'attribut de produit.
    """
    class Meta:
        verbose_name = "Valeur attribut"
        ordering = ['position']
        
    value              = models.CharField(max_length=100)
    product_attribute  = models.ForeignKey('ProductAttribute', verbose_name="Unité", on_delete=models.CASCADE)
    position           = models.PositiveSmallIntegerField("Position", null=True, blank=True)

    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères de la valeur d'attribut de produit.
        """
        return "{0} [{1}]".format(self.value, self.product_attribute)

class Supplier(models.Model):
    """
    Modèle représentant un fournisseur.
    """
    class Meta:
        verbose_name = "Supplier"
    
    name = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100, default="password")
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    products = models.ManyToManyField('Product', through='ProductSupplier', related_name='suppliers')

    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères du fournisseur.
        """
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Panier de {self.user.username}"

    def add_product(self, product_supplier, quantity=1):
        cart_item = CartItem.objects.filter(cart=self, product_supplier=product_supplier).first()
        if cart_item:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(cart=self, product_supplier=product_supplier, quantity=quantity)
        self.total_price += product_supplier.price * quantity
        self.save()

    def update_quantity(self, product_supplier, quantity):
        cart_item = CartItem.objects.filter(cart=self, product_supplier=product_supplier).first()
        if cart_item:
            self.total_price -= cart_item.total_price
            cart_item.quantity = quantity
            cart_item.save()
            self.total_price += cart_item.total_price
            self.save()

    def remove_product(self, product_supplier):
        cart_item = CartItem.objects.filter(cart=self, product_supplier=product_supplier).first()
        self.total_price -= cart_item.total_price
        cart_item.delete()
        self.save()

    def clear_cart(self):
        self.total_price = 0
        CartItem.objects.filter(cart=self).delete()
        self.save()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', null=True, blank=True)
    product_supplier = models.ForeignKey(ProductSupplier, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product_supplier.product.name}"

    @property
    def total_price(self):
        return self.quantity * self.product_supplier.price

class CartItem(models.Model):
    """
    Modèle représentant un article dans le panier.
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', null=True, blank=True)
    product_supplier = models.ForeignKey(ProductSupplier, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product_supplier.product.name}"

    @property
    def total_price(self):
        return self.quantity * self.product_supplier.price

class ValidatedCart(models.Model):
    """
    Modèle représentant un panier validé.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='validated_carts')
    date_of_purchase = models.DateTimeField(default=timezone.now)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères du panier validé.
        """
        return f"Panier validé de {self.user.username}"

class ValidatedCartItem(models.Model):
    """
    Modèle représentant un article dans un panier validé.
    """
    validated_cart = models.ForeignKey(ValidatedCart, on_delete=models.CASCADE, related_name='items')
    product_supplier = models.ForeignKey(ProductSupplier, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product_supplier.product.name}"

    @property
    def total_price(self):
        return self.quantity * self.product_supplier.price
