from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum
from django.utils.safestring import mark_safe
from .models import Marque, Modele, Produit, Boutique, Stock, GestionnaireStock

# Gestionnaire Stock Admin
@admin.register(GestionnaireStock)
class GestionnaireStockAdmin(admin.ModelAdmin):
    list_display = ('username', 'nom_complet', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('username', 'nom_utilisateur', 'prenom')
    ordering = ('nom_utilisateur',)
    list_per_page = 20
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Informations personnelles'), {'fields': ('prenom', 'nom_utilisateur', 'date_naissance')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    
    def nom_complet(self, obj):
        return f"{obj.prenom} {obj.nom_utilisateur}"
    nom_complet.short_description = _('Nom complet')

# Boutique Admin
@admin.register(Boutique)
class BoutiqueAdmin(admin.ModelAdmin):
    list_display = ('nom', 'ville_departement', 'gestionnaire', 'contact')
    list_filter = ('departement', 'ville')
    search_fields = ('nom', 'ville', 'departement', 'gestionnaire_stock__username')
    raw_id_fields = ('gestionnaire_stock',)
    list_per_page = 20
    
    fieldsets = (
        (None, {'fields': ('nom', 'gestionnaire_stock')}),
        (_('Localisation'), {'fields': ('adresse', 'code_postal', 'ville', 'departement', 'longitude', 'latitude')}),
        (_('Contact'), {'fields': ('num_telephone', 'email')}),
    )
    
    def ville_departement(self, obj):
        return f"{obj.ville} ({obj.departement})"
    ville_departement.short_description = _('Localisation')
    
    def gestionnaire(self, obj):
        return obj.gestionnaire_stock.username
    gestionnaire.short_description = _('Gestionnaire')
    
    def contact(self, obj):
        return f"{obj.num_telephone} | {obj.email}"
    contact.short_description = _('Contact')

# Marque Admin
@admin.register(Marque)
class MarqueAdmin(admin.ModelAdmin):
    list_display = ('marque', 'nb_modeles')
    search_fields = ('marque',)
    ordering = ('marque',)
    list_per_page = 20
    
    def nb_modeles(self, obj):
        return obj.modele_set.count()
    nb_modeles.short_description = _('Nombre de modèles')

# Modele Admin
@admin.register(Modele)
class ModeleAdmin(admin.ModelAdmin):
    list_display = ('modele', 'marque', 'nb_produits')
    list_filter = ('marque',)
    search_fields = ('modele', 'marque__marque')
    raw_id_fields = ('marque',)
    list_per_page = 20
    
    def nb_produits(self, obj):
        return obj.produit_set.count()
    nb_produits.short_description = _('Nombre de produits')

# Produit Admin
@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'modele_marque', 'prix', 'couleur', 'capacite', 'disponibilite')
    list_filter = ('modele__marque', 'couleur')
    search_fields = ('nom', 'modele__modele')
    raw_id_fields = ('modele',)
    list_per_page = 20
    readonly_fields = ('image_preview',)
    
    fieldsets = (
        (None, {'fields': ('nom', 'modele')}),
        (_('Caractéristiques'), {'fields': ('prix', 'couleur', 'capacite', 'image')}),
        (_('Prévisualisation'), {'fields': ('image_preview',)}),
    )
    
    def modele_marque(self, obj):
        return f"{obj.modele.modele} ({obj.modele.marque})"
    modele_marque.short_description = _('Modèle')
    
    def disponibilite(self, obj):
        total = obj.stock_set.aggregate(total=Sum('quantite'))['total']
        return total if total is not None else 0
    disponibilite.short_description = _('Disponibilité')
    
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150" />')
        return _("Aucune image")
    image_preview.short_description = _('Aperçu')

# Stock Admin
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('produit_info', 'boutique_info', 'quantite')
    list_filter = ('boutique', 'produit__modele__marque')
    search_fields = ('produit__nom', 'boutique__nom')
    raw_id_fields = ('produit', 'boutique')
    list_editable = ('quantite',)
    list_per_page = 20
    
    def produit_info(self, obj):
        return f"{obj.produit.nom} ({obj.produit.modele.marque})"
    produit_info.short_description = _('Produit')
    
    def boutique_info(self, obj):
        return f"{obj.boutique.nom} - {obj.boutique.ville}"
    boutique_info.short_description = _('Boutique')