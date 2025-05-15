from django.shortcuts import renderfrom django.http import JsonResponse
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from geopy.geocoders import Nominatim
from django.contrib.auth.decorators import login_required
from boutique.models import Boutique, Stock, Produit

@login_required
def accueil(request):
    context = {
        'boutiques_count': Boutique.objects.filter(est_active=True).count(),
        #'alertes_count': AlerteStock.objects.filter(lue=False).count(),
        'user': request.user
    }
    return render(request, 'boutique/accueil.html', context)
@login_required
def tableau_bord(request):
   # alertes = AlerteStock.objects.filter(lue=False).select_related('stock')
    stocks_faibles = Stock.objects.filter(quantite__lt=5).select_related('produit', 'boutique')
    
    context = {
        'alertes': alertes,
        'stocks_faibles': stocks_faibles,
        'total_boutiques': Boutique.objects.filter(est_active=True).count()
    }
    return render(request, 'boutique/tableau_bord.html', context)
@login_required
def carte_produits(request):
    boutiques = []

    for b in Boutique.objects.all():
        produits = [f"{s.produit.nom} ({s.quantite})" for s in b.stocks.select_related("produit")]
        boutiques.append({
            "nom": b.nom,
            "latitude": b.location.y if b.location else 0,
            "longitude": b.location.x if b.location else 0,
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
        # Géocodage de l’adresse avec Nominatim (OpenStreetMap)
        geolocator = Nominatim(user_agent="eboutique_app")
        location = geolocator.geocode(adresse)
        if not location:
            return JsonResponse({"error": "Adresse introuvable"}, status=404)

        user_location = Point(location.longitude, location.latitude, srid=4326)

        # Recherche des boutiques dans un rayon de 10 km, triées par distance
        boutiques = Boutique.objects.annotate(
            distance=Distance("localisation", user_location)
        ).filter(
            localisation__distance_lte=(user_location, 10000)  # 10 km
        ).order_by("distance")

        resultat = []
        for boutique in boutiques:
            stocks = Stock.objects.filter(boutique=boutique)
            if nom_produit:
                stocks = stocks.filter(produit__nom__icontains=nom_produit)
            produits = [
                {
                    "nom": stock.produit.nom,
                    "quantite": stock.quantite
                }
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