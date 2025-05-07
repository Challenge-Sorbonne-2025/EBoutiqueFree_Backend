from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Produit, Marque, Modele, Boutique, Stock
from .serializers import (
    ProduitSerializer, MarqueSerializer, ModeleSerializer,
    BoutiqueSerializer, StockSerializer
)
from .models import GestionnaireStock
from .serializers import GestionnaireStockSerializer


class ProduitViewSet(viewsets.ModelViewSet):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer


class MarqueViewSet(viewsets.ModelViewSet):
    queryset = Marque.objects.all()
    serializer_class = MarqueSerializer


class ModeleViewSet(viewsets.ModelViewSet):
    queryset = Modele.objects.all()
    serializer_class = ModeleSerializer


class BoutiqueViewSet(viewsets.ModelViewSet):
    queryset = Boutique.objects.all()
    serializer_class = BoutiqueSerializer

    @action(detail=True, methods=['get'])
    def produits(self, request, pk=None):
        boutique = self.get_object()
        stocks = boutique.stocks.select_related('produit')
        produits = [stock.produit for stock in stocks]
        serializer = ProduitSerializer(produits, many=True)
        return Response(serializer.data)


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    @action(detail=False, methods=['get'])
    def alertes(self, request):
        seuil = 5  # Valeur de seuil par défaut
        stocks_faibles = self.queryset.filter(quantite__lt=seuil)
        serializer = self.get_serializer(stocks_faibles, many=True)
        return Response(serializer.data)
class GestionnaireStockViewSet(viewsets.ModelViewSet):
    queryset = GestionnaireStock.objects.all()
    serializer_class = GestionnaireStockSerializer
