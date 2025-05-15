from django.contrib import admindocs


from django.contrib import admin
from .models import Boutique, Produit, Marque, Modele, Stock, ArchivedBoutique, ArchivedProduit

@admin.register(Marque)
class MarqueAdmin(admin.ModelAdmin):
    list_display = ('marque_id', 'marque')
    search_fields = ('marque',)
    ordering = ('marque',)

@admin.register(Modele)
class ModeleAdmin(admin.ModelAdmin):
    list_display = ('modele_id', 'modele', 'marque')
    list_filter = ('modele',)
    search_fields = ('modele', 'marque__marque')
    autocomplete_fields = ['marque']

@admin.register(Boutique)
class BoutiqueAdmin(admin.ModelAdmin):
    list_display = ('boutique_id', 'nom_boutique', 'ville', 'code_postal', 'responsable', 'date_creation')
    list_filter = ('ville', 'departement')
    search_fields = ('nom_boutique', 'ville', 'code_postal', 'responsable__username')
    readonly_fields = ('date_creation', 'date_maj')
    filter_horizontal = ('gestionnaires',)
    fieldsets = (
        ('Informations principales', {
            'fields': ('nom_boutique', 'responsable', 'gestionnaires')
        }),
        ('Localisation', {
            'fields': ('adresse', 'ville', 'code_postal', 'departement', 'longitude', 'latitude')
        }),
        ('Contact', {
            'fields': ('num_telephone', 'email')
        }),
        ('Dates', {
            'fields': ('date_creation', 'date_maj'),
            'classes': ('collapse',)
        })
    )

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('produit_id', 'nom_produit', 'modele', 'prix', 'couleur', 'capacite', 'ram')
    list_filter = ('modele', 'couleur')
    search_fields = ('nom_produit', 'modele__modele', 'modele__marque__marque')
    autocomplete_fields = ['modele']
    readonly_fields = ('user',)
    fieldsets = (
        ('Informations principales', {
            'fields': ('nom_produit', 'modele', 'prix')
        }),
        ('Caractéristiques', {
            'fields': ('couleur', 'capacite', 'ram')
        }),
        ('Image', {
            'fields': ('image',)
        }),
        ('Métadonnées', {
            'fields': ('user',),
            'classes': ('collapse',)
        })
    )

class StockInline(admin.TabularInline):
    model = Stock
    extra = 1
    min_num = 0
    autocomplete_fields = ['produit']

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('stock_id', 'boutique', 'produit', 'quantite', 'seuil_alerte')
    list_filter = ('boutique', 'produit__modele__marque')
    search_fields = ('boutique__nom_boutique', 'produit__nom_produit')
    autocomplete_fields = ['boutique', 'produit']
    list_editable = ('quantite', 'seuil_alerte')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'profile'):
            if request.user.profile.role == 'GESTIONNAIRE':
                return qs.filter(boutique__gestionnaires=request.user)
        return qs.none()

@admin.register(ArchivedProduit)
class ArchivedProduitAdmin(admin.ModelAdmin):
    list_display = ('nom_produit',  'modele', 'prix', 'date_archivage', 'archive_par')
    list_filter = ('date_archivage', 'modele')
    search_fields = ('nom_produit', 'modele__modele', 'modele__marque__marque')
    readonly_fields = ('date_archivage', 'archive_par')

@admin.register(ArchivedBoutique)
class ArchivedBoutiqueAdmin(admin.ModelAdmin):
    list_display = ('nom_boutique', 'ville', 'code_postal', 'date_archivage', 'archive_par')
    list_filter = ('date_archivage', 'ville')
    search_fields = ('nom_boutique', 'ville', 'code_postal')
    readonly_fields = ('date_archivage', 'archive_par')