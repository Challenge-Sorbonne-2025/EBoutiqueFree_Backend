from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from boutique.models import Boutique, Produit, Stock, Marque, Modele
#from .models import UserProfile, ArchivedUser

# --- Boutique ---
@admin.register(Boutique)
class BoutiqueAdmin(admin.ModelAdmin):
    list_display = ('nom', 'ville', 'code_postal', 'responsable_link', 'nombre_produits')
    list_filter = ('ville',)
    search_fields = ('nom', 'ville', 'code_postal')
    raw_id_fields = ('responsable',)

    def responsable_link(self, obj):
        if obj.responsable:
            return format_html(
                '<a href="/admin/auth/user/{}/change/">{}</a>',
                obj.responsable.id,
                obj.responsable.get_full_name() or obj.responsable.username
            )
        return "-"
    responsable_link.short_description = "Responsable"

    def nombre_produits(self, obj):
        return obj.stocks.count()
    nombre_produits.short_description = "Produits en stock"

# --- Produit ---
@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'marque', 'modele', 'prix', 'image_preview')
    list_filter = ('marque', 'modele')
    search_fields = ('nom', 'marque__nom', 'modele__nom')

    def image_preview(self, obj):
        if obj.image and obj.image.url:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 50px;"/>')
        return "-"
    image_preview.short_description = "Image"

# --- Stock ---
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('produit', 'boutique', 'quantite', 'seuil_alerte', 'statut_stock')
    list_filter = ('boutique', 'produit__marque')
    list_editable = ('quantite', 'seuil_alerte')
    search_fields = ('produit__nom', 'boutique__nom')
    raw_id_fields = ('produit', 'boutique')

    def statut_stock(self, obj):
        if obj.quantite == 0:
            return format_html('<span style="color: red; font-weight: bold;">RUPTURE</span>')
        elif obj.quantite < obj.seuil_alerte:
            return format_html('<span style="color: orange; font-weight: bold;">FAIBLE</span>')
        return format_html('<span style="color: green;">OK</span>')
    statut_stock.short_description = "Statut"

# --- Marque ---
@admin.register(Marque)
class MarqueAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)

# --- Modele ---
@admin.register(Modele)
class ModeleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'marque')
    search_fields = ('nom', 'marque__nom')
    list_filter = ('marque',)