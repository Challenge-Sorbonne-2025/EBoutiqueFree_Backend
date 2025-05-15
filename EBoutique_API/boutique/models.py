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
    marque_id = models.AutoField(primary_key=True)  # Identifiant unique de la marque
    marque = models.CharField(max_length=100, unique=True)  # Nom unique de la marque

    class Meta:
        db_table = 'tb_marque'  # Nom personnalisé de la table

    def __str__(self):
        return self.marque

class Modele(models.Model):
    """
    Modèle représentant un modèle de téléphone spécifique.
    Chaque modèle est associé à une marque.
    """
    modele_id = models.AutoField(primary_key=True)  # Identifiant unique du modèle
    modele = models.CharField(max_length=100)  # Nom du modèle
    marque = models.ForeignKey(Marque, on_delete=models.CASCADE)  # Relation avec la marque

    class Meta:
        db_table = 'tb_modele'  # Nom personnalisé de la table

    def __str__(self):
        return f"{self.marque} - {self.modele}"

# ============================================================================
# Modèles principaux de l'application
# ============================================================================

class Boutique(models.Model):
    """
    Modèle représentant une boutique physique.
    Gère les informations de localisation, contact et personnel.
    """
    boutique_id = models.AutoField(primary_key=True)  # Identifiant unique de la boutique
    nom_boutique = models.CharField(max_length=100)  # Nom de la boutique
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

    class Meta:
        db_table = 'tb_boutique'  # Nom personnalisé de la table

    def __str__(self):
        return f"{self.nom_boutique} - {self.ville} ({self.code_postal})"

class Produit(models.Model):
    """
    Modèle représentant un produit (téléphone) en vente.
    Stocke les caractéristiques techniques et l'utilisateur qui l'a ajouté.
    """
    produit_id = models.AutoField(primary_key=True)  # Identifiant unique du produit
    nom_produit = models.CharField(max_length=100)  # Nom du produit
    modele = models.ForeignKey(Modele, on_delete=models.CASCADE, related_name='produits')  # Modèle associé
    prix = models.DecimalField(max_digits=10, decimal_places=2)  # Prix de vente
    couleur = models.CharField(max_length=50)  # Couleur du produit
    capacite = models.DecimalField(max_digits=10, decimal_places=2)  # Capacité de stockage
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='produits')  # Utilisateur ayant ajouté le produit
    ram = models.DecimalField(max_digits=10, decimal_places=2)  # Quantité de RAM
    image = models.ImageField(upload_to='produits/', null=True, blank=True)  # Image du produit (optionnelle)
    validation_responsable = models.BooleanField(default=False)  # Validation du responsable de la boutique

    class Meta:
        db_table = 'tb_produit'  # Nom personnalisé de la table

    def __str__(self):
        return f"{self.nom_produit} ({self.modele})"

class Stock(models.Model):
    """
    Modèle de gestion des stocks.
    Gère la quantité de produits disponibles dans chaque boutique.
    """
    stock_id = models.AutoField(primary_key=True)  # Identifiant unique du stock
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

# ============================================================================
# Modèles d'archivage pour la traçabilité et l'historique des ventes
# ============================================================================

class HistoriqueVentes(models.Model):
    """
    Modèle pour archiver les produits supprimés.
    Conserve l'historique des produits avec leurs caractéristiques au moment de l'archivage.
    """
    original_id = models.IntegerField()  # ID du produit original avant archivage
    nom_produit = models.CharField(max_length=100)  # Nom du produit
    marque = models.CharField(max_length=50)  # Nom de la marque (stocké en texte)
    modele = models.CharField(max_length=50)  # Nom du modèle (stocké en texte)
    prix = models.DecimalField(max_digits=10, decimal_places=2)  # Prix au moment de l'archivage
    couleur = models.CharField(max_length=50)  # Couleur du produit
    capacite = models.DecimalField(max_digits=10, decimal_places=2)  # Capacité de stockage
    ram = models.DecimalField(max_digits=10, decimal_places=2)  # Quantité de RAM
    date_vente = models.DateTimeField(auto_now_add=True)  # Date automatique d'archivage
    quantite_vendue = models.IntegerField(validators=[MinValueValidator(0)], default=0)  # Quantité vendue
    vendu_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='historique_produits')  # Utilisateur ayant archivé
    description = models.TextField()  # ajouter un texte 

    class Meta:
        db_table = 'tb_historique_ventes'  # Nom personnalisé de la table

    def __str__(self):
        return f"Archive: {self.nom_produit} (ID original: {self.original_id})"

class ArchivedBoutique(models.Model):
    """
    Modèle pour archiver les boutiques supprimées.
    Conserve l'historique des boutiques avec leurs informations au moment de l'archivage.
    """
    original_id = models.IntegerField()  # ID de la boutique originale
    nom_boutique = models.CharField(max_length=100)  # Nom de la boutique
    adresse = models.TextField()  # Adresse complète
    ville = models.CharField(max_length=50)  # Ville
    code_postal = models.CharField(max_length=10)  # Code postal
    departement = models.CharField(max_length=50, blank=True, null=True)  # Département (optionnel)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)  # Coordonnée GPS
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)  # Coordonnée GPS
    date_archivage = models.DateTimeField(auto_now_add=True)  # Date automatique d'archivage
    archive_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='archived_boutiques')  # Utilisateur ayant archivé
    raison = models.TextField()  # Motif de l'archivage

    class Meta:
        db_table = 'tb_archive_boutique'  # Nom personnalisé de la table

    def __str__(self):
        return f"Archive: {self.nom} (ID original: {self.original_id})"

class ArchivedProduit(models.Model):
    """
    Modèle pour archiver les produits supprimés.
    Conserve l'historique des produits avec leurs caractéristiques au moment de l'archivage.
    """
    original_id = models.IntegerField()  # ID du produit original avant archivage
    nom_produit = models.CharField(max_length=100)  # Nom du produit
    marque = models.CharField(max_length=50)  # Nom de la marque (stocké en texte)
    modele = models.CharField(max_length=50)  # Nom du modèle (stocké en texte)
    prix = models.DecimalField(max_digits=10, decimal_places=2)  # Prix au moment de l'archivage
    couleur = models.CharField(max_length=50)  # Couleur du produit
    capacite = models.DecimalField(max_digits=10, decimal_places=2)  # Capacité de stockage
    ram = models.DecimalField(max_digits=10, decimal_places=2)  # Quantité de RAM
    date_archivage = models.DateTimeField(auto_now_add=True)  # Date automatique d'archivage
    archive_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='archived_produits')  # Utilisateur ayant archivé
    raison = models.TextField()  # Motif de l'archivage

    class Meta:
        db_table = 'tb_archive_produit'  # Nom personnalisé de la table

    def __str__(self):
        return f"Archive: {self.nom_produit} (ID original: {self.original_id})"

# ============================================================================
# Modèles pour la gestion des demandes de suppression de produits
# ============================================================================

class DemandeSuppressionProduit(models.Model):
    """
    Modèle pour gérer les demandes de suppression de produits.
    Permet au responsable de valider ou annuler les demandes de suppression.
    """
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='demandes_suppression')
    demandeur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='demandes_suppression_faites')
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='demandes_suppression_a_valider')
    date_demande = models.DateTimeField(auto_now_add=True)
    date_validation = models.DateTimeField(null=True, blank=True)
    statut = models.CharField(
        max_length=20,
        choices=[
            ('EN_ATTENTE', 'En attente de validation'),
            ('VALIDE', 'Validé'),
            ('ANNULE', 'Annulé')
        ],
        default='EN_ATTENTE'
    )
    raison = models.TextField(blank=True)
    commentaire_responsable = models.TextField(blank=True)

    class Meta:
        db_table = 'tb_demande_suppression_produit'
        ordering = ['-date_demande']

    def __str__(self):
        return f"Demande de suppression de {self.produit} par {self.demandeur}"