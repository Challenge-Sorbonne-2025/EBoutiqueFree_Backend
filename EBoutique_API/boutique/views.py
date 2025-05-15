from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from geopy.geocoders import Nominatim
from django.contrib.auth.decorators import login_required
from boutique.models import Boutique, Stock, Produit

@login_required
def accueil(request):
    context = {
        'boutiques_count': Boutique.objects.count(),
        'user': request.user
    }
    return render(request, 'boutique/accueil.html', context)


@login_required
def tableau_bord(request):
    stocks_faibles = Stock.objects.filter(quantite__lt=5).select_related('produit', 'boutique')

    context = {
        'stocks_faibles': stocks_faibles,
        'total_boutiques': Boutique.objects.count()
    }
    return render(request, 'boutique/tableau_bord.html', context)


@login_required
def carte_produits(request):
    boutiques = []

    for b in Boutique.objects.all():
        produits = [f"{s.produit.nom} ({s.quantite})" for s in b.stocks.select_related("produit") if s.quantite > 0]
        if b.location and produits:
            boutiques.append({
                "nom": b.nom,
                "latitude": b.location.y,
                "longitude": b.location.x,
                "produits": ", ".join(produits)
            })

    return render(request, "boutique/map.html", {"boutiques": boutiques})


@login_required
def recherche_produits_par_adresse(request):
    adresse = request.GET.get("adresse")
    nom_produit = request.GET.get("produit", None)

    if not adresse:
        return JsonResponse({"error": "Adresse manquante"}, status=400)

    try:
        geolocator = Nominatim(user_agent="eboutique_app")
        location = geolocator.geocode(adresse)
        if not location:
            return JsonResponse({"error": "Adresse introuvable"}, status=404)

        user_location = Point(location.longitude, location.latitude, srid=4326)

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
