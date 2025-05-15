from django.test import TestCase
from django.contrib.gis.geos import Point
from rest_framework.test import APIClient
from django.urls import reverse

from boutique.models import Boutique, Produit, Marque, Modele, Stock

class RechercheProduitsProchesTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        marque = Marque.objects.create(nom="Samsung")
        modele = Modele.objects.create(nom="S21", marque=marque)

        boutique = Boutique.objects.create(
            nom="Boutique Paris",
            adresse="1 rue de Paris",
            ville="Paris",
            code_postal="75000",
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

    def test_api_recherche_produits_proches(self):
        response = self.client.get(reverse("boutique:recherche_produits_proches"), {
            "lat": 48.8566,
            "lon": 2.3522,
            "rayon": 10
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(len(data) >= 1)
        self.assertEqual(data[0]["boutique"], "Boutique Paris")


class BoutiquesProduitsJSONTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        marque = Marque.objects.create(nom="Apple")
        modele = Modele.objects.create(nom="iPhone 14", marque=marque)

        boutique = Boutique.objects.create(
            nom="Apple Store",
            adresse="2 rue de Lyon",
            ville="Lyon",
            code_postal="69000",
            location=Point(4.8357, 45.7640)
        )

        produit = Produit.objects.create(
            nom="iPhone 14",
            marque=marque,
            modele=modele,
            prix=899.99,
            couleur="Blanc",
            capacite=256
        )

        Stock.objects.create(boutique=boutique, produit=produit, quantite=10)

    def test_api_boutiques_produits_json(self):
        response = self.client.get(reverse("boutique:boutiques_produits_json"))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["nom"], "Apple Store")
        self.assertEqual(len(data[0]["produits"]), 1)
        self.assertEqual(data[0]["produits"][0]["nom"], "iPhone 14")
