from django.test import TestCase
from boutique.models import Boutique, Produit, Marque, Modele, Stock
from django.contrib.gis.geos import Point
from rest_framework.test import APIClient

class CarteProduitsTest(TestCase):
    def setUp(self):
        marque = Marque.objects.create(marque="Samsung")
        modele = Modele.objects.create(modele="S21", marque=marque)
        boutique = Boutique.objects.create(
            nom="Boutique Test",
            ville="Paris",
            code_postal="75000",
            adresse="123 rue de Paris",
            location=Point(2.3522, 48.8566)
        )
        produit = Produit.objects.create(
            nom="Galaxy S21",
            marque=marque,
            modele=modele,
            prix=599.99,
            couleur="Noir",
            capacite=128
        )
        Stock.objects.create(boutique=boutique, produit=produit, quantite=5)

    def test_boutiques_api(self):
        client = APIClient()
        response = client.get("/boutique/api/boutiques-produits/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["nom"], "Boutique Test")
