"""
Telegram bot integration for VolunteerHub.
"""
import logging
import os
from django.conf import settings
from django.utils import timezone
from django.db.models import Q
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import telegram
# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get Telegram token from settings
TOKEN = getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
CHANNEL_ID = getattr(settings, 'TELEGRAM_CHANNEL_ID', '')

# Initialize bot
bot = None
if TOKEN:
    try:
        bot = telegram.Bot(token=TOKEN)
        logger.info("Telegram bot initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize Telegram bot: {e}")


async def start_bot():
    """
    Start the Telegram bot if it's configured.
    """
    if not TOKEN:
        logger.warning("Telegram bot token not set. Bot will not be started.")
        return

    try:
        application = Application.builder().token(TOKEN).build()

        # Register command handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("events", events_command))

        await application.initialize()
        await application.start()
        await application.run_polling()

    except Exception as e:
        logger.error(f"Failed to start Telegram bot: {e}")
        if application:
            await application.shutdown()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler for the /start command.
    """
    welcome_text = (
        "Welcome to VolunteerHub Bot! 🌟\n\n"
        "I can help you stay updated with the latest volunteer opportunities. "
        "Use /events to see active events or /help for more information."
    )
    await update.message.reply_text(welcome_text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler for the /help command.
    """
    help_text = (
        "VolunteerHub Bot Commands:\n\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/events - List active volunteer events\n\n"
        "Visit our website for more features!"
    )
    await update.message.reply_text(help_text)


async def events_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handler for the /events command. Returns a list of active events.
    """
    # Import here to avoid circular imports
    from events.models import Event
    
    events = Event.objects.filter(
        status=Event.Status.ACTIVE,
        date__gte=timezone.now()
    ).order_by('date')[:5]
    
    if not events:
        await update.message.reply_text("There are no active events at the moment. Check back later!")
        return
    
    response = "📅 Upcoming Volunteer Events:\n\n"
    for event in events:
        response += f"🔸 {event.title}\n"
        response += f"📆 {event.date.strftime('%d %b %Y, %H:%M')}\n"
        response += f"📍 {event.location}\n"
        response += f"👥 {event.registered_count}/{event.capacity} registered\n\n"
    
    response += "Check our website for more details and to register!"
    await update.message.reply_text(response)


async def shutdown():
    """
    Gracefully shut down the bot.
    """
    try:
        if bot:
            await bot.close()
        logger.info("Bot shutdown complete")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")


def send_telegram_notification(event):
    """
    Send a notification about a new event to the Telegram channel.
    """
    if not TOKEN or not CHANNEL_ID or not bot:
        logger.warning("Telegram bot not configured correctly. Notification not sent.")
        return
    
    try:
        message = (
            f"🆕 New Volunteer Opportunity!\n\n"
            f"📌 *{event.title}*\n\n"
            f"📝 {event.description[:100]}...\n\n"
            f"🗓️ {event.date.strftime('%d %b %Y, %H:%M')}\n"
            f"📍 {event.location}\n"
            f"👥 Capacity: {event.capacity} volunteers\n\n"
            f"Join us and make a difference! Check our website for more details and to register."
        )
        
        bot.send_message(
            chat_id=CHANNEL_ID,
            text=message,
            parse_mode=telegram.ParseMode.MARKDOWN
        )
        logger.info(f"Notification sent for event: {event.title}")
    except Exception as e:
        logger.error(f"Failed to send Telegram notification: {e}")

def main():
    import asyncio
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(start_bot())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        loop.run_until_complete(shutdown())
    finally:
        loop.close()
# Don't start the bot automatically in development
# The bot will be initialized when the app starts
if settings.DEBUG:
    logger.info("Bot will not start automatically in DEBUG mode")
    main()
else:
    # Start the bot in production
    main()