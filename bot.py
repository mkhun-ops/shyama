import logging
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

# --- Configuration ---
import os
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # Use environment variable for security
ALLOWED_USERS = {8040038495}  # Your Telegram user ID

# --- Logging Setup ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Handler Function ---
def file_handler(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        logger.warning(f"Unauthorized access attempt by user {user_id}")
        return

    message = update.message
    file = (
        message.document or
        message.video or
        message.audio or
        (message.photo[-1] if message.photo else None)
    )

    if not file:
        message.reply_text("❗ Please send a file (document, video, audio, or photo).")
        return

    try:
        telegram_file = context.bot.get_file(file.file_id)
        direct_link = telegram_file.file_path
        message.reply_text(
            f"✅ Direct download link (valid ~1 hour):\n{direct_link}"
        )
        logger.info(f"Sent direct link to user {user_id}: {direct_link}")
    except Exception as e:
        logger.error(f"Error generating link: {e}")
        message.reply_text("❌ An error occurred while processing your file.")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(
        Filters.document | Filters.video | Filters.audio | Filters.photo,
        file_handler
    ))

    logger.info("Bot started. Listening for files...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
