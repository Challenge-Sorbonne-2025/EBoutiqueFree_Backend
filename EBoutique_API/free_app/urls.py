from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MarqueViewSet, ModeleViewSet, ProduitViewSet, BoutiqueViewSet,
    StockViewSet, GestionnaireStockViewSet
)

# Routeur principal
router = DefaultRouter()
router.register(r'marques', MarqueViewSet, basename='marque')
router.register(r'modeles', ModeleViewSet, basename='modele')
router.register(r'produits', ProduitViewSet, basename='produit')
router.register(r'boutiques', BoutiqueViewSet, basename='boutique')
router.register(r'stocks', StockViewSet, basename='stock')
router.register(r'gestionnaires', GestionnaireStockViewSet, basename='gestionnaire')

# URL personnalisées
custom_urlpatterns = [
    path('stocks/alertes/', StockViewSet.as_view({'get': 'alertes'}), name='stock-alertes'),
    path('boutiques/<int:pk>/produits/', BoutiqueViewSet.as_view({'get': 'produits'}), name='boutique-produits'),
]

urlpatterns = [
    path('', include(router.urls)),
] + custom_urlpatterns
