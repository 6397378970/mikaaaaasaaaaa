import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG  # DEBUG mode se pata chalega kya ho raha hai
)
logger = logging.getLogger(__name__)

# Bot token
TOKEN = os.getenv("8674194296:AAGqxTPggfH52IyefdVP8565SFOJcmspOwI")

# Welcome photo
WELCOME_PHOTO = "https://files.catbox.moe/xg13wf.png"

# Simple functions (without database)
def register_user(update):
    user = update.effective_user
    logger.info(f"User registered: {user.id} - {user.first_name}")
    # TODO: Add your database logic here

def get_user(user_id):
    logger.info(f"Getting user: {user_id}")
    return {"id": user_id, "name": "User"}

def prefix(user):
    return ""  # Aapka custom prefix logic yahan

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message with photo and red owner button"""
    
    logger.info(f"Start command received from user: {update.effective_user.id}")
    
    register_user(update)

    u = update.effective_user
    user = get_user(u.id)
    p = prefix(user)

    text = (
        "✨ Hey I'm Mikasa\n\n Enjoy and play 🚀"
    )

    keyboard = [
        [
            InlineKeyboardButton(
                "👥 Groups",
                url="https://t.me/midnight_chatclub"
            ),
            InlineKeyboardButton(
                "👑 Owner",
                url="https://t.me/light_speedy",
            )
        ],
        [
            InlineKeyboardButton(
                "📢 Channel",
                url="https://t.me/anonymous_rides"
            )
        ],
        [
            InlineKeyboardButton(
                "➕ Add Me To Your Group",
                url=f"https://t.me/mikasa_ibot?startgroup=true"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send photo with caption
    try:
        await update.message.reply_photo(
            photo=WELCOME_PHOTO,
            caption=text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        logger.info("Photo message sent successfully")
    except Exception as e:
        logger.error(f"Failed to send photo: {e}")
        # Fallback to text only
        await update.message.reply_text(
            text=text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        logger.info("Text message sent as fallback")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎮 Bot Commands:\n/start - Start the bot\n/help - Get help",
        parse_mode=ParseMode.MARKDOWN
    )

async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Test command to check if bot is responding"""
    await update.message.reply_text("Bot is working! 🎉")

def main():
    """Start the bot"""
    print("🤖 Mikasa Bot is starting...")
    print(f"Using token: {TOKEN[:10]}...")  # Token ka first part show karega
    
    # Create Application
    application = Application.builder().token(TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("test", test_command))  # Test command
    
    # Callback handler for buttons (agar future mein use karo)
    # application.add_handler(CallbackQueryHandler(button_callback))
    
    # ✅ IMPORTANT: Webhook delete karo pehle (conflict resolve karne ke liye)
    print("Deleting old webhook...")
    application.bot.delete_webhook(drop_pending_updates=True)
    
    # ✅ Polling mode start karo
    print("Starting polling...")
    application.run_polling(
        poll_interval=1.0,
        timeout=30,
        allowed_updates=Update.ALL_TYPES
    )

if __name__ == '__main__':
    main()
