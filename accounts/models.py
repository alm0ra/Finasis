from django.db import models


class ExchangeAccounts(models.Model):
    OKEX = 'okex'
    EXCHANGE_CHOICES = (
        (OKEX, OKEX)
    )
    username = models.CharField(max_length=40, verbose_name="کاربر")

    exchanage_name = models.CharField(choices=EXCHANGE_CHOICES, verbose_name='صرافی مربوطه')

    api_key = models.TextField(blank=False, null=False)
    secret_key = models.TextField(blank=False, null=False)
    password = models.TextField(blank=False, null=False)

    is_active = models.BooleanField(default=True, verbose_name='آیا فعال است؟')

    description = models.TextField(blank=False, null=False, verbose_name="توضیحات")

    class Meta:
        verbose_name = _('حساب مشتریان در صرافی ها')
        verbose_name_plural = _('حساب مشتریان در صرافی ها')

    def __str__(self):
        return self.username
