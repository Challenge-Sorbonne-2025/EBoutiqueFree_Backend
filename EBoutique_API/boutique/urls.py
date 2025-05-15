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
]
# 