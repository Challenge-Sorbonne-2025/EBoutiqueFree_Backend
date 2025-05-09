from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Stock
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Stock)
def alerte_stock(sender, instance, created, **kwargs):
    """Envoie une alerte email lorsque le stock est faible"""
    if created:
        return  # Ne pas alerter à la création du stock
    
    # Vérifie si le stock est inférieur au seuil d'alerte
    if instance.quantite < settings.STOCK_ALERT_THRESHOLD:
        boutique = instance.boutique
        gestionnaire = boutique.gestionnaire

        # Vérifie si le gestionnaire a une adresse email
        if not gestionnaire or not gestionnaire.email:
            return

        # Crée l'email d'alerte
        sujet = f"Alerte stock - {instance.produit.nom} ({boutique.nom})"
        message = (
            f"Bonjour {gestionnaire.first_name or 'gestionnaire'},\n\n"
            f"Le produit {instance.produit.nom} dans votre boutique {boutique.nom} "
            f"a un stock faible :\n\n"
            f"- Quantité actuelle : {instance.quantite}\n"
            f"- Seuil d'alerte : {settings.STOCK_ALERT_THRESHOLD}\n\n"
            f"Veuillez procéder au réapprovisionnement.\n\n"
            f"Cordialement,\nVotre système de gestion de stock"
        )

        # Envoi de l'email
        send_mail(
            subject=sujet,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[gestionnaire.email],
            fail_silently=False,
        )

        logger.info(f"Alerte stock envoyée pour le produit {instance.produit.nom} à {gestionnaire.email}")

@receiver(pre_save, sender=Stock)
def tracer_changement_stock(sender, instance, **kwargs):
    """Crée un historique des modifications de stock, sans HistoriqueStock"""
    if not instance.pk:
        return

    try:
        ancien_stock = Stock.objects.get(pk=instance.pk)
    except Stock.DoesNotExist:
        return

    if ancien_stock.quantite != instance.quantite:
        difference = instance.quantite - ancien_stock.quantite
        type_mouvement = 'ENTREE' if difference > 0 else 'SORTIE'

        # Tu peux loguer le changement ici ou effectuer d'autres actions,
        # mais pas de création d'objet HistoriqueStock.
        logger.info(f"Changement de stock pour {instance.produit.nom}: "
                    f"{ancien_stock.quantite} -> {instance.quantite} ({type_mouvement})")

@receiver(post_save, sender=Stock)
def notifier_api_frontend(sender, instance, created, **kwargs):
    """
    Pour une future intégration avec React (webhooks ou SSE)
    """
    logger.info(f"[Notifier Frontend] Stock mis à jour : {instance.produit.nom} ({instance.quantite})")

# ============================================================================