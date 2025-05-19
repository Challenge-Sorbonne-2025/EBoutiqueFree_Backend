from django.urls import path
from boutique import views
from . import api_views
from .views import tableau_bord, accueil, carte_produits
from .api_views import recherche_produits_proches # Import API séparé

app_name = 'boutique'

urlpatterns = [
    # Vue tableau de bord de l'application
    path('tableau-bord/', views.tableau_bord, name='tableau_bord'),
    # Recherche de boutiques proches où le stock est non nul
    path('api/recherche-produits/', recherche_produits_proches, name='recherche_produits_proches'),
    # Page de la carte via l'API Google Maps
    path("map/", views.map_view, name="google_map_view"),
    # Coordonnées des boutiques et leurs produits utilisées par la carte
    path("api/boutiques-produits/", api_views.boutiques_produits_json, name="boutiques_produits_json"),
    # Page d'accueil de l'application boutique
    path('accueil/', accueil, name='accueil'),
]
