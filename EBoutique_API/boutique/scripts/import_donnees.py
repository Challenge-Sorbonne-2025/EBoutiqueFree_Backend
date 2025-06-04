from django.contrib.gis.geos import Point
from boutique.models import Marque, Modele, Produit, Boutique, Stock

def run():
    print("Création de données de test...")

    marque = Marque.objects.create(nom="Apple")
    modele = Modele.objects.create(nom="iPhone 13", marque=marque)

    boutique = Boutique.objects.create(
        nom="iStore Paris",
        adresse="1 rue Apple",
        ville="Paris",
        code_postal="75001",
        location=Point(2.34, 48.86),  # Paris centre
    )

    produit = Produit.objects.create(
        nom="iPhone 13",
        marque=marque,
        modele=modele,
        prix=799.99,
        couleur="Bleu",
        capacite=128,
    )

    Stock.objects.create(
        boutique=boutique,
        produit=produit,
        quantite=5,
    )

    print("✅ Données de test importées.")
