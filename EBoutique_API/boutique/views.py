from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from geopy.geocoders import Nominatim
from django.contrib.auth.decorators import login_required
from boutique.models import Boutique, Stock

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
from django.contrib.auth.decorators import login_required

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