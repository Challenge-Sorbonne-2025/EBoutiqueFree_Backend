from django.http import JsonResponse
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from boutique.models import Boutique, Stock
from geopy.geocoders import Nominatim

@csrf_exempt
@login_required
def recherche_produits_proches(request):
    try:
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')
        nom_produit = request.GET.get('produit', None)

        if not lat or not lon:
            return JsonResponse({"error": "Coordonnées manquantes"}, status=400)

        user_location = Point(float(lon), float(lat), srid=4326)

        boutiques = Boutique.objects.annotate(
            distance=Distance("location", user_location)
        ).filter(
            location__distance_lte=(user_location, 10000)  # 10 km
        ).order_by("distance")

        resultat = []
        for boutique in boutiques:
            stocks = Stock.objects.filter(boutique=boutique, quantite__gt=0)
            if nom_produit:
                stocks = stocks.filter(produit__nom__icontains=nom_produit)

            produits = [
                {"nom": stock.produit.nom, "quantite": stock.quantite}
                for stock in stocks
            ]

            if produits:
                resultat.append({
                    "boutique": boutique.nom,
                    "adresse": boutique.adresse,
                    "distance_km": round(boutique.distance.km, 2),
                    "produits": produits
                })

        return JsonResponse(resultat, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required
def boutiques_produits_json(request):
    boutiques = []

    for b in Boutique.objects.all():
        produits = [
            {
                "nom": s.produit.nom,
                "quantite": s.quantite
            }
            for s in b.stocks.select_related("produit") if s.quantite > 0
        ]

        if b.location and produits:
            boutiques.append({
                "nom": b.nom,
                "latitude": b.location.y,
                "longitude": b.location.x,
                "produits": produits
            })

    return JsonResponse(boutiques, safe=False)
