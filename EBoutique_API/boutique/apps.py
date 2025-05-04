from django.apps import AppConfig

class BoutiqueConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'boutique'  # ← Corrige ici
    verbose_name = "Gestion des boutiques Free"

    def ready(self):
        import boutique.signals  # ← Corrige ici aussi si nécessaire
