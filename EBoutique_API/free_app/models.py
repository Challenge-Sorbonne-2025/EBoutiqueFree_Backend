from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('RESPONSABLE', 'Responsable de la boutique'),
        ('GESTIONNAIRE', 'Gestionnaire de laboutique'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    telephone = models.CharField(max_length=20, blank=True, null=True, unique=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_maj = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    

class ArchivedUser(models.Model):
    original_id = models.IntegerField()
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    date_archivage = models.DateTimeField(auto_now_add=True)
    archive_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='users_archives')
    raison = models.TextField()

    def __str__(self):
        return f"Archive: {self.username} (ID original: {self.original_id})"
