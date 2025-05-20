from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from geopy.geocoders import Nominatim

from boutique.models import Boutique, Stock

# Page d'accueil avec compteur de boutiques
@login_required
def accueil(request):
    context = {
        'boutiques_count': Boutique.objects.count(),
        'user': request.user
    }
    return render(request, 'boutique/accueil.html', context)

# Tableau de bord affichant les stocks faibles
@login_required
def tableau_bord(request):
    stocks_faibles = Stock.objects.filter(quantite__lt=5).select_related('produit', 'boutique')

    context = {
        'stocks_faibles': stocks_faibles,
        'total_boutiques': Boutique.objects.count()
    }
    return render(request, 'boutique/tableau_bord.html', context)

# Affichage de la carte Google Maps
@login_required
def map_view(request):
    # l'utilisateur peut entrer une adresse ou utiliser la géolocalisation
    return render(request, "boutique/google_map.html")
