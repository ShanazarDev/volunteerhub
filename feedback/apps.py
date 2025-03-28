from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FeedbackConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'feedback'
    verbose_name = _('Feedback and Ratings')

    def ready(self):
        """
        Import signals to register them with Django.
        """
        import feedback.signals  # noqa