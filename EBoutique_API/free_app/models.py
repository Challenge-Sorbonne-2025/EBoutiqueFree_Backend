from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class GestionnaireStockManager(BaseUserManager):
    def create_user(self, username, mot_passe=None, **extra_fields):
        if not username:
            raise ValueError("Le username est requis")
        user = self.model(username=username, **extra_fields)
        user.set_password(mot_passe)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, mot_passe=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, mot_passe, **extra_fields)

class GestionnaireStock(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    mot_passe = models.CharField(max_length=128)
    nom_utilisateur = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    date_naissance = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = GestionnaireStockManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nom_utilisateur', 'prenom']

    def __str__(self):
        return f"{self.prenom} {self.nom_utilisateur}"

class Marque(models.Model):
    marque = models.CharField(max_length=255)

    def __str__(self):
        return self.marque

class Modele(models.Model):
    marque = models.ForeignKey(Marque, on_delete=models.CASCADE)
    modele = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.marque} - {self.modele}"

class Produit(models.Model):
    nom = models.CharField(max_length=255)
    modele = models.ForeignKey(Modele, on_delete=models.CASCADE)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    couleur = models.CharField(max_length=50)
    capacite = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.nom

class Boutique(models.Model):
    nom = models.CharField(max_length=255)
    gestionnaire_stock = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code_postal = models.IntegerField()
    adresse = models.CharField(max_length=255)
    ville = models.CharField(max_length=100)
    departement = models.CharField(max_length=100)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    num_telephone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.nom

class Stock(models.Model):
    boutique = models.ForeignKey(Boutique, related_name="stocks", on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, related_name="stocks", on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()

    class Meta:
        unique_together = ('boutique', 'produit')

    def __str__(self):
        return f"{self.produit.nom} - {self.boutique.nom} ({self.quantite})"



