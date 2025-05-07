from rest_framework import generics, permissions, viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import  UserProfile, ArchivedUser
from .serializers import  UserSerializer, UserProfileSerializer, ArchivedUserSerializer
from django.contrib.auth.models import User
from boutique.permissions import EstResponsableBoutique




class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [EstResponsableBoutique]

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
