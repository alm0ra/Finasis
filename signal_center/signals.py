from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from signal_center.models import NewSignal
from signal_center.services.operations import check_conditions, TelegramManager, MessageTemplator


@receiver(post_save, sender=NewSignal)
def new_signal_event(sender, instance, created, *args, **kwargs):
    if created:
        check_conditions(instance=instance)
        TelegramManager.send(message=MessageTemplator.get_new_signal_message(instance=instance))

        # register signal in signal center


@receiver(pre_save, sender=NewSignal)
def modify_signal_event(sender, instance, created, *args, **kwargs):
    if created:
        check_conditions(instance=instance)
        TelegramManager.send(message=MessageTemplator.get_modify_signal_message(instance=instance))


@receiver(post_delete, sender=NewSignal)
def remove_new_signal(sender, instance, created, *args, **kwargs):
    if instance.remove_signal_strategy == NewSignal.CLOSE_2:
        pass
    elif instance.remove_signal_strategy == NewSignal.CLOSE_1:
        # close this position and cancel all order or stop orders
        pass

    TelegramManager.send(message=MessageTemplator.get_remove_signal_notif_message(instance=instance))