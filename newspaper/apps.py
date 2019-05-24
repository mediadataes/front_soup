from django.apps import AppConfig


class NewspaperConfig(AppConfig):
    name = 'newspaper'

    def ready(self):
        import newspaper.signals
