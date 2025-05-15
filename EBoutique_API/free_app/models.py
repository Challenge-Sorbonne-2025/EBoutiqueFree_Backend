from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
# La ligne suivante est ajoutée uniquement pour PointField
#(utilisation de la GeoDjango)
from django.contrib.gis.db import models as gis_models
User = get_user_model()

# Modèle pour la table Marque
class Marque(models.Model):
    nom = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nom

# Modèle pour la table Modele
class Modele(models.Model):
    nom = models.CharField(max_length=50)
    marque = models.ForeignKey(Marque, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.marque} - {self.nom}"

# Modèle pour la table Boutique
class Boutique(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.TextField()
    ville = models.CharField(max_length=50)
    code_postal = models.CharField(max_length=5)  # Pour garder les zéros initiaux
    departement = models.CharField(max_length=50, blank=True, null=True)
    #location = (longitude, latitude) 
    location = gis_models.PointField(geography=True, blank=True, null=True)
    num_telephone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='boutiques_free_app')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_maj = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nom} - {self.ville} ({self.code_postal})"

# Modèle pour la table Produit
class Produit(models.Model):
    nom = models.CharField(max_length=100)
    marque = models.ForeignKey(Marque, on_delete=models.CASCADE)  # Changé en ForeignKey
    modele = models.ForeignKey(Modele, on_delete=models.CASCADE)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    couleur = models.CharField(max_length=50)
    capacite = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='produits/', null=True, blank=True)

    def __str__(self):
        return f"{self.nom} ({self.marque})" 

# Modèle pour la table Stock
class Stock(models.Model):
    boutique = models.ForeignKey(Boutique, on_delete=models.CASCADE, related_name='stocks')
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='stocks')
    quantite = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    seuil_alerte = models.PositiveIntegerField(default=5)

    class Meta:
        unique_together = ('boutique', 'produit')

    def __str__(self):
        return f"{self.produit} @ {self.boutique} - {self.quantite} en stock"
