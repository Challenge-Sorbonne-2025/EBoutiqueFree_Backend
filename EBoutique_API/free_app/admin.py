from django.contrib import admin
from .models import (
    Marque,
    Modele,
    Boutique,
    Produit,
    Stock,
    UserProfile,
    ArchivedUser
)

@admin.register(Marque)
class MarqueAdmin(admin.ModelAdmin):
    list_display = ('nom',)

@admin.register(Modele)
class ModeleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'marque')
    list_filter = ('marque',)

@admin.register(Boutique)
class BoutiqueAdmin(admin.ModelAdmin):
    list_display = ('nom', 'ville', 'code_postal', 'departement', 'responsable')
    search_fields = ('nom', 'ville', 'code_postal')
    list_filter = ('ville', 'departement')

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'marque', 'modele', 'prix', 'couleur', 'capacite')
    list_filter = ('marque', 'modele')
    search_fields = ('nom',)

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('produit', 'boutique', 'quantite', 'seuil_alerte')
    list_filter = ('boutique',)
    search_fields = ('produit__nom', 'boutique__nom')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'telephone', 'role', 'date_creation', 'date_archivage')
    list_filter = ('role',)
    search_fields = ('user__username',)

@admin.register(ArchivedUser)
class ArchivedUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_archivage', 'raison')
    search_fields = ('user__username',)
