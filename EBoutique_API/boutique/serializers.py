from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Marque, Modele, Boutique, Produit, Stock,
    ArchivedProduit, ArchivedBoutique
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

class ModeleSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Modele.
    Inclut les détails de la marque associée dans la représentation.
    """
    class Meta:
        model = Modele
        fields = '__all__'

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
            nom=instance.nom,
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
    boutique_id = serializers.IntegerField(write_only=True)  # ID de la boutique pour le stock initial
    quantite_initiale = serializers.IntegerField(write_only=True, default=1, min_value=1)  # Quantité initiale en stock

    class Meta:
        model = Produit
        fields = '__all__'
        read_only_fields = ['user']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['modele'] = ModeleSerializer(instance.modele).data
        return representation

    def create(self, validated_data):
        """
        Crée un produit et son stock initial dans la boutique spécifiée.
        """
        boutique_id = validated_data.pop('boutique_id')
        quantite_initiale = validated_data.pop('quantite_initiale', 1)
        
        # Créer le produit
        validated_data['user'] = self.context['request'].user
        produit = super().create(validated_data)
        
        # Créer l'entrée dans le stock
        Stock.objects.create(
            boutique_id=boutique_id,
            produit=produit,
            quantite=quantite_initiale
        )
        
        return produit

class StockSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Stock.
    Gère la gestion des stocks et l'archivage automatique des produits épuisés.
    """
    produit_nom = serializers.CharField(source='produit.nom', read_only=True)  # Nom du produit en lecture seule
    boutique_nom = serializers.CharField(source='boutique.nom', read_only=True)  # Nom de la boutique en lecture seule

    class Meta:
        model = Stock
        fields = '__all__'

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
                    nom=instance.produit.nom,
                    marque=instance.produit.marque.nom,
                    modele=instance.produit.modele.nom,
                    prix=instance.produit.prix,
                    couleur=instance.produit.couleur,
                    capacite=instance.produit.capacite,
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

class ArchivedBoutiqueSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle ArchivedBoutique.
    Lecture seule pour consulter l'historique des boutiques archivées.
    """
    class Meta:
        model = ArchivedBoutique
        fields = '__all__'
        read_only_fields = ['date_archivage', 'archive_par'] 