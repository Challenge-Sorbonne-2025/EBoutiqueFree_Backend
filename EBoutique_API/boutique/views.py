from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import (
    Marque, Modele, Boutique, Produit, Stock,
    ArchivedProduit, ArchivedBoutique, HistoriqueVentes,
    DemandeSuppressionProduit
)
from .serializers import (
    MarqueSerializer, ModeleSerializer, BoutiqueSerializer,
    ProduitSerializer, StockSerializer, ArchivedProduitSerializer,
    ArchivedBoutiqueSerializer, HistoriqueVentesSerializer,
    DemandeSuppressionProduitSerializer
)
from .permissions import EstResponsableBoutique, EstGestionnaireOuResponsable
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

# ============================================================================
# Gestion des marques
# ============================================================================
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
    
    @swagger_auto_schema(
        operation_description="Récupère une marque par son ID",
        responses={200: MarqueSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Met à jour une marque existante",
        request_body=MarqueSerializer,
        responses={200: MarqueSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Supprime une marque existante",
        responses={204: None}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

# ============================================================================
# Gestion des modèles
# ============================================================================
class ModeleViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les modèles de téléphones.
    """
    queryset = Modele.objects.all()
    serializer_class = ModeleSerializer
    permission_classes = [EstGestionnaireOuResponsable]

    @swagger_auto_schema(
        operation_description="Liste tous les modèles",
        responses={200: ModeleSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Crée un nouveau modèle",
        request_body=ModeleSerializer,
        responses={201: ModeleSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Récupère un modèle par son ID",
        responses={200: ModeleSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Met à jour un modèle existant",
        request_body=ModeleSerializer,
        responses={200: ModeleSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Supprime un modèle existant",
        responses={204: None}
    )
    def destroy(self, request, *args, **kwargs):    
        return super().destroy(request, *args, **kwargs)

# ============================================================================
# Gestion des boutiques
# ============================================================================
class BoutiqueViewSet(viewsets.ModelViewSet):
    queryset = Boutique.objects.all()
    serializer_class = BoutiqueSerializer
    permission_classes = [EstResponsableBoutique]

    def perform_create(self, serializer):
        # Assigner automatiquement le responsable lors de la création
        serializer.save(responsable=self.request.user.profile)

    @swagger_auto_schema(
        operation_description="Liste toutes les boutiques",
        responses={200: BoutiqueSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Crée une nouvelle boutique",
        request_body=BoutiqueSerializer,
        responses={201: BoutiqueSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Récupère une boutique par son ID",
        responses={200: BoutiqueSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Met à jour une boutique existante",
        request_body=BoutiqueSerializer,
        responses={200: BoutiqueSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Supprime une boutique existante",
        responses={204: None}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        # Archiver la boutique avant de la supprimer
        ArchivedBoutique.objects.create(
            original_id=instance.boutique_id,
            nom_boutique=instance.nom_boutique,
            adresse=instance.adresse,
            ville=instance.ville,
            code_postal=instance.code_postal,
            departement=instance.departement,
            archive_par=self.request.user,
            raison=self.request.data.get('raison', 'Point de vente fermé')
        )
        instance.delete()

# ============================================================================
# Gestion des produits
# ============================================================================
class ProduitViewSet(viewsets.ModelViewSet):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer
    permission_classes = [EstGestionnaireOuResponsable]
    

    @swagger_auto_schema(
        operation_description="Crée un nouveau produit",
        request_body=ProduitSerializer,
        responses={201: ProduitSerializer()}
    )
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        operation_description="Liste tous les produits",
        responses={200: ProduitSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Récupère un produit par son ID",
        responses={200: ProduitSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Met à jour un produit existant",
        request_body=ProduitSerializer,
        responses={200: ProduitSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Envoie d'une demande de suppression d'un produit",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'raison': openapi.Schema(type=openapi.TYPE_STRING, description='Raison de la suppression')
            },
            required=['raison']
        ),
        responses={
            201: DemandeSuppressionProduitSerializer(),
            400: "Erreur lors de la création de la demande"
        }
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Vérifier si une demande de suppression existe déjà
        if DemandeSuppressionProduit.objects.filter(produit=instance, statut='EN_ATTENTE').exists():
            return Response(
                {"error": "Une demande de suppression est déjà en attente pour ce produit"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Récupérer les stocks du produit pour trouver les boutiques associées
        stocks = instance.stocks.all()
        if not stocks.exists():
            return Response(
                {"error": "Ce produit n'est associé à aucune boutique"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Créetion d'une demande de suppression pour chaque boutique associée
        demandes = []
        for stock in stocks:
            if stock.boutique.responsable:  # je vérifie si la boutique a un responsable
                try:
                    demande = DemandeSuppressionProduit.objects.create(
                        produit=instance,
                        demandeur=request.user,
                        responsable=stock.boutique.responsable,
                        raison=request.data.get('raison', '')
                    )
                    demandes.append(demande)
                except Exception as e:
                    return Response(
                        {"error": f"Erreur lors de l'envoi de la demande: {str(e)}"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
        
        if not demandes:
            return Response(
                {"error": "Aucune boutique associée n'a de responsable"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = DemandeSuppressionProduitSerializer(demandes[0])  # je renvoie la première demande
        return Response(
            {
                "message": "Demande de suppression envoyée avec succès. En attente de validation par le responsable.",
                "demande": serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    @swagger_auto_schema(
        operation_description="Validation de la suppression d'un produit par le responsable de la boutique",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'commentaire': openapi.Schema(type=openapi.TYPE_STRING, description='Commentaire du responsable')
            }
        ),
        responses={
            200: "Produit supprimé avec succès",
            403: "Vous n'avez pas les permissions nécessaires pour valider cette demande",
            404: "Demande de suppression non trouvée"
        }
    )
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def valider(self, request, pk=None):
        # Vérifier si l'utilisateur est authentifié
        if not request.user.is_authenticated:
            return Response(
                {"error": "Vous devez être connecté pour effectuer cette action"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Vérifier si l'utilisateur est un responsable
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'RESPONSABLE':
            return Response(
                {"error": "Seul un responsable peut valider une demande de suppression"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            # Récupérer le produit
            produit = self.get_object()
            
            # Récupérer la demande de suppression
            try:
                demande = DemandeSuppressionProduit.objects.get(produit=produit, statut='EN_ATTENTE')
            except DemandeSuppressionProduit.DoesNotExist:
                return Response(
                    {"error": "Demande de suppression non trouvée ou déjà traitée"},
                    status=status.HTTP_404_NOT_FOUND
                )
        except Exception as e:
            return Response(
                {"error": f"Erreur lors de la récupération du produit: {str(e)}"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Récupérer les stocks du produit
        stocks = produit.stocks.all()
        
        if not stocks.exists():
            return Response(
                {"error": "Ce produit n'est associé à aucune boutique"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Vérifier si l'utilisateur est responsable d'au moins une des boutiques du produit
        is_responsable = False
        for stock in stocks:
            if stock.boutique.responsable == request.user:
                is_responsable = True
                break

        if not is_responsable:
            return Response(
                {
                    "error": "Vous n'êtes pas le responsable d'une des boutiques de ce produit",
                    "details": {
                        "user_id": request.user.id,
                        "user_role": request.user.profile.role if hasattr(request.user, 'profile') else None,
                        "boutiques_responsable": [stock.boutique.id for stock in stocks],
                        "boutiques_responsable_names": [stock.boutique.nom_boutique for stock in stocks] if stocks else []
                    }
                },
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Archiver le produit avant de le supprimer
        ArchivedProduit.objects.create(
            original_id=produit.produit_id,
            nom_produit=produit.nom_produit,
            marque =produit.modele.marque.marque, # Nom de la marque (stocké en texte)
            modele = produit.modele.modele, 
            prix=produit.prix,
            couleur=produit.couleur,
            capacite=produit.capacite,
            ram=produit.ram,
            archive_par=request.user,
            raison=demande.raison
        )
        
        # Mettre à jour le statut de la demande
        demande.statut = 'VALIDE'
        demande.date_validation = timezone.now()
        demande.commentaire_responsable = request.data.get('commentaire', '')
        demande.save()
        
        # Supprimer le produit
        produit.delete()
        
        return Response(
            {"message": "Produit supprimé avec succès"},
            status=status.HTTP_200_OK
        )
    
    # De même pour la méthode annuler
    @swagger_auto_schema(
        operation_description="Annulation d'une demande de suppression d'un produit",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'commentaire': openapi.Schema(type=openapi.TYPE_STRING, description='Commentaire du responsable')
            }
        ),
        responses={
            200: DemandeSuppressionProduitSerializer(),
            400: "Erreur lors de l'annulation",
            403: "Non autorisé",
            404: "Demande de suppression non trouvée"
        }
    )


    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def annuler(self, request, pk=None):
       try:
            # Récupérer le produit
            produit = self.get_object()
            
            # Récupérer la demande de suppression
            try:
                demande = DemandeSuppressionProduit.objects.get(produit=produit, statut='EN_ATTENTE')
            except DemandeSuppressionProduit.DoesNotExist:
                return Response(
                    {"error": "Demande de suppression non trouvée ou déjà traitée"},
                    status=status.HTTP_404_NOT_FOUND
                )
       except Exception as e:
            return Response(
                {"error": f"Erreur lors de la récupération du produit: {str(e)}"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Vérifier que l'utilisateur est bien le responsable
       stocks = produit.stocks.all()
       is_responsable = any(stock.boutique.responsable == request.user for stock in stocks)
        
       if not is_responsable:
            return Response(
                {"error": "Vous n'êtes pas autorisé à annuler cette demande"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Mettre à jour la demande
       demande.statut = 'ANNULE'
       demande.date_validation = timezone.now()
       demande.commentaire_responsable = request.data.get('commentaire', '')
       demande.save()

       serializer = DemandeSuppressionProduitSerializer(demande)
       return Response(serializer.data)

# ============================================================================
# Gestion des stocks
# ============================================================================
class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [EstGestionnaireOuResponsable]
    http_method_names = ['get', 'put', 'head', 'options', 'post', ]  # Suppression de 'post' et 'delete'

    @swagger_auto_schema(
        operation_description="Liste tous les stocks",
        responses={200: StockSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Récupère un stock par son ID",
        responses={200: StockSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Met à jour un stock existant",
        request_body=StockSerializer,
        responses={200: StockSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def get_permissions(self):
        if self.action in ['vendre', 'update', 'partial_update']:
            return [IsAuthenticated(), EstGestionnaireOuResponsable()]
        return []  # Pas de permission requise pour la lecture

    # Surcharge des méthodes pour les désactiver explicitement
    def create(self, request, *args, **kwargs):
        return Response(
            {"error": "La création directe d'un stock n'est pas autorisée. Veuillez utiliser l'API de produits."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def destroy(self, request, *args, **kwargs):
        return Response(
            {"error": "La suppression directe d'un stock n'est pas autorisée pour préserver l'intégrité des données."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @swagger_auto_schema(
        operation_description="Liste les stocks faibles",
        responses={200: StockSerializer(many=True)}
    )
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
        # Archiver le produit deja vendu dans l'historique des ventes pour gerer la traçabilité
        HistoriqueVentes.objects.create(
            original_id=stock.produit.produit_id,
            nom_produit=stock.produit.nom_produit,
            marque=stock.produit.modele.marque.marque,
            modele=stock.produit.modele.modele,
            prix=stock.produit.prix,
            couleur=stock.produit.couleur,
            capacite=stock.produit.capacite,
            ram=stock.produit.ram,
            vendu_par=request.user,
            quantite_vendue=quantite_a_vendre,
            description="Produit vendu et archivé"
        )
        stock.save()
        serializer = self.get_serializer(stock)
        return Response({'message': 'Produit vendu et dans l\'historique des ventes', 
                         'data': serializer.data}, status=status.HTTP_200_OK)
    
# ============================================================================
# Archivage des produits et des boutiques
# ============================================================================
class ArchivedProduitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ArchivedProduit.objects.all()
    serializer_class = ArchivedProduitSerializer
    permission_classes = [EstGestionnaireOuResponsable]

    @swagger_auto_schema(
        operation_description="Liste tous les produits archivés",
        responses={200: ArchivedProduitSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Récupère un produit archivé par son ID",
        responses={200: ArchivedProduitSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

class HistoriqueVentesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HistoriqueVentes.objects.all()
    serializer_class = HistoriqueVentesSerializer
    permission_classes = [EstGestionnaireOuResponsable]

    @swagger_auto_schema(
        operation_description="Liste tous les produits deja vendus",
        responses={200: HistoriqueVentesSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Récupère un produit deja vendu par son ID",
        responses={200: HistoriqueVentesSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

class ArchivedBoutiqueViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ArchivedBoutique.objects.all()
    serializer_class = ArchivedBoutiqueSerializer
    permission_classes = [EstResponsableBoutique]

    @swagger_auto_schema(
        operation_description="Liste toutes les boutiques archivées",
        responses={200: ArchivedBoutiqueSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)  
    
    @swagger_auto_schema(
        operation_description="Récupère une boutique archivée par son ID",
        responses={200: ArchivedBoutiqueSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

