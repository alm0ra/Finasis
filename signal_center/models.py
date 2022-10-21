from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class NewSignal(models.Model):
    WAITING = 'waiting'
    OPEN = 'open'
    SL = 'sl_triggered'
    TP_1 = 'tp1_triggered'
    TP_2 = 'tp2_triggered'
    TP_3 = 'tp3_triggered'
    TP_4 = 'tp4_triggered'
    TP_5 = 'tp5_triggered'
    Done = 'Done'
    STATUS_CHOICES = (
        (WAITING, WAITING),
        (OPEN, OPEN),
        (SL, SL),
        (TP_1, TP_1),
        (TP_2, TP_2),
        (TP_3, TP_3),
        (TP_4, TP_4),
        (TP_5, TP_5),
        (Done, Done),
    )
    ETH = 'ETH/USDT'
    BTC = 'BTC/USDT'
    XRP = 'XRP/USDT'
    DYDX = 'DYDX/USDT'
    LTC = 'LTC/USDT'
    APT = 'APT/USDT'
    AAVE = 'AAVE/USDT'
    AVAX = 'AVAX/USDT'
    COMP = 'COMP/USDT'
    SUSHI = 'SUSHI/USDT'
    MATIC = 'MATIC/USDT'
    TRX = 'TRX/USDT'
    RSR = 'RSR/USDT'

    SYMBOL_CHOICES  = (
        (ETH, ETH),
        (BTC, BTC),
        (XRP, XRP),
        (DYDX, DYDX),
        (LTC, LTC),
        (APT, APT),
        (AAVE, AAVE),
        (AVAX, AVAX),
        (COMP, COMP),
        (SUSHI, SUSHI),
        (MATIC, MATIC),
        (TRX, TRX),
        (RSR, RSR),
    )
    LONG = 'LONG'
    SHORT = 'SHORT'
    SIDE_CHOICES = (
        (LONG, LONG),
        (SHORT, SHORT)
    )
    CLOSE_1 = "close_all"
    CLOSE_2 = "nothing"
    CLOSE_CHOICE = (
        (CLOSE_1, 'همه چیز را ببند و کنسل کن'),
        (CLOSE_2, 'کاری نکن'),
    )
    author_name = models.CharField(max_length=30, verbose_name='ثبت کننده سیگنال')

    symbol = models.CharField(choices=SYMBOL_CHOICES, max_length=30, verbose_name='جفت ارز')

    side = models.CharField(choices=SIDE_CHOICES, max_length=10, verbose_name='انتخاب جهت معامله', default=LONG)
    entry_point = models.DecimalField(decimal_places=20, max_digits=30, blank=False,
                                      verbose_name='نقطه ورود')

    is_market = models.BooleanField(default=False, verbose_name=_('آیا میخواهید مارکت انجام شود؟ '))

    stop_loss = models.DecimalField(decimal_places=20, max_digits=30, blank=False,
                                    verbose_name='حد ضرر')
    tp1 = models.DecimalField(decimal_places=20, max_digits=30, blank=False,
                              verbose_name='حد سود ۱')
    tp2 = models.DecimalField(decimal_places=20, max_digits=30, blank=False,
                              verbose_name='حد سود ۲')
    tp3 = models.DecimalField(decimal_places=20, max_digits=30, blank=False,
                              verbose_name='حد سود ۳')
    tp4 = models.DecimalField(decimal_places=20, max_digits=30, blank=False,
                              verbose_name='حد سود ۴')
    tp5 = models.DecimalField(decimal_places=20, max_digits=30, blank=False,
                              verbose_name='حد سود ۵')

    leverage = models.IntegerField(verbose_name=_('تعیین لورج (بیشتر از ۵۰ اوردر ثبت نخواهد شد)'), default=1)
    volume = models.IntegerField(verbose_name='تعیین حجم معامله بر اساس دلار', default=20)

    position_status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=50,
        default=WAITING,
        verbose_name=_('وضعیت معامله')
    )
    remove_signal_strategy = models.CharField(max_length=100, choices=CLOSE_CHOICE, default=CLOSE_2,
                                              verbose_name="استراتژی حذف سیگنال")

    created_at = models.DateTimeField(default=timezone.now, verbose_name=_('تاریخ ثبت سیگنال'))

    class Meta:
        verbose_name = _('سیگنال')
        verbose_name_plural = _('سیگنال ها')

    def __str__(self):
        return self.symbol
