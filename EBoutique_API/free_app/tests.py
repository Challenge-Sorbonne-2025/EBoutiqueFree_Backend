from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from django.contrib.auth import get_user_model
from free_app.models import Boutique, Produit, Stock, Marque, Modele

User = get_user_model()

class ProduitPermissionsTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Création des utilisateurs
        self.admin = User.objects.create_superuser(username='admin', email='admin@test.com', password='adminpass')
        self.gestionnaire1 = User.objects.create_user(username='gest1', email='gest1@test.com', password='gestpass', is_gestionnaire=True)
        self.utilisateur_normal = User.objects.create_user(username='normal', email='normal@test.com', password='normalpass')

        # Boutiques
        self.boutique1 = Boutique.objects.create(nom="Boutique 1", gestionnaire=self.gestionnaire1, ville="Paris", code_postal="75000")
        self.boutique2 = Boutique.objects.create(nom="Boutique 2", gestionnaire=self.gestionnaire1, ville="Lyon", code_postal="69000")

        # Produits et Stocks
        self.marque_a = Marque.objects.create(nom="Marque A")
        self.modele1 = Modele.objects.create(nom="Modèle 1", marque=self.marque_a)
        self.produit1 = Produit.objects.create(nom="Produit 1", boutique=self.boutique1, prix=100, modele=self.modele1)
        self.stock1 = Stock.objects.create(produit=self.produit1, quantite=10, seuil_alerte=5)

    def test_gestionnaire_acces_produits(self):
        """Test que le gestionnaire peut accéder à ses produits"""
        url = reverse('produit-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nom'], self.produit1.nom)
