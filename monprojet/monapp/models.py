from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

PRODUCT_STATUS = (
    (0, 'Offline'),
    (1, 'Online'),
    (2, 'Out of stock')              
)

class User(AbstractUser):
    ADMIN = 'admin'
    FOURNISSEUR = 'fournisseur'
    UTILISATEUR = 'utilisateur'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (FOURNISSEUR, 'Fournisseur'),
        (UTILISATEUR, 'Utilisateur'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=UTILISATEUR)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Ajout d'un related_name unique
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',  # Ajout d'un related_name unique
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def is_admin(self):
        return self.role == self.ADMIN
    
    def is_fournisseur(self):
        return self.role == self.FOURNISSEUR
    
    def is_utilisateur(self):
        return self.role == self.UTILISATEUR

    def __str__(self):
        return self.username

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
    suppliers     = models.ManyToManyField("Supplier", related_name="products", through='ProductSupplier')
    image         = models.FileField(upload_to='img/', null=True, blank=True, verbose_name="Image du produit")

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
    quantity = models.PositiveIntegerField(default=1)  # Ajout d'une valeur par défaut

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
    
    name = models.CharField(max_length=100)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères du fournisseur.
        """
        return self.name

class Cart(models.Model):
    """
    Modèle représentant un panier d'utilisateur.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Panier de {self.user.username}"

    def add_product(self, product_supplier, quantity=1):
        cart_item = CartItem.objects.filter(cart=self, product_supplier=product_supplier).first()
        if cart_item:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            CartItem.objects.create(cart=self, product_supplier=product_supplier, quantity=quantity)

    def update_quantity(self, product_supplier, quantity):
        cart_item = CartItem.objects.filter(cart=self, product_supplier=product_supplier).first()
        if cart_item:
            cart_item.quantity = quantity
            cart_item.save()

    def remove_product(self, product_supplier):
        CartItem.objects.filter(cart=self, product_supplier=product_supplier).delete()

class CartItem(models.Model):
    """
    Modèle représentant un article dans le panier.
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product_supplier = models.ForeignKey(ProductSupplier, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product_supplier.product.name}"

    @property
    def total_price(self):
        return self.quantity * self.product_supplier.price