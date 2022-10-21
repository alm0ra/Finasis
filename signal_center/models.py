from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class NewSignal(models.Model):

    author_name = models.CharField(max_length=30, verbose_name='ثبت کننده سیگنال')

    symbol = models.CharField(max_length=30, verbose_name='جفت ارز')

    entry_point = models.DecimalField(decimal_places=10, max_digits=10, blank=False,
                                      verbose_name='نقطه ورود')

    stop_loss = models.DecimalField(decimal_places=10, max_digits=10, blank=False,
                                    verbose_name='حد ضرر')
    tp1 = models.DecimalField(decimal_places=10, max_digits=10, blank=False,
                              verbose_name='حد سود ۱')
    tp2 = models.DecimalField(decimal_places=10, max_digits=10, blank=False,
                              verbose_name='حد سود ۲')
    tp3 = models.DecimalField(decimal_places=10, max_digits=10, blank=False,
                              verbose_name='حد سود ۳')
    tp4 = models.DecimalField(decimal_places=10, max_digits=10, blank=False,
                              verbose_name='حد سود ۴')
    tp5 = models.DecimalField(decimal_places=10, max_digits=10, blank=False,
                              verbose_name='حد سود ۵')

    created_at = models.DateTimeField(default=timezone.now, verbose_name=_('تاریخ ثبت'))

    class Meta:
        verbose_name = _('سیگنال')
        verbose_name_plural = _('سیگنال ها')

    def __str__(self):
        return self.symbol
