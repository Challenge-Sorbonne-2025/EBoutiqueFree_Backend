from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
from .models import (
    Marque, Modele, Boutique, Produit, Stock,
    ArchivedProduit, ArchivedBoutique
)
from .serializers import (
    MarqueSerializer, ModeleSerializer, BoutiqueSerializer,
    ProduitSerializer, StockSerializer, ArchivedProduitSerializer,
    ArchivedBoutiqueSerializer
)
from .permissions import EstResponsableBoutique, EstGestionnaireOuResponsable
from rest_framework.permissions import IsAuthenticated


class MarqueViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les marques de téléphones.
    """
    queryset = Marque.objects.all()
    serializer_class = MarqueSerializer
    permission_classes = [EstGestionnaireOuResponsable]

    @swagger_auto_schema(
        operation_description="Liste toutes les marques",
        responses={200: MarqueSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Crée une nouvelle marque",
        request_body=MarqueSerializer,
        responses={201: MarqueSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class ModeleViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les modèles de téléphones.
    """
    queryset = Modele.objects.all()
    serializer_class = ModeleSerializer
    permission_classes = [EstGestionnaireOuResponsable]

class BoutiqueViewSet(viewsets.ModelViewSet):
    queryset = Boutique.objects.all()
    serializer_class = BoutiqueSerializer
    permission_classes = [EstResponsableBoutique]

    def perform_destroy(self, instance):
        # Archiver la boutique avant de la supprimer
        ArchivedBoutique.objects.create(
            original_id=instance.id,
            nom=instance.nom,
            adresse=instance.adresse,
            ville=instance.ville,
            code_postal=instance.code_postal,
            departement=instance.departement,
            archive_par=self.request.user,
            raison=self.request.data.get('raison', 'Point de vente fermé')
        )
        instance.delete()

class ProduitViewSet(viewsets.ModelViewSet):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer
    permission_classes = [EstGestionnaireOuResponsable]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        # Archiver le produit avant de le supprimer
        ArchivedProduit.objects.create(
            original_id=instance.id,
            nom=instance.nom,
            marque=instance.marque.nom,
            modele=instance.modele.nom,
            prix=instance.prix,
            couleur=instance.couleur,
            capacite=instance.capacite,
            archive_par=self.request.user,
            raison=self.request.data.get('raison', 'Produit deja vendu')
        )
        instance.delete()

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [EstGestionnaireOuResponsable]

    def get_permissions(self):
        if self.action in ['vendre', 'update', 'partial_update', 'create', 'destroy']:
            return [IsAuthenticated(), EstGestionnaireOuResponsable()]
        return []  # Pas de permission requise pour la lecture

    @action(detail=False, methods=['get'])
    def alertes(self, request):
        seuil = 5  # Valeur de seuil par défaut
        stocks_faibles = self.queryset.filter(quantite__lt=seuil)
        serializer = self.get_serializer(stocks_faibles, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        method='post',
        operation_description="Vendre un produit (décrémente la quantité en stock)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'quantite': openapi.Schema(type=openapi.TYPE_INTEGER, description='Quantité à vendre')
            },
            required=['quantite']
        ),
        responses={
            200: StockSerializer(),
            400: 'Quantité invalide ou stock insuffisant',
            404: 'Stock non trouvé'
        }
    )
    @action(detail=True, methods=['post'])
    def vendre(self, request, pk=None):
        stock = self.get_object()
        quantite_a_vendre = int(request.data.get('quantite', 1))
        
        if quantite_a_vendre <= 0:
            return Response(
                {'error': 'La quantité à vendre doit être positive'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if stock.quantite < quantite_a_vendre:
            return Response(
                {'error': 'Stock insuffisant'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Mettre à jour le stock
        stock.quantite -= quantite_a_vendre
        if stock.quantite == 0:
            # Archiver le produit si le stock est épuisé
            ArchivedProduit.objects.create(
                original_id=stock.produit.id,
                nom=stock.produit.nom,
                marque=stock.produit.marque.nom,
                modele=stock.produit.modele.nom,
                prix=stock.produit.prix,
                couleur=stock.produit.couleur,
                capacite=stock.produit.capacite,
                archive_par=request.user,
                raison="Stock épuisé après vente"
            )
            stock.produit.delete()
            return Response({'message': 'Produit vendu et archivé'}, status=status.HTTP_200_OK)
        
        stock.save()
        serializer = self.get_serializer(stock)
        return Response(serializer.data)

class ArchivedProduitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ArchivedProduit.objects.all()
    serializer_class = ArchivedProduitSerializer
    permission_classes = [EstResponsableBoutique]

class ArchivedBoutiqueViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ArchivedBoutique.objects.all()
    serializer_class = ArchivedBoutiqueSerializer
    permission_classes = [EstResponsableBoutique]