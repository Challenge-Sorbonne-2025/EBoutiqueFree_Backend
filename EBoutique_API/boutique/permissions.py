from django.contrib.auth.mixins import UserPassesTestMixin
from rest_framework import permissions

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
        # Pour les autres méthodes, vérifier si c'est un responsable
        return request.user.is_authenticated and request.user.is_superuser

class EstGestionnaireBoutique(permissions.BasePermission):
    def has_permission(self, request, view):
        # Permettre GET à tout le monde
        if request.method in permissions.SAFE_METHODS:
            return True
        # Pour les autres méthodes, vérifier si c'est un gestionnaire
        if not request.user.is_authenticated:
            return False
        try:
            return request.user.profile.role == 'GESTIONNAIRE'
        except:
            return False

    def has_object_permission(self, request, view, obj):
        # Permettre GET à tout le monde
        if request.method in permissions.SAFE_METHODS:
            return True
        # Pour les autres méthodes, vérifier si c'est un gestionnaire de la boutique
        if not request.user.is_authenticated:
            return False
        try:
            if hasattr(obj, 'boutique'):
                return request.user in obj.boutique.gestionnaires.all()
            return request.user in obj.gestionnaires.all()
        except:
            return False

class PeutModifierProduit(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            role = request.user.userrole.role
            return role in ['RESPONSABLE', 'GESTIONNAIRE']
        except:
            return False

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        try:
            role = request.user.userrole.role
            if role == 'RESPONSABLE':
                return obj.boutique.responsable == request.user
            elif role == 'GESTIONNAIRE':
                return request.user in obj.boutique.gestionnaires.all()
            return False
        except:
            return False

class EstGestionnaireOuResponsable(permissions.BasePermission):
    def has_permission(self, request, view):
        # Permettre l'accès en lecture à tout le monde
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
            
        # Vérifier l'authentification et les rôles pour les autres méthodes
        if not request.user.is_authenticated:
            return False
            
        if request.user.is_superuser:
            return True
            
        if hasattr(request.user, 'profile'):
            return request.user.profile.role in ['RESPONSABLE', 'GESTIONNAIRE']
            
        return False

    def has_object_permission(self, request, view, obj):
        # Permettre GET à tout le monde
        if request.method in permissions.SAFE_METHODS:
            return True
            
        if not request.user.is_authenticated:
            return False
            
        # Le superuser peut tout faire
        if request.user.is_superuser:
            return True
            
        # Vérifier si c'est un gestionnaire
        try:
            return request.user.profile.role == 'GESTIONNAIRE'
        except:
            return False