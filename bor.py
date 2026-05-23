import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot token
TOKEN = os.getenv("8674194296:AAGqxTPggfH52IyefdVP8565SFOJcmspOwI")

# Register user function (aapke database ke according adjust karein)
def register_user(update):
    # TODO: Add your user registration logic here
    pass

def get_user(user_id):
    # TODO: Add your get user logic here
    return {"id": user_id, "name": "User"}

def prefix(user):
    # TODO: Add your prefix logic here
    return ""

# Welcome photo URL (aapki di hui image)
WELCOME_PHOTO = "https://files.catbox.moe/xg13wf.png"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
                style="danger"  # 🔴 RED BUTTON - YAHAN CHANGE KIYA!
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

    # PHOTO KE SAATH SEND KARO - YAHAN CHANGE KIYA!
    try:
        await update.message.reply_photo(
            photo=WELCOME_PHOTO,
            caption=text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        logger.error(f"Failed to send photo: {e}")
        # Agar photo fail ho to fallback (sirf text)
        await update.message.reply_text(
            text=text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎮 Bot Commands:\n/start - Start the bot\n/help - Get help",
        parse_mode=ParseMode.MARKDOWN
    )

def main():
    """Start the bot"""
    application = Application.builder().token(TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    # Start bot
    print("🤖 Mikasa Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
