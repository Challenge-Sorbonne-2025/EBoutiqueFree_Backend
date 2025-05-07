from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


# Modèle pour la table Marque
class Marque(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom

# Modèle pour la table Modele 
class Modele(models.Model):
    nom = models.CharField(max_length=100)
    marque = models.ForeignKey(Marque, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.marque} - {self.nom}"

# Tables d'archivage
class ArchivedProduit(models.Model):
    original_id = models.IntegerField()
    nom = models.CharField(max_length=100)
    marque = models.CharField(max_length=50)
    modele = models.CharField(max_length=50)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    couleur = models.CharField(max_length=50)
    capacite = models.DecimalField(max_digits=10, decimal_places=2)
    date_archivage = models.DateTimeField(auto_now_add=True)
    archive_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='archived_produits')
    raison = models.TextField()

    def __str__(self):
        return f"Archive: {self.nom} (ID original: {self.original_id})"

class ArchivedBoutique(models.Model):
    original_id = models.IntegerField()
    nom = models.CharField(max_length=100)
    adresse = models.TextField()
    ville = models.CharField(max_length=50)
    code_postal = models.CharField(max_length=5)
    departement = models.CharField(max_length=50, blank=True, null=True)
    date_archivage = models.DateTimeField(auto_now_add=True)
    archive_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='archived_boutiques')
    raison = models.TextField()

    def __str__(self):
        return f"Archive: {self.nom} (ID original: {self.original_id})"


# Modèle pour la table Boutique
class Boutique(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.TextField()
    ville = models.CharField(max_length=50)
    code_postal = models.CharField(max_length=10)  # Pour garder les zéros initiaux
    departement = models.CharField(max_length=50, blank=True, null=False)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=False)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=False)
    num_telephone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='boutiques_responsable')
    gestionnaires = models.ManyToManyField(User, related_name='boutiques_gestionnaire', blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_maj = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nom} - {self.ville} ({self.code_postal})"

# Modèle pour la table Produit
class Produit(models.Model):
    nom = models.CharField(max_length=100)
    marque = models.ForeignKey(Marque, on_delete=models.CASCADE, related_name='produits')  # Changé en ForeignKey
    modele = models.ForeignKey(Modele, on_delete=models.CASCADE, related_name='produits')
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    couleur = models.CharField(max_length=50)
    capacite = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='produits')
    ram = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='produits/', null=True, blank=True)

    def __str__(self):
        return f"{self.nom} ({self.marque}, {self.modele})"

# Modèle pour la table Stock
class Stock(models.Model):
    boutique = models.ForeignKey(Boutique, on_delete=models.CASCADE, related_name='stocks', primary_key=False)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='stocks', primary_key=False)
    quantite = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    seuil_alerte = models.PositiveIntegerField(default=5)

    class Meta:
        db_table = 'tb_stock'
        constraints = [
            models.UniqueConstraint(
                fields=['boutique', 'produit'],
                name='stock_composite_key'
            )
        ]

    def __str__(self):
        return f"{self.produit} @ {self.boutique} - {self.quantite} en stock"