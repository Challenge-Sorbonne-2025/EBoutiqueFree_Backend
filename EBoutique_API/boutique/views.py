from django.shortcuts import render
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

from rest_framework.permissions import AllowAny

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
    ArchivedBoutiqueSerializer, HistoriqueVentesSerializer, CSVImportSerializer, ProduitBulkCreateSerializer,
    DemandeSuppressionProduitSerializer, BoutiqueBulkCreateSerializer, BoutiqueCSVImportSerializer
)
from .permissions import EstResponsableBoutique, EstGestionnaireOuResponsable
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

from boutique.models import Boutique, Stock
from free_app.models import UserProfile

from django.views.decorators.http import require_GET
import csv
import io
from django.db import transaction
from rest_framework.parsers import MultiPartParser, FormParser



@require_GET
def map_view(request):
    # l'utilisateur peut entrer une adresse ou utiliser la géolocalisation
    return render(request, "boutique/map.html")

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
        

        # calculer la localisation de la boutique
        location = Point(float(self.request.data.get('longitude')),
            float(self.request.data.get('latitude')),
            srid=4326
        )
        serializer.save(responsable=self.request.user.profile,location=location)


    def perform_update(self, serializer):
        location = Point(float(self.request.data.get('longitude')),
            float(self.request.data.get('latitude')),
            srid=4326
        )
        save_kwargs = {}
        if location:
            save_kwargs['location'] = location
            
        serializer.save(**save_kwargs)
       

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
        operation_description="Met à jour partiellement une boutique existante",
        request_body=BoutiqueSerializer,
        responses={200: BoutiqueSerializer()}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

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

    
    @swagger_auto_schema(
    operation_description="Ajout de plusieurs boutiques en masse via fichier CSV",
    consumes=['multipart/form-data'],
    responses={
        200: openapi.Response(
            description="Import réussi",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING, example='5 boutique(s) importée(s) avec succès'),
                    'boutiques_creees': openapi.Schema(type=openapi.TYPE_INTEGER, example=5),
                    'erreurs': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING))
                }
            )
        ),
        400: openapi.Response(
            description="Erreur de validation du fichier CSV",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'erreur': openapi.Schema(type=openapi.TYPE_STRING),
                    'erreurs': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
                    'colonnes_attendues': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING))
                }
            )
        ),
        500: openapi.Response(
            description="Erreur serveur",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'erreur': openapi.Schema(type=openapi.TYPE_STRING)
                 }
                )
            )
        }
        )
    @action(
    detail=False, 
    methods=['post'], 
    permission_classes=[EstResponsableBoutique],
    url_path='import_csv',  
    parser_classes=[MultiPartParser, FormParser],
    # Spécifier explicitement le serializer pour éviter la génération automatique
    serializer_class=BoutiqueCSVImportSerializer
    )
    def import_csv(self, request):
        """
        Importer des boutiques à partir d'un fichier CSV.
        
        Format du fichier CSV attendu:
        nom_boutique,adresse,ville,code_postal,departement,latitude,longitude,responsable
        Boutique Test,123 Rue Example,Paris,75001,Paris,48.8566,2.3522,1,2
        """
        # Vérifier que seul le fichier CSV est fourni
        if len(request.data) > 1 or 'fichier_csv' not in request.data:
            return Response({
                'erreur': 'Seul le fichier CSV doit être fourni. Aucun autre paramètre n\'est nécessaire.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = BoutiqueCSVImportSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        fichier_csv = serializer.validated_data['fichier_csv']

        try: 
            # Lire le contenu du fichier CSV
            contenu = fichier_csv.read().decode('utf-8')
            csv_reader = csv.DictReader(io.StringIO(contenu))
            
            boutiques_a_creer = []
            erreurs = []
            ligne_numero = 1  # Commencer à 1 pour ignorer l'en-tête

            # Colonnes attendues
            colonnes_attendues = ['nom_boutique', 'adresse', 'ville', 'code_postal', 
            'departement', 'latitude', 'longitude', 'responsable',]   

            if not all(col in csv_reader.fieldnames for col in colonnes_attendues):
                colonnes_manquantes = [col for col in colonnes_attendues if col not in csv_reader.fieldnames]
                return Response({
                    'erreur': f"Colonnes manquantes dans le CSV: {', '.join(colonnes_manquantes)}",
                    'colonnes_attendues': colonnes_attendues,
                    'colonnes_trouvees': list(csv_reader.fieldnames)
                }, status=status.HTTP_400_BAD_REQUEST)

            for ligne in csv_reader:
                ligne_numero += 1
                
                # Nettoyer les données (supprimer les espaces)
                ligne_nettoyee = {k: v.strip() if isinstance(v, str) else v for k, v in ligne.items()}
                
                # Valider la ligne avec le serializer
                boutique_serializer = BoutiqueBulkCreateSerializer(data=ligne_nettoyee)
                
                if boutique_serializer.is_valid():
                    boutiques_a_creer.append(boutique_serializer.validated_data)
                else:
                    erreurs.append(f"Ligne {ligne_numero}: {boutique_serializer.errors}")
            
            # Si il y a des erreurs, on ne crée rien
            if erreurs:
                return Response({
                    'message': 'Erreurs détectées dans le fichier CSV',
                    'erreurs': erreurs,
                    'boutiques_validees': len(boutiques_a_creer),
                    'total_lignes': ligne_numero - 1
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Créer les boutiques en une seule transaction
            boutiques_creees = 0
            with transaction.atomic():
                for donnees_boutique in boutiques_a_creer:
                    # Créer le point géographique
                    location = Point(
                        float(donnees_boutique['longitude']),
                        float(donnees_boutique['latitude']),
                        srid=4326
                    )

                    donnees_creation = donnees_boutique.copy()
                
                # Gérer le responsable
                    if 'responsable' in donnees_creation:
                        # Si un responsable est spécifié dans le CSV, l'utiliser
                        responsable_id = donnees_creation.pop('responsable')
                        try:
                            responsable = UserProfile.objects.get(profile_id=responsable_id)
                        except UserProfile.DoesNotExist:
                            # Si le responsable n'existe pas, utiliser l'utilisateur actuel
                            responsable = request.user.profile
                    else:
                        # Si pas de responsable spécifié, utiliser l'utilisateur actuel
                        responsable = request.user.profile
                        
                    # Créer la boutique
                    Boutique.objects.create(
                        responsable=responsable,
                        location=location,
                        **donnees_creation
                    )
                    boutiques_creees += 1
            
            return Response({
                'message': f'{boutiques_creees} boutique(s) importée(s) avec succès',
                'boutiques_creees': boutiques_creees,
                'erreurs': []
            }, status=status.HTTP_200_OK)
            
        except UnicodeDecodeError:
            return Response({
                'erreur': 'Erreur d\'encodage du fichier. Assurez-vous que le fichier est encodé en UTF-8'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'erreur': f'Erreur lors du traitement du fichier: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  

    @swagger_auto_schema(
        operation_description="Recherche de boutiques par nom_boutique, adresse, ville, departement ou code postal",
        manual_parameters=[
            openapi.Parameter('query', openapi.IN_QUERY, description="Recherche par nom_boutique, adresse, ville, departement ou code postal",
                              type=openapi.TYPE_STRING)
        ],  
        responses={200: BoutiqueSerializer(many=True)}  
    )
    @action(detail=False, methods=['get'])  
    def search_boutique(self, request):
        query = request.query_params.get('query', '')
        if not query:
            return Response(
                {"error": "Aucun critère de recherche fourni"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        boutiques = self.queryset.filter(
            nom_boutique__icontains=query
        ) | self.queryset.filter(
            adresse__icontains=query
        ) | self.queryset.filter(
            ville__icontains=query
        ) | self.queryset.filter(
            departement__icontains=query
        ) | self.queryset.filter(
            code_postal__icontains=query
        )
        
        serializer = self.get_serializer(boutiques, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Récupère les boutiques a proximite d'un client avec au moins un produit en stock",   
        responses={
            200: BoutiqueSerializer(many=True),
            400: "Erreur de validation des paramètres"
        }
    )
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])   
    def boutiques_proches(self, request):
        latitude = request.GET.get('latitude')
        longitude = request.GET.get('longitude')
        try:
            latitude = float(latitude)
            longitude = float(longitude)

        except (ValueError, TypeError):
            return Response(
                {"error": "Paramètres de latitude, longitude invalides"},
                status=status.HTTP_400_BAD_REQUEST
            )   
        if not latitude or not longitude:
            return Response(
                {"error": "Latitude et longitude sont obligatoires"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Calculer le point géographique du client
        client_location = Point(longitude, latitude, srid=4326)
        # client_lambert93 = client_location.transform(2154, clone=True)  # Convertir en Lambert 93
        # Filtrer les boutiques à proximité avec au moins un produit en stock en une distance de 20 km
        boutiques_proches = Boutique.objects.filter(
            location__distance_lte=(client_location, 20000) # 20 km
        ).annotate(distance=Distance('location', client_location)).order_by('distance')

        resultats = []
        if not boutiques_proches:
            return Response(
                {"message": "Aucune boutique trouvée dans un rayon de 20 km."},
                status=status.HTTP_404_NOT_FOUND
            )
        else:
            for boutique in boutiques_proches:
                # Filtrer les stocks avec quantite > 0
                stocks = boutique.stocks.filter(quantite__gt=0).select_related(
                    'produit', 'produit__modele__marque', 'produit__modele'
                )
                for stock in stocks:
                    resultats.append({
                        "boutique": boutique.nom_boutique,
                        "ville": boutique.ville,
                        "latitude": boutique.latitude,
                        "longitude": boutique.longitude,
                        "adresse": boutique.adresse,
                        "code_postal": boutique.code_postal,
                        "departement": boutique.departement,                        
                        "produit": stock.produit.nom_produit,
                        "marque": stock.produit.modele.marque.marque,
                        "modele": stock.produit.modele.modele,
                        "prix": float(stock.produit.prix),
                        "quantite": stock.quantite,
                    })
                    break
                if len(resultats) >= 5:
                    break  # Affichage des 5 premiers résultats
            if not resultats:
                return Response(
                    {"message": "Aucun produit trouvé dans un rayon de 20 km."},
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(resultats, status=status.HTTP_200_OK)
    

    @swagger_auto_schema(
        operation_description="Recuperer tous les produits d'une boutique",
        manual_parameters=[
            openapi.Parameter('boutique_id', openapi.IN_QUERY, description="ID de la boutique",
                              type=openapi.TYPE_INTEGER)
        ],      
        responses={
            200: ProduitSerializer(many=True),
            400: "Erreur de validation des paramètres"
        }
    )
    @action(detail=False, methods=['get'], permission_classes=[EstGestionnaireOuResponsable])
    def getProduitByBoutiqueId(self, request):
        boutique_id = request.query_params.get('boutique_id')
        if not boutique_id:
            return Response(
                {"error": "ID de la boutique est obligatoire"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            boutique = Boutique.objects.get(boutique_id=boutique_id)
        except Boutique.DoesNotExist:
            return Response(
                {"error": "Boutique non trouvée"},
                status=status.HTTP_404_NOT_FOUND
            )
        # recuperer tous les produits de la boutique
        produits = Produit.objects.filter(stocks__boutique=boutique).distinct()
        serializer = ProduitSerializer(produits, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
     

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
    

    @swagger_auto_schema(
        operation_description="Recherche de produit par nom, marque ou modele",
        manual_parameters=[
            openapi.Parameter('query', openapi.IN_QUERY, description="Recherche par nom, marque ou modele",
                              type=openapi.TYPE_STRING)
        ],
        responses={200: ProduitSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])   
    def search_product(self, request):
        query = request.query_params.get('query', '')
        if not query:
            return Response(
                {"error": "Aucun critère de recherche fourni"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        produits = self.queryset.filter(
            nom_produit__icontains=query
        ) | self.queryset.filter(
            modele__marque__marque__icontains=query
        ) | self.queryset.filter(
            modele__modele__icontains=query
        )
        
        serializer = self.get_serializer(produits, many=True)
        return Response(serializer.data)


    @swagger_auto_schema(
        operation_description="Ajouter plusieurs produits en masse via fichier CSV",
        consumes=['multipart/form-data'],  
        responses={
            201: openapi.Response(
                description="Import réussi",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, example='5 produit(s) importé(s) avec succès'),
                        'produits_crees': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_INTEGER)),
                        'erreurs': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT))
                    }
                )
            ),
            400: openapi.Response(
                description="Erreur de validation du fichier CSV",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'erreur': openapi.Schema(type=openapi.TYPE_STRING),
                        'erreurs': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT)),
                        'colonnes_attendues': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING))
                    }
                )
            ),
            500: openapi.Response(
                description="Erreur serveur",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'erreur': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            )
        } 
    )
    @action(
        detail=False,
        methods=['post'],
        permission_classes=[AllowAny],  
        url_path='import_csv',  # URL personnalisée pour l'import CSV
        parser_classes=[MultiPartParser, FormParser],  # Pour gérer les fichiers multipart/form-data
        serializer_class=CSVImportSerializer,)
    def import_csv(self, request):

        if len(request.data) > 1 or 'csv_file' not in request.data:
            return Response({
                'erreur': 'Seul le fichier CSV doit être fourni. Aucun autre paramètre n\'est nécessaire.'
            }, status=status.HTTP_400_BAD_REQUEST)      
        # Valider le fichier CSV avec le serializer
        serializer = CSVImportSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        fichier_csv = serializer.validated_data['csv_file']
        try:
            # Lire le contenu du fichier CSV
            contenu = fichier_csv.read().decode('utf-8')
            csv_reader = csv.DictReader(io.StringIO(contenu))

            produits_a_creer = []   
            erreurs = []
            ligne_numero = 1  # Commencer à 1 pour ignorer l'en-tête

            # Colonnes attendues
            colonnes_attendues = [
                'boutique_id', 'nom_produit',
                'prix','couleur',  'capacite', 'ram', 'modele', 'image']   
            if not all(col in csv_reader.fieldnames for col in colonnes_attendues):
                colonnes_manquantes = [col for col in colonnes_attendues if col not in csv_reader.fieldnames]
                return Response({
                    'erreur': f"Colonnes manquantes dans le CSV: {', '.join(colonnes_manquantes)}",
                    'colonnes_attendues': colonnes_attendues,
                    'colonnes_trouvees': list(csv_reader.fieldnames)
                }, status=status.HTTP_400_BAD_REQUEST)

            for ligne in csv_reader:
                ligne_numero += 1
                
                # Nettoyer les données (supprimer les espaces)
                ligne_nettoyee = {k: v.strip() if isinstance(v, str) else v for k, v in ligne.items()}
                
                # Valider la ligne avec le serializer
                produit_serializer = ProduitBulkCreateSerializer(data=ligne_nettoyee, context={'request': request})   
                
                if produit_serializer.is_valid():
                    produits_a_creer.append(produit_serializer.validated_data)
                else:
                    erreurs.append({
                        'ligne': ligne_numero,
                        'erreurs': produit_serializer.errors,
                        'data': ligne_nettoyee
                    })   

            # Si il y a des erreurs, on ne crée rien
            if erreurs:
                return Response({
                    'message': 'Erreurs détectées dans le fichier CSV',
                    'erreurs': erreurs,
                    'produits_valides': len(produits_a_creer),
                    'total_lignes': ligne_numero - 1
                }, status=status.HTTP_400_BAD_REQUEST)     

            # Créer les produits en une seule transaction
            produits_crees = 0
            with transaction.atomic():
                for index, donnees_produit in enumerate(produits_a_creer, start=2):
                    # Gérer le modèle et la boutique
                    modele = Modele.objects.get(modele_id=donnees_produit['modele'])
                 
                    
                    user = request.user # Récupérer le profil de l'utilisateur connecté
                    # Créer le produit
                    produit = Produit.objects.create(
                        nom_produit=donnees_produit['nom_produit'],
                        prix=donnees_produit['prix'],
                        couleur=donnees_produit['couleur'],
                        capacite=donnees_produit['capacite'],
                        ram=donnees_produit['ram'],
                        modele=modele,
                        image=donnees_produit.get('image', None),
                        user=user,
                    )
                    
                    # Associer le produit à la boutique
                    boutique_id = donnees_produit['boutique_id']
                    try:
                        boutique = Boutique.objects.get(boutique_id=boutique_id)
                    except Boutique.DoesNotExist:
                        erreurs.append({
                            'ligne': index,
                            'erreur': f"Boutique avec ID {boutique_id} non trouvée",
                            'data': donnees_produit
                        })
                        continue
                    
                    # Créer le stock pour la boutique
                    Stock.objects.create(
                        produit=produit,
                        boutique=boutique,
                        quantite=donnees_produit.get('quantite_initiale', 10)
                    )
                    
                    produits_crees += 1
                
                return Response({
                    'message': f'{produits_crees} produit(s) importé(s) avec succès',
                    'produits_crees': produits_crees,
                    'erreurs': erreurs
                }, status=status.HTTP_201_CREATED)
        except UnicodeDecodeError:
            return Response({
                'erreur': 'Erreur d\'encodage du fichier. Assurez-vous que le fichier est encodé en UTF-8'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'erreur': f'Erreur lors du traitement du fichier: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        return super().create(request, *args, **kwargs)

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
