from django.urls import path
from boutique import views
# from . import api_views
from .views import tableau_bord, accueil, map_view
from .api_views import boutiques_produits_json # Import API séparé

app_name = 'boutique'
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'marques', views.MarqueViewSet)
router.register(r'modeles', views.ModeleViewSet)
router.register(r'boutiques', views.BoutiqueViewSet)
router.register(r'produits', views.ProduitViewSet)
router.register(r'stocks', views.StockViewSet)
router.register(r'archives-produits', views.ArchivedProduitViewSet)
router.register(r'archives-boutiques', views.ArchivedBoutiqueViewSet)
router.register(r'historique-ventes', views.HistoriqueVentesViewSet)
# router.register(r'demandes-suppression', views.DemandeSuppressionProduitViewSet)


urlpatterns = [
     path('', include(router.urls)),

    # Vue tableau de bord de l'application
    path('tableau-bord/', tableau_bord, name='tableau_bord'),
    # Recherche de boutiques proches où le stock est non nul
    path('recherche-produits/', boutiques_produits_json, name='recherche_produits_proches'),
    # Page de la carte via l'API Google Maps
    path("map/", map_view, name="google_map_view"),
    # Coordonnées des boutiques et leurs produits utilisées par la carte
    path("boutiques-produits/", boutiques_produits_json, name="boutiques_produits_json"),
    # Page d'accueil de l'application boutique
    path('accueil/', accueil, name='accueil'),
]
