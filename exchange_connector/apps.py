from django.apps import AppConfig


class ExchangeConnetorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'exchange_connector'

    def ready(self):
        import exchange_connector.signals
