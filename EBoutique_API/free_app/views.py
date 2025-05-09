from rest_framework import viewsets
from .models import UserProfile, ArchivedUser
from drf_yasg.utils import swagger_auto_schema
from .serializers import UserProfileSerializer, ArchivedUserSerializer
from boutique.permissions import EstResponsableBoutique

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [EstResponsableBoutique]

    @swagger_auto_schema(
        operation_description="Liste tous les utilisateurs",
        responses={200: UserProfileSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Récupère un utilisateur par son ID",
        responses={200: UserProfileSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Crée un nouvel utilisateur",
        request_body=UserProfileSerializer,
        responses={201: UserProfileSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Met à jour un utilisateur existant",
        request_body=UserProfileSerializer,
        responses={200: UserProfileSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    
    @swagger_auto_schema(
        operation_description="Archiver un utilisateur existant",
        responses={204: None}
    )
    def perform_destroy(self, instance):
        user = instance.user
        # Archiver l'utilisateur avant de le supprimer
        ArchivedUser.objects.create(
            original_id=user.id,
            username=user.username,
            email=user.email,
            role=instance.role,
            telephone=instance.telephone,
            archive_par=self.request.user,
            raison=self.request.data.get('raison', 'Non spécifiée')
        )
        user.delete()  # Cela supprimera aussi le profil à cause de la relation CASCADE

class ArchivedUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ArchivedUser.objects.all()
    serializer_class = ArchivedUserSerializer
    permission_classes = [EstResponsableBoutique]

    @swagger_auto_schema(
        operation_description="Liste tous les utilisateurs archivés",
        responses={200: ArchivedUserSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Récupère un utilisateur archivé par son ID",
        responses={200: ArchivedUserSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
