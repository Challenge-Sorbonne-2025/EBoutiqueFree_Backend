from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from EBoutique_API.utils.geocoding import geocode_address
from boutique.models import Boutique
from free_app.models import Produit

def recherche_produits_par_adresse(request):
    adresse = request.GET.get('adresse')
    rayon_km = float(request.GET.get('rayon', 5))  # rayon par défaut = 5 km

    if not adresse:
        return JsonResponse({'error': 'Adresse manquante'}, status=400)

    lat, lng = geocode_address(adresse)
    if lat is None or lng is None:
        return JsonResponse({'error': 'Adresse invalide ou non trouvée'}, status=400)

    point_utilisateur = Point(lng, lat, srid=4326)

    boutiques_proches = Boutique.objects.annotate(
        distance=Distance('location', point_utilisateur)
    ).filter(distance__lte=rayon_km * 1000).order_by('distance')

    resultats = []
    for boutique in boutiques_proches:
        produits_dispos = Product.objects.filter(boutique=boutique, stock__gt=0).values(
            'name', 'price', 'stock'
        )
        resultats.append({
            'boutique': boutique.nom,
            'adresse': boutique.adresse,
            'distance_km': round(boutique.distance.km, 2),
            'produits': list(produits_dispos)
        })

    return JsonResponse(resultats, safe=False)
