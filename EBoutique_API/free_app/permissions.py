from rest_framework import permissions
class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Autorise tout le monde à lire (GET, HEAD, OPTIONS),
    mais seules les personnes avec is_staff=True peuvent modifier (POST, PUT, DELETE).
    """
    def has_permission(self, request, view):
        # Tout le monde peut lire
        if request.method in permissions.SAFE_METHODS:
            return True
        # Seuls les admins peuvent écrire
        return request.user and request.user.is_staff


class IsBoutiqueManager(permissions.BasePermission):
    """
    Permission pour qu’un gestionnaire accède uniquement à ses propres boutiques.
    Les superusers ont tous les droits.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_staff:
            return True

        # obj peut être une boutique ou autre liée à une boutique
        if hasattr(obj, 'gestionnaire_stock'):
            return obj.gestionnaire_stock == request.user

        if hasattr(obj, 'boutique'):
            return obj.boutique.gestionnaire_stock == request.user

        return False


class IsStockManager(permissions.BasePermission):
    """
    Permission pour gérer les stocks :
    - Lecture autorisée à tous les utilisateurs authentifiés.
    - Écriture (ajout/modif/suppression) autorisée uniquement au gestionnaire de la boutique.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_staff:
            return True

        # obj est une instance de Stock
        return obj.boutique.gestionnaire_stock == request.user
