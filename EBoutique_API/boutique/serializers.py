from rest_framework import serializers
from .models import (
    Marque, Modele, Boutique, Produit, Stock,
    ArchivedProduit, ArchivedBoutique
)
from django.contrib.auth.models import User

class MarqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marque
        fields = '__all__'

class ModeleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modele
        fields = '__all__'

class BoutiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boutique
        fields = '__all__'
        read_only_fields = ['date_creation', 'date_maj']

class ProduitSerializer(serializers.ModelSerializer):
    marque_nom = serializers.CharField(source='marque.nom', read_only=True)
    modele_nom = serializers.CharField(source='modele.nom', read_only=True)
    boutique_id = serializers.IntegerField(write_only=True)
    quantite_initiale = serializers.IntegerField(write_only=True, default=1, min_value=1)

    class Meta:
        model = Produit
        fields = '__all__'
        read_only_fields = ['user']

    def create(self, validated_data):
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
    produit_nom = serializers.CharField(source='produit.nom', read_only=True)
    boutique_nom = serializers.CharField(source='boutique.nom', read_only=True)

    class Meta:
        model = Stock
        fields = '__all__'

    def update(self, instance, validated_data):
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
                # Supprimer le produit (cela supprimera aussi l'entrée de stock à cause de la relation)
                instance.produit.delete()
                return instance
        
        return super().update(instance, validated_data)

class ArchivedProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchivedProduit
        fields = '__all__'
        read_only_fields = ['date_archivage', 'archive_par']

class ArchivedBoutiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchivedBoutique
        fields = '__all__'
        read_only_fields = ['date_archivage', 'archive_par'] 