from django.test import TestCase
from monapp.models import Status

class StatusModelTest(TestCase):
    def setUp(self):
        self.status = Status.objects.create(numero=1, libelle="En stock")

    def test_status_creation(self):
        """
        Tester si un statut est bien créé
        """
        self.assertEqual(self.status.numero, 1)
        self.assertEqual(self.status.libelle, "En stock")

    def test_string_representation(self):
        """
        Tester la méthode __str__ du modèle Status
        """
        self.assertEqual(str(self.status), "1 En stock")

    def test_update_status(self):
        """
        Tester la mise à jour d'un statut
        """
        self.status.libelle = "Hors stock"
        self.status.save()
        updated_status = Status.objects.get(id=self.status.id)
        self.assertEqual(updated_status.libelle, "Hors stock")

    def test_delete_status(self):
        """
        Tester la suppression d'un statut
        """
        self.status.delete()
        self.assertEqual(Status.objects.count(), 0)
