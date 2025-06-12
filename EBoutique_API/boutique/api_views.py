from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from .models import Boutique
from .permissions import EstGestionnaireOuResponsable

# API : Recherche des 5 boutiques les plus proches avec stock non nul
@api_view(['GET'])
@permission_classes([EstGestionnaireOuResponsable])
def boutiques_produits_json(request):
    try:
        # Lecture des coordonnées GPS depuis la requête
        lat = float(request.GET.get("lat"))
        lon = float(request.GET.get("lon"))
    except (TypeError, ValueError):
        return Response({"error": "Coordonnées invalides"}, status=status.HTTP_400_BAD_REQUEST)

    user_location = Point(lon, lat, srid=4326)

    # Boutiques dans un rayon de 10km, triées par distance
    boutiques_proches = Boutique.objects.filter(
        location__distance_lte=(user_location, 100000)
    ).annotate(distance=Distance("location", user_location)).order_by("distance")

    resultats = []
    # VERIFIER SI LA LISTE EST VIDE
    if not boutiques_proches:
        return Response({"message": "Aucune boutique trouvée dans un rayon de 10 km."}, status=status.HTTP_404_NOT_FOUND)
    else:   

        for boutique in boutiques_proches:
            # Filtrer les stocks avec quantite > 0
            stocks = boutique.stocks.filter(quantite__gt=0).select_related("produit", "produit__modele__marque", "produit__modele")
            for stock in stocks:
                resultats.append({
                    "boutique": boutique.nom_boutique,
                    "ville": boutique.ville,
                    "lat": boutique.latitude,
                    "lon": boutique.longitude,
                    "adresse": boutique.adresse,
                    "code_postal": boutique.code_postal,
                    "departement": boutique.departement,
                    # "distance_km": round(boutique.distance.km, 2),
                    "produit": stock.produit.nom_produit,
                    "marque": stock.produit.modele.marque.marque,
                    "modele": stock.produit.modele.modele,
                    "prix": float(stock.produit.prix),
                    "quantite": stock.quantite,
                })
                break  # On suppose une recherche d'un seul produit à la fois par boutique
            if len(resultats) >= 5:
                break  # Affichage des 5 premiers résultats
        if not resultats:
            return Response({"message": "Aucun produit trouvé dans un rayon de 10 km."}, status=status.HTTP_404_NOT_FOUND)
   
        return Response(resultats)