from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# ============================================================================
# Modèles de base pour la gestion des produits
# ============================================================================

class Marque(models.Model):
    """
    Modèle représentant une marque de téléphone.
    Une marque peut avoir plusieurs modèles associés.
    """
    nom = models.CharField(max_length=100, unique=True)  # Nom unique de la marque

    def __str__(self):
        return self.nom

class Modele(models.Model):
    """
    Modèle représentant un modèle de téléphone spécifique.
    Chaque modèle est associé à une marque.
    """
    nom = models.CharField(max_length=100)  # Nom du modèle
    marque = models.ForeignKey(Marque, on_delete=models.CASCADE)  # Relation avec la marque

    def __str__(self):
        return f"{self.marque} - {self.nom}"

# ============================================================================
# Modèles d'archivage pour la traçabilité
# ============================================================================

class ArchivedProduit(models.Model):
    """
    Modèle pour archiver les produits supprimés.
    Conserve l'historique des produits avec leurs caractéristiques au moment de l'archivage.
    """
    original_id = models.IntegerField()  # ID du produit original avant archivage
    nom = models.CharField(max_length=100)  # Nom du produit
    marque = models.CharField(max_length=50)  # Nom de la marque (stocké en texte)
    modele = models.CharField(max_length=50)  # Nom du modèle (stocké en texte)
    prix = models.DecimalField(max_digits=10, decimal_places=2)  # Prix au moment de l'archivage
    couleur = models.CharField(max_length=50)  # Couleur du produit
    capacite = models.DecimalField(max_digits=10, decimal_places=2)  # Capacité de stockage
    ram = models.DecimalField(max_digits=10, decimal_places=2)  # Quantité de RAM
    date_archivage = models.DateTimeField(auto_now_add=True)  # Date automatique d'archivage
    archive_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='archived_produits')  # Utilisateur ayant archivé
    raison = models.TextField()  # Motif de l'archivage

    def __str__(self):
        return f"Archive: {self.nom} (ID original: {self.original_id})"

class ArchivedBoutique(models.Model):
    """
    Modèle pour archiver les boutiques supprimées.
    Conserve l'historique des boutiques avec leurs informations au moment de l'archivage.
    """
    original_id = models.IntegerField()  # ID de la boutique originale
    nom = models.CharField(max_length=100)  # Nom de la boutique
    adresse = models.TextField()  # Adresse complète
    ville = models.CharField(max_length=50)  # Ville
    code_postal = models.CharField(max_length=5)  # Code postal
    departement = models.CharField(max_length=50, blank=True, null=True)  # Département (optionnel)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)  # Coordonnée GPS
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)  # Coordonnée GPS
    date_archivage = models.DateTimeField(auto_now_add=True)  # Date automatique d'archivage
    archive_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='archived_boutiques')  # Utilisateur ayant archivé
    raison = models.TextField()  # Motif de l'archivage

    def __str__(self):
        return f"Archive: {self.nom} (ID original: {self.original_id})"

# ============================================================================
# Modèles principaux de l'application
# ============================================================================

class Boutique(models.Model):
    """
    Modèle représentant une boutique physique.
    Gère les informations de localisation, contact et personnel.
    """
    nom = models.CharField(max_length=100)  # Nom de la boutique
    adresse = models.TextField()  # Adresse complète
    ville = models.CharField(max_length=50)  # Ville
    code_postal = models.CharField(max_length=10)  # Code postal (avec zéros initiaux)
    departement = models.CharField(max_length=50, blank=True, null=False)  # Département
    longitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=False)  # Coordonnée GPS
    latitude = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=False)  # Coordonnée GPS
    num_telephone = models.CharField(max_length=20, blank=True, null=True, unique=True)  # Numéro de téléphone unique
    email = models.EmailField(blank=True, null=True, unique=True)  # Email unique
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='boutiques_responsable')  # Responsable principal
    gestionnaires = models.ManyToManyField(User, related_name='boutiques_gestionnaire', blank=True)  # Équipe de gestion
    date_creation = models.DateTimeField(auto_now_add=True)  # Date de création automatique
    date_maj = models.DateTimeField(auto_now=True)  # Date de dernière modification automatique

    def __str__(self):
        return f"{self.nom} - {self.ville} ({self.code_postal})"

class Produit(models.Model):
    """
    Modèle représentant un produit (téléphone) en vente.
    Stocke les caractéristiques techniques et l'utilisateur qui l'a ajouté.
    """
    nom = models.CharField(max_length=100)  # Nom du produit
    modele = models.ForeignKey(Modele, on_delete=models.CASCADE, related_name='produits')  # Modèle associé
    prix = models.DecimalField(max_digits=10, decimal_places=2)  # Prix de vente
    couleur = models.CharField(max_length=50)  # Couleur du produit
    capacite = models.DecimalField(max_digits=10, decimal_places=2)  # Capacité de stockage
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='produits')  # Utilisateur ayant ajouté le produit
    ram = models.DecimalField(max_digits=10, decimal_places=2)  # Quantité de RAM
    image = models.ImageField(upload_to='produits/', null=True, blank=True)  # Image du produit (optionnelle)

    def __str__(self):
        return f"{self.nom} ({self.modele})"

class Stock(models.Model):
    """
    Modèle de gestion des stocks.
    Gère la quantité de produits disponibles dans chaque boutique.
    """
    boutique = models.ForeignKey(Boutique, on_delete=models.CASCADE, related_name='stocks')  # Boutique concernée
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='stocks')  # Produit en stock
    quantite = models.IntegerField(validators=[MinValueValidator(0)], default=0)  # Quantité disponible (minimum 0)
    seuil_alerte = models.PositiveIntegerField(default=5)  # Seuil pour alerter de stock bas

    class Meta:
        db_table = 'tb_stock'  # Nom personnalisé de la table
        constraints = [
            models.UniqueConstraint(
                fields=['boutique', 'produit'],
                name='stock_composite_key'  # Clé composite unique pour éviter les doublons
            )
        ]

    def __str__(self):
        return f"{self.produit} @ {self.boutique} - {self.quantite} en stock"