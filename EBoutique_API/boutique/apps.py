from django.apps import AppConfig

class BoutiqueConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.boutique'
    verbose_name = "Gestion des boutiques Free"
    def ready(self):
        import apps.boutique.signals  # Active les signaux à l'initialisation
