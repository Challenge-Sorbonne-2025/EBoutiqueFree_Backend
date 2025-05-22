#@ -0,0 +1,26 @@
from rest_framework import serializers
from boutique.models import Produit
from django.contrib.auth.models import User

class ProductSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Produit
        fields = ['id', 'name', 'description', 'price', 'stock', 'created_at', 'updated_at', 'created_by']

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    products = serializers.PrimaryKeyRelatedField(many=True, queryset=Produit.objects.all(), required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'products']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user 
    

# free_app/serializers.py
from rest_framework import serializers
from .models import UserProfile, ArchivedUser
from django.contrib.auth.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'}, required=True)
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = UserProfile
        fields = ['profile_id', 'role', 'telephone', 'username', 'email', 'password', 'first_name', 'last_name']

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