from django.apps import AppConfig


class EventsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'events'

    def ready(self):
        """
        Initialize signals when the app is ready.
        """
        import events.signals  # noqa
