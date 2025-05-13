from django.urls import path
from boutique import views
from .views import tableau_bord, accueil, carte_produits
from .api_views import recherche_produits_proches # Import API séparé

app_name = 'boutique'

urlpatterns = [
    path('tableau-bord/', views.tableau_bord, name='tableau_bord'),
# API US5 & US6 : recherche de boutiques proches où le stock est non nul
    path('api/recherche-produits/', recherche_produits_proches, name='recherche_produits_proches'),
    path('carte/', views.carte_produits, name='carte_produits'),
    path('accueil/', accueil, name='accueil'),
]