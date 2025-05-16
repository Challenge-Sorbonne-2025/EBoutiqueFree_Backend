from django.urls import path
<<<<<<< HEAD
from boutique import api_views
from boutique import views
from .views import tableau_bord, accueil, carte_produits
from .api_views import recherche_produits_proches # Import API séparé
from .views import recherche_produits_par_adresse
=======
from boutique import views
from .views import tableau_bord, accueil, carte_produits
from .api_views import recherche_produits_proches # Import API séparé
>>>>>>> d98d3597390a31714ae9622bc68b3f1fc7d7692c

app_name = 'boutique'

urlpatterns = [
    path('tableau-bord/', views.tableau_bord, name='tableau_bord'),
# API US5 & US6 : recherche de boutiques proches où le stock est non nul
    path('api/recherche-produits/', recherche_produits_proches, name='recherche_produits_proches'),
<<<<<<< HEAD
    path('api/recherche-produits/', recherche_produits_par_adresse, name='recherche_par_adresse'),
=======
>>>>>>> d98d3597390a31714ae9622bc68b3f1fc7d7692c
    path('carte/', views.carte_produits, name='carte_produits'),
    path('carte/', views.carte_produits, name='map_produits'),
    path("api/boutiques-produits/", api_views.boutiques_produits_json, name="boutiques_produits_json"),
    path('accueil/', accueil, name='accueil'),
]