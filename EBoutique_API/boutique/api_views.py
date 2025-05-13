from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Boutique, Stock

@api_view(['GET'])
def recherche_produits_proches(request):
    try:
        lat = float(request.GET.get("lat"))
        lon = float(request.GET.get("lon"))
        rayon = float(request.GET.get("rayon", 10))  # Rayon par défaut : 10 km
    except (TypeError, ValueError):
        return Response({"error": "Paramètres GPS invalides."}, status=400)

    user_location = Point(lon, lat, srid=4326)

    boutiques_proches = Boutique.objects.filter(
        location__distance_lte=(user_location, rayon * 1000)
    ).annotate(distance=Distance("location", user_location)).order_by("distance")

    resultats = []
    for boutique in boutiques_proches:
        for stock in boutique.stocks.filter(quantite__gt=0).select_related('produit__marque', 'produit__modele'):
            produit = stock.produit
            resultats.append({
                "boutique": boutique.nom,
                "ville": boutique.ville,
                "distance_km": round(boutique.distance.km, 2),
                "produit": produit.nom,
                "marque": produit.marque.nom,
                "modele": produit.modele.nom,
                "prix": float(produit.prix),
                "quantite": stock.quantite,
            })

    return Response(resultats)
