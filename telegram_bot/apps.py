from django.apps import AppConfig


class TelegramBotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'telegram_bot'

    def ready(self):
        """
        Initialize the Telegram bot when the app is ready.
        """
        # Import the bot module to start it
        from . import bot  # noqa
