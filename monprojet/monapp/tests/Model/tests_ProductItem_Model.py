from django.test import TestCase
from monapp.models import Product, ProductAttribute, ProductAttributeValue, ProductItem

class ProductItemModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="T-shirt")
        self.attribute = ProductAttribute.objects.create(name="Couleur")
        self.value = ProductAttributeValue.objects.create(value="Vert", product_attribute=self.attribute, position=1)
        self.item = ProductItem.objects.create(product=self.product, code="TSHIRT-001")
        self.item.attributes.add(self.value)

    def test_product_item_creation(self):
        """
        Tester si une ProductItem est bien créée
        """
        self.assertEqual(self.item.product.name, "T-shirt")
        self.assertEqual(self.item.code, "TSHIRT-001")
        self.assertEqual(self.item.attributes.first().value, "Vert")

    def test_string_representation(self):
        """
        Tester la méthode __str__ du modèle ProductItem
        """
        self.assertEqual(str(self.item), "T-shirt None TSHIRT-001")

    def test_update_product_item(self):
        """
        Tester la mise à jour d'une ProductItem
        """
        self.item.code = "TSHIRT-002"
        self.item.save()
        updated_item = ProductItem.objects.get(id=self.item.id)
        self.assertEqual(updated_item.code, "TSHIRT-002")

    def test_delete_product_item(self):
        """
        Tester la suppression d'une ProductItem
        """
        self.item.delete()
        self.assertEqual(ProductItem.objects.count(), 0)


    # class ProductItem(models.Model):
    #     """
    #     Modèle représentant une déclinaison de produit.
    #     """
    #     class Meta:
    #         verbose_name = "Déclinaison Produit"

    #     code    = models.CharField(max_length=10, null=True, blank=True, unique=True)
    #     product = models.ForeignKey('Product', on_delete=models.CASCADE)
    #     attributes  = models.ManyToManyField("ProductAttributeValue", related_name="product_item", blank=True)

    #     def __str__(self):
    #         """
    #         Retourne une représentation en chaîne de caractères de la déclinaison de produit.
    #         """
    #         return "{0} {1}".format(self.product, self.code)