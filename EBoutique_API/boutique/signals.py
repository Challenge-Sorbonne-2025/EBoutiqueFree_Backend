from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Stock

# @receiver(post_save, sender=Stock)
# def verifier_seuil_stock(sender, instance, **kwargs):
#     # Seuil d'alerte fixe à 5
#     seuil = 5

#     if instance.quantite < seuil:
#         type_alerte = 'RUPTURE' if instance.quantite == 0 else 'FAIBLE'

#         # Crée une alerte seulement si aucune alerte non lue du même type n'existe
#         AlerteStock.objects.get_or_create(
#             stock=instance,
#             type_alerte=type_alerte,
#             lue=False
#         )
