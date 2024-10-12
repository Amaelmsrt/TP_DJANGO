from django.db import models
from django.utils import timezone

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
    price_ht      = models.DecimalField(max_digits=8, decimal_places=2,  null=True, blank=True, verbose_name="Prix unitaire HT")
    price_ttc     = models.DecimalField(max_digits=8, decimal_places=2,  null=True, blank=True, verbose_name="Prix unitaire TTC")
    status        = models.SmallIntegerField(choices=PRODUCT_STATUS, default=0)
    date_creation = models.DateTimeField(blank=True, verbose_name="Date création", default=timezone.now)
    suppliers  = models.ManyToManyField("Supplier", related_name="products", through='ProductSupplier')

    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères du produit.
        """
        return "{0} {1}".format(self.name, self.code)

class ProductSupplier(models.Model):
    """
    Modèle représentant la relation entre un produit et un fournisseur.
    """
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2,  null=True, blank=True, verbose_name="Prix unitaire HT")
    quantity = models.PositiveIntegerField(null=True, blank=True, verbose_name="Quantité en stock")

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
    date_update = models.DateTimeField(blank=True, verbose_name="Date modification", default=timezone.now)

    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères de la commande.
        """
        return "{0} {1}".format(self.supplier, self.date_creation)

class OrderItem(models.Model):
    """
    Modèle représentant un article dans une commande.
    """
    order = models.ForeignKey('Order', related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        """
        Retourne une représentation en chaîne de caractères de l'article de commande.
        """
        return "{0} ({1})".format(self.product.name, self.quantity)

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