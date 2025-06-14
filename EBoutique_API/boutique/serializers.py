from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Marque, Modele, Boutique, Produit, Stock,
    ArchivedProduit, ArchivedBoutique, HistoriqueVentes, DemandeSuppressionProduit
)

# ============================================================================
# Serializers pour les modèles de base
# ============================================================================

class MarqueSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Marque.
    Permet la sérialisation/désérialisation des marques de téléphones.
    """
    class Meta:
        model = Marque
        fields = '__all__'
        extra_kwargs = {
            'marque_id': {'read_only': True}
        }

class ModeleSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Modele.
    Inclut les détails de la marque associée dans la représentation.
    """
    class Meta:
        model = Modele
        fields = '__all__'
        extra_kwargs = {
            'modele_id': {'read_only': True}
        }

    def to_representation(self, instance):
        """
        Personnalise la représentation du modèle en incluant les détails de la marque.
        """
        representation = super().to_representation(instance)
        representation['marque'] = MarqueSerializer(instance.marque).data
        return representation

# ============================================================================
# Serializers pour les utilisateurs
# ============================================================================

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer pour les utilisateurs.
    Inclut les informations de base de l'utilisateur.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class ResponsableSerializer(serializers.ModelSerializer):
    """
    Serializer pour les responsables de boutique.
    Limite les champs aux informations essentielles.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class GestionnaireSerializer(serializers.ModelSerializer):
    """
    Serializer pour les gestionnaires de boutique.
    Utilise les mêmes champs que le ResponsableSerializer.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

# ============================================================================
# Serializers pour les modèles principaux
# ============================================================================

class BoutiqueSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Boutique.
    Gère la sérialisation des informations de la boutique et de son personnel.
    """
    class Meta:
        model = Boutique
        fields = '__all__'
        read_only_fields = ['date_creation', 'date_maj']
        extra_kwargs = {
            'boutique_id': {'read_only': True}
        }

    def to_representation(self, instance):
        """
        Personnalise la représentation de la boutique en incluant les détails du responsable
        et des gestionnaires.
        """
        representation = super().to_representation(instance)
        representation['responsable'] = ResponsableSerializer(instance.responsable).data
        representation['gestionnaires'] = GestionnaireSerializer(instance.gestionnaires.all(), many=True).data
        return representation

    def destroy(self, instance):
        """
        Gère la suppression d'une boutique en créant une archive avant la suppression.
        """
        ArchivedBoutique.objects.create(
            original_id=instance.id,
            nom_boutique=instance.nom_boutique,
            adresse=instance.adresse,
            ville=instance.ville,
            code_postal=instance.code_postal,
            departement=instance.departement,
            longitude=instance.longitude,
            latitude=instance.latitude,
            archive_par=self.context['request'].user,
            raison="Point de vente fermé"
        )
        instance.delete()

class ProduitSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Produit.
    Gère la création de produits et leur stock initial.
    """
    boutique_id = serializers.IntegerField(write_only=True, required=False)  # ID de la boutique pour le stock initial
    quantite_initiale = serializers.IntegerField(write_only=True, default=1, min_value=1)  # Quantité initiale en stock
    boutiques = serializers.SerializerMethodField()  # Champ pour les informations des boutiques

    class Meta:
        model = Produit
        fields = '__all__'
        read_only_fields = ['user', 'validation_responsable']
        extra_kwargs = {
            'produit_id': {'read_only': True}
        }

    def get_boutiques(self, obj):
        """
        Récupère les informations des boutiques associées au produit via la table Stock.
        """
        stocks = obj.stocks.all()
        boutiques_info = []
        for stock in stocks:
            try:
                boutiques_info.append({
                    'boutique_id': stock.boutique.boutique_id,
                    'nom_boutique': stock.boutique.nom_boutique,
                    'quantite': stock.quantite
                })
            except (Boutique.DoesNotExist, AttributeError):
                continue
        return boutiques_info

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['modele'] = ModeleSerializer(instance.modele).data
        representation['user'] = UserSerializer(instance.user).data
        return representation

    def create(self, validated_data):
        """
        Crée un produit et son stock initial dans la boutique spécifiée.
        """
        boutique_id = validated_data.pop('boutique_id', None)
        quantite_initiale = validated_data.pop('quantite_initiale', 1)
        
        # Créer le produit
        validated_data['user'] = self.context['request'].user
        produit = super().create(validated_data)
        
        # Créer l'entrée dans le stock si une boutique est spécifiée
        if boutique_id is not None:
            try:
                Stock.objects.create(
                    boutique_id=boutique_id,
                    produit=produit,
                    quantite=quantite_initiale
                )
            except Exception as e:
                # Si la création du stock échoue, supprimer le produit
                produit.delete()
                raise serializers.ValidationError(f"Erreur lors de la création du stock: {str(e)}")
        
        return produit

    def update(self, instance, validated_data):
        """
        Met à jour un produit et gère son stock dans la boutique spécifiée.
        """
        boutique_id = validated_data.pop('boutique_id', None)
        quantite_initiale = validated_data.pop('quantite_initiale', 1)

        # Mettre à jour le produit
        instance = super().update(instance, validated_data)

        # Gérer le stock si une boutique est spécifiée
        if boutique_id is not None:
            try:
                # Vérifier si un stock existe déjà pour cette boutique
                stock, created = Stock.objects.get_or_create(
                    boutique_id=boutique_id,
                    produit=instance,
                    defaults={'quantite': quantite_initiale}
                )
                
                # Si le stock existait déjà, mettre à jour la quantité
                if not created:
                    stock.quantite = quantite_initiale
                    stock.save()
            except Exception as e:
                raise serializers.ValidationError(f"Erreur lors de la mise à jour du stock: {str(e)}")

        return instance

class StockSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Stock.
    Gère la gestion des stocks et l'archivage automatique des produits épuisés.
    """
    produit_nom = serializers.CharField(source='produit.nom_produit', read_only=True)
    boutique_nom = serializers.CharField(source='boutique.nom_boutique', read_only=True)

    class Meta:
        model = Stock
        fields = '__all__'
        extra_kwargs = {
            'stock_id': {'read_only': True}
        }

    def update(self, instance, validated_data):
        """
        Met à jour le stock et archive automatiquement le produit si le stock est épuisé.
        """
        if 'quantite' in validated_data:
            nouvelle_quantite = validated_data['quantite']
            if nouvelle_quantite <= 0:
                # Archiver le produit
                ArchivedProduit.objects.create(
                    original_id=instance.produit.id,
                    nom_produit=instance.produit.nom_produit,
                    marque=instance.produit.modele.marque.marque,
                    modele=instance.produit.modele.modele,
                    prix=instance.produit.prix,
                    couleur=instance.produit.couleur,
                    capacite=instance.produit.capacite,
                    ram=instance.produit.ram,
                    archive_par=self.context['request'].user,
                    raison="Stock épuisé"
                )
                # Supprimer le produit
                instance.produit.delete()
                return instance
        
        return super().update(instance, validated_data)

# ============================================================================
# Serializers pour les archives
# ============================================================================

class ArchivedProduitSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle ArchivedProduit.
    Lecture seule pour consulter l'historique des produits archivés.
    """
    class Meta:
        model = ArchivedProduit
        fields = '__all__'
        read_only_fields = ['date_archivage', 'archive_par']

class HistoriqueVentesSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle HistoriqueVentes.
    Lecture seule pour consulter l'historique des produits deja vendus.
    """
   
    class Meta:
        model = HistoriqueVentes
        fields = '__all__'
        read_only_fields = ['date_vente', 'vendu_par']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['vendu_par'] = UserSerializer(instance.vendu_par).data
        return representation

class ArchivedBoutiqueSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle ArchivedBoutique.
    Lecture seule pour consulter l'historique des boutiques archivées.
    """
    class Meta:
        model = ArchivedBoutique
        fields = '__all__'
        read_only_fields = ['date_archivage', 'archive_par']

# ============================================================================
# Serializers pour les demandes de suppression de produits
# ============================================================================

class DemandeSuppressionProduitSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle DemandeSuppressionProduit.
    Gère la création et la validation des demandes de suppression.
    """
    produit_details = ProduitSerializer(source='produit', read_only=True)
    demandeur_details = UserSerializer(source='demandeur', read_only=True)
    responsable_details = UserSerializer(source='responsable', read_only=True)
    produit = serializers.PrimaryKeyRelatedField(queryset=Produit.objects.all(), write_only=True)

    class Meta:
        model = DemandeSuppressionProduit
        fields = '__all__'
        read_only_fields = ['date_demande', 'date_validation', 'statut', 'commentaire_responsable', 'demandeur', 'responsable']

    def create(self, validated_data):
        """
        Crée une demande de suppression et associe automatiquement le responsable de la boutique.
        """
        produit = validated_data['produit']
        # Récupérer le responsable de la boutique associée au produit
        stock = produit.stocks.first()
        if stock and stock.boutique.responsable:
            validated_data['responsable'] = stock.boutique.responsable
        validated_data['demandeur'] = self.context['request'].user
        return super().create(validated_data) 