from django.db import models
from django.contrib.auth.models import User


# ============================================================================
# Modèle pour stocker les informations de profil des utilisateurs.
# ============================================================================
class UserProfile(models.Model):
    """
    Modèle pour stocker les informations de profil des utilisateurs.
    """
    profile_id = models.AutoField(primary_key=True) # Identifiant unique du profil    
    ROLE_CHOICES = [
        ('RESPONSABLE', 'Responsable de la boutique'),
        ('GESTIONNAIRE', 'Gestionnaire de laboutique'),]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile') # Relation avec l'utilisateur
    role = models.CharField(max_length=20, choices=ROLE_CHOICES) # Rôle de l'utilisateur
    telephone = models.CharField(max_length=20, blank=True, null=True, unique=True) # Numéro de téléphone de l'utilisateur
    date_creation = models.DateTimeField(auto_now_add=True) # Date de création de l'utilisateur
    boutiques = models.ForeignKey('boutique.Boutique', on_delete=models.SET_NULL, null=True, blank=True, related_name='gestionnaires_boutique')  # Gestionnaires Boutique
    date_maj = models.DateTimeField(auto_now=True) # Date de mise à jour de l'utilisateur   

    class Meta:
        db_table = 'tb_user_profile' # Nom personnalisé de la table pour les profils des utilisateurs

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    

# ============================================================================
# Modèle pour archiver les utilisateurs.
# ============================================================================
class ArchivedUser(models.Model):
    original_id = models.IntegerField() # ID original de l'utilisateur
    username = models.CharField(max_length=150, unique=True) # Nom d'utilisateur de l'utilisateur
    email = models.EmailField(unique=True) # Email de l'utilisateur
    first_name = models.CharField(max_length=150) # Prénom de l'utilisateur
    last_name = models.CharField(max_length=150) # Nom de l'utilisateur
    role = models.CharField(max_length=20) # Rôle de l'utilisateur
    telephone = models.CharField(max_length=20, blank=True, null=True) # Numéro de téléphone de l'utilisateur
    date_archivage = models.DateTimeField(auto_now_add=True) # Date d'archivage de l'utilisateur        
    archive_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='users_archives') # Utilisateur qui a archivé l'utilisateur
    raison = models.TextField() # Raison de l'archivage de l'utilisateur

    class Meta:
        db_table = 'tb_user_archive' # Nom personnalisé de la table pour l'historique des utilisateurs

    def __str__(self):
        return f"Archive: {self.username} (ID original: {self.original_id})"

