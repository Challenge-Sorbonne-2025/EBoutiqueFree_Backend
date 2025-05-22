from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from boutique.models import Boutique, Produit, Stock, Marque, Modele

# --- Boutique ---
@admin.register(Boutique)
class BoutiqueAdmin(admin.ModelAdmin):
    list_display = ('nom_boutique', 'ville', 'code_postal', 'responsable', 'nombre_produits')
    list_filter = ('ville',)
    search_fields = ('nom_boutique', 'ville', 'code_postal')
    raw_id_fields = ('responsable',)

    def responsable(self, obj):
        if obj.responsable:
            return format_html(
                '<a href="/admin/auth/user/{}/change/">{}</a>',
                obj.responsable.id,
                obj.responsable.get_full_name() or obj.responsable.username
            )
        return "-"
    responsable.short_description = "Responsable"

    def nombre_produits(self, obj):
        return obj.stocks.count()
    nombre_produits.short_description = "Produits en stock"

# --- Produit ---
@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom_produit', 'modele', 'prix', 'image')
    list_filter = ('modele', 'modele__marque')
    search_fields = ('nom_produit', 'modele__modele', 'modele__modele__marque')

    def image_preview(self, obj):
        if obj.image and obj.image.url:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 50px;"/>')
        return "-"
    image_preview.short_description = "Image"

# --- Stock ---
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('produit', 'boutique', 'quantite', 'seuil_alerte')
    list_filter = ('boutique', 'produit__modele__marque')
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
    list_display = ('marque',)
    search_fields = ('marque',)

# --- Modele ---
@admin.register(Modele)
class ModeleAdmin(admin.ModelAdmin):
    list_display = ('modele', 'marque')
    search_fields = ('modele', 'marque__marque')
    list_filter = ('modele',)