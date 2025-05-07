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
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, ArchivedUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'}, required=False)
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = UserProfile
        fields = ['id', 'role', 'telephone', 'username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user_data = {
            'username': validated_data.pop('username'),
            'email': validated_data.pop('email'),
            'password': validated_data.pop('password'),
            'first_name': validated_data.pop('first_name', ''),
            'last_name': validated_data.pop('last_name', '')
        }
        user = User.objects.create_user(**user_data)
        profile = UserProfile.objects.create(user=user, **validated_data)
        return profile

    def update(self, instance, validated_data):
        # Mise à jour des données de l'utilisateur
        user = instance.user
        if 'username' in validated_data:
            user.username = validated_data.pop('username')
        if 'email' in validated_data:
            user.email = validated_data.pop('email')
        if 'password' in validated_data:
            user.set_password(validated_data.pop('password'))
        if 'first_name' in validated_data:
            user.first_name = validated_data.pop('first_name')
        if 'last_name' in validated_data:
            user.last_name = validated_data.pop('last_name')
        user.save()

        # Mise à jour du profil
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user_data = {
            'username': instance.user.username,
            'email': instance.user.email,
            'first_name': instance.user.first_name,
            'last_name': instance.user.last_name
        }
        representation.update(user_data)
        return representation

class ArchivedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchivedUser
        fields = '__all__'
        read_only_fields = ['date_archivage', 'archive_par'] 