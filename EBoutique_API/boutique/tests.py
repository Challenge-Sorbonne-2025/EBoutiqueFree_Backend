from django.test import TestCase
# from boutique.models import Boutique
# Create your tests here.
from django.contrib.gis.geos import Point
from rest_framework.test import APIClient
from boutique.models import Boutique, Produit, Stock, Marque, Modele

class RechercheProduitAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.marque = Marque.objects.create(nom="Samsung")
        self.modele = Modele.objects.create(nom="S21", marque=self.marque)
        self.boutique = Boutique.objects.create(
            nom="Boutique Test",
            adresse="123 rue Test",
            ville="Paris",
            code_postal="75000",
            location=Point(2.35, 48.85),
        )
        self.produit = Produit.objects.create(
            nom="Galaxy S21",
            marque=self.marque,
            modele=self.modele,
            prix=599.99,
            couleur="Noir",
            capacite=128,
        )
        Stock.objects.create(
            boutique=self.boutique,
            produit=self.produit,
            quantite=10
        )

    def test_recherche_produits(self):
        url = "/boutique/api/recherche-produits/?lat=48.85&lon=2.35&rayon=10"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["produit"], "Galaxy S21")
        self.assertEqual(data[0]["boutique"], "Boutique Test")
