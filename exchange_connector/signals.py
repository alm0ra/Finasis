from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import ExchangeAccounts
from signal_center.services.operations import TelegramManager, MessageTemplator


@receiver(post_save, sender=ExchangeAccounts)
def new_signal_event(sender, instance, created, *args, **kwargs):
    if created:
        TelegramManager.send(message=MessageTemplator.new_account_message(instance=instance))
