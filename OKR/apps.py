from django.apps import AppConfig


class OkrConfig(AppConfig):
    name = 'OKR'

    def ready(self):
        import OKR.signals
