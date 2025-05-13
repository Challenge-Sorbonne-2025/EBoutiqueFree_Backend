from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from boutique.models import Boutique, AlerteStock, Stock

@login_required
def accueil(request):
    context = {
        'boutiques_count': Boutique.objects.filter(est_active=True).count(),
        'alertes_count': AlerteStock.objects.filter(lue=False).count(),
        'user': request.user
    }
    return render(request, 'boutique/accueil.html', context)
@login_required
def tableau_bord(request):
    alertes = AlerteStock.objects.filter(lue=False).select_related('stock')
    stocks_faibles = Stock.objects.filter(quantite__lt=5).select_related('produit', 'boutique')
    
    context = {
        'alertes': alertes,
        'stocks_faibles': stocks_faibles,
        'total_boutiques': Boutique.objects.filter(est_active=True).count()
    }
    return render(request, 'boutique/tableau_bord.html', context)
from django.contrib.auth.decorators import login_required

@login_required
def carte_produits(request):
    return render(request, 'boutique/map.html')
