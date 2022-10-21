from django.apps import AppConfig


class SignalCenterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'signal_center'
    verbose_name = "مرکز سیگنال دهی"

    def ready(self) -> None:
        import signal_center.signals
