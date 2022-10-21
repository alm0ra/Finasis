from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from signal_center.models import NewSignal


@receiver(post_save, sender=NewSignal)
def new_signal_event(sender, instance, created, *args, **kwargs):
    if created:
        pass
        # check if symbol exist in exchange
        # register signal in signal center
        # send notification to telegram


@receiver(post_delete, sender=NewSignal)
def remove_new_signal(sender, instance, created, *args, **kwargs):
    # delete registered signal in signal center
    # send notification to telegram
    pass
