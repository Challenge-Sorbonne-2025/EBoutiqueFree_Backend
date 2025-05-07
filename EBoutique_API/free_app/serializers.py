# free_app/serializers.py
from rest_framework import serializers
from .models import Produit, Marque, Modele, Boutique, Stock
from .models import GestionnaireStock

class MarqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marque
        fields = '__all__'

class ModeleSerializer(serializers.ModelSerializer):
    marque = MarqueSerializer()
    class Meta:
        model = Modele
        fields = '__all__'

class ProduitSerializer(serializers.ModelSerializer):
    modele = ModeleSerializer()
    class Meta:
        model = Produit
        fields = '__all__'

class BoutiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boutique
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    boutique = BoutiqueSerializer()
    produit = ProduitSerializer()
    class Meta:
        model = Stock
        fields = '__all__'
class GestionnaireStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = GestionnaireStock
        fields = '__all__'
