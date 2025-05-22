from django.contrib.auth.mixins import UserPassesTestMixin
from rest_framework import permissions

from.models import Produit, Boutique

class GestionnaireBoutiqueMixin(UserPassesTestMixin):
    def test_func(self):
        return (
            self.request.user.is_authenticated and 
            hasattr(self.request.user, 'boutique_geree')
        )
    
    def get_queryset(self):
        qs = super().get_queryset()
        if hasattr(self.request.user, 'boutique_geree'):
            return qs.filter(boutique=self.request.user.boutique_geree)
        return qs.none()

class EstResponsableBoutique(permissions.BasePermission):
    """
    Permission pour les responsables de boutique :
    - Un responsable ne peut modifier que sa propre boutique
    - Un responsable ne peut agir que sur les produits de sa boutique
    """
    def has_permission(self, request, view):
        # Permettre l'accès en lecture à tout le monde
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
            
        # Vérifier l'authentification et le rôle pour les autres méthodes
        if not request.user.is_authenticated:
            return False
            
        if request.user.is_superuser:
            return True
            
        if hasattr(request.user, 'profile'):
            return request.user.profile.role == 'RESPONSABLE'
            
        return False

    def has_object_permission(self, request, view, obj):
        # Permettre GET à tout le monde
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Pour les autres méthodes, vérifier si c'est un responsable ou un superuser
        if not request.user.is_authenticated:
            return False
            
        if request.user.is_superuser:
            return True
            
        # Si l'objet est une boutique
        if hasattr(obj, 'responsable'):
            return obj.responsable == request.user
                    
        # Si l'objet est un produit ou un stock
        if hasattr(obj, 'boutique'):
            return obj.boutique.responsable == request.user
            
        return False

class PeuModifierUserProfile(permissions.BasePermission):
    """
    Permission pour les gestionnaires de boutique :
    - Un gestionnaire ne peut agir que sur les produits des boutiques où il travaille
    """
    def has_permission(self, request, view):
        # Permettre GET à tout le monde
        if request.method in permissions.SAFE_METHODS:
            return True
        # Pour les autres méthodes, vérifier si c'est un gestionnaire
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        try:
            return request.user.profile.role == 'RESPONSABLE'
        except:
            return False

    def has_object_permission(self, request, view, obj):
        # Permettre GET à tout le monde
        if request.method in permissions.SAFE_METHODS:
            return True
        # Pour les autres méthodes, vérifier si c'est un gestionnaire de la boutique
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        try:
            if request.user.profile.role == 'RESPONSABLE':
                return True
            else:
                return False
        except:
            return False

class EstGestionnaireOuResponsable(permissions.BasePermission):
    """
    Permission combinée pour les gestionnaires et responsables :
    - Lecture autorisée à tous les utilisateurs authentifiés
    - Écriture autorisée uniquement aux responsables et gestionnaires
    - Un responsable ne peut agir que sur les produits de sa boutique
    - Un gestionnaire ne peut agir que sur les produits des boutiques où il travaille
    """
    def has_permission(self, request, view):
        # Permettre l'accès en lecture à tout le monde
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
            
        # Vérifier l'authentification et les rôles pour les autres méthodes
        if not request.user.is_authenticated:
            return False
            
        if request.user.is_superuser:
            return True
            
        if not hasattr(request.user, 'profile'):
            return False

        role = request.user.profile.role
        if role not in ['RESPONSABLE', 'GESTIONNAIRE']:
            return False

        # Vérifier les permissions pour la création de produit
        if request.method == 'POST' and view.get_queryset().model == Produit:
            boutique_id = request.data.get('boutique_id')
            if not boutique_id:
                return False

            try:
                boutique = Boutique.objects.get(boutique_id=boutique_id)
                if role == 'RESPONSABLE':
                    return boutique.responsable == request.user
                elif role == 'GESTIONNAIRE':
                    return request.user in boutique.gestionnaires.all()
            except Boutique.DoesNotExist:
                return False

        return True

    def has_object_permission(self, request, view, obj):
        # Permettre GET à tout le monde
        if request.method in permissions.SAFE_METHODS:
            return True
            
        if not request.user.is_authenticated:
            return False
            
        # Le superuser peut tout faire
        if request.user.is_superuser:
            return True
            
        # Vérifier les permissions spécifiques selon le rôle
        try:
            role = request.user.profile.role
            
            # Si l'objet est un produit
            if isinstance(obj, Produit):
                # Récupérer les stocks du produit
                stocks = obj.stocks.all()
                if not stocks.exists():
                    return False
                
                if role == 'RESPONSABLE':
                    # Un responsable ne peut agir que sur les produits de sa boutique
                    return any(stock.boutique.responsable == request.user for stock in stocks)
                elif role == 'GESTIONNAIRE':
                    # Un gestionnaire ne peut agir que sur les produits des boutiques où il travaille
                    return any(request.user in stock.boutique.gestionnaires.all() for stock in stocks)
                return False
            
            # Si l'objet est une boutique
            if hasattr(obj, 'responsable'):
                if role == 'RESPONSABLE':
                    return obj.responsable == request.user
                elif role == 'GESTIONNAIRE':
                    return request.user in obj.gestionnaires.all()
                return False
            
            # Si l'objet est un stock
            if hasattr(obj, 'boutique'):
                if role == 'RESPONSABLE':
                    return obj.boutique.responsable == request.user
                elif role == 'GESTIONNAIRE':
                    return request.user in obj.boutique.gestionnaires.all()
                return False
            
            return False
        except:
            return False