import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot token - environment variable se lelo
TOKEN = os.getenv("8674194296:AAGqxTPggfH52IyefdVP8565SFOJcmspOwI")

# Premium animated emoji ke saath welcome message
WELCOME_MESSAGE = """
✨ <b>Hey {first_name},</b> ✨

🎮 <b>Welcome to Game Bot!</b> 🎮

🎯 Exciting games and amazing features await you!

Click on the help button for more info.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message with premium animated emoji style buttons"""
    
    # User ka naam lelo
    user = update.effective_user
    first_name = user.first_name if user.first_name else "Player"
    
    # Customized welcome message with user's name
    custom_welcome = WELCOME_MESSAGE.format(first_name=first_name)
    
    # Create inline keyboard with RED OWNER BUTTON (style="danger")
    keyboard = [
        [
            InlineKeyboardButton(
                "➕ Add me to your group", 
                url=f"https://t.me/{context.bot.username}?startgroup=botstart"
            ),
        ],
        [
            InlineKeyboardButton("👥 Groups", callback_data="groups"),
        ],
        [
            InlineKeyboardButton("❓ Help", callback_data="help"),
        ],
        [
            InlineKeyboardButton(
                "👑 OWNER 👑", 
                url="https://t.me/light_speedy",
                style="danger"  # 🔴 RED BUTTON!
            ),
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Photo URL - aapki di hui image
    photo_url = "https://files.catbox.moe/xg13wf.png"
    
    try:
        await update.message.reply_photo(
            photo=photo_url,
            caption=custom_welcome,
            parse_mode="HTML",
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Failed to send photo: {e}")
        # Agar photo fail ho to fallback
        await update.message.reply_text(
            custom_welcome,
            parse_mode="HTML",
            reply_markup=reply_markup
        )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "groups":
        # Groups sub-menu
        sub_keyboard = [
            [
                InlineKeyboardButton(
                    "🎭 𝙼𝙸𝙳𝙽𝙸𝙶𝙷𝚃 𝙲𝙻𝚄𝙱", 
                    url="https://t.me/midnight_chatclub"
                ),
            ],
            [
                InlineKeyboardButton(
                    "🏴‍☠️ 𝑶𝒏𝒆 𝑷𝒊𝒆𝒄𝒆 𝑾𝒐𝒓𝒍𝒅", 
                    url="https://t.me/+em6PdzD7hB83Zjc1"
                ),
            ],
            [
                InlineKeyboardButton("🔙 Back", callback_data="back_to_main"),
            ]
        ]
        sub_reply_markup = InlineKeyboardMarkup(sub_keyboard)
        
        await query.edit_message_caption(
            caption="🎮 <b>Our Gaming Communities</b> 🎮\n\nJoin these awesome groups!",
            parse_mode="HTML",
            reply_markup=sub_reply_markup
        )
    
    elif query.data == "help":
        # Help response
        help_text = """
🎮 <b>Game Bot Help</b> 🎮

✨ <b>Commands:</b>
/start - Start the bot

🎯 <b>About:</b>
This is a gaming bot with exciting features!

⚡ More games coming soon!
        """
        await query.edit_message_caption(
            caption=help_text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_to_main")]])
        )
    
    elif query.data == "back_to_main":
        # Get user name again for main menu
        user = update.effective_user
        first_name = user.first_name if user.first_name else "Player"
        custom_welcome = WELCOME_MESSAGE.format(first_name=first_name)
        
        # Return to main menu with RED owner button
        main_keyboard = [
            [
                InlineKeyboardButton(
                    "➕ Add me to your group", 
                    url=f"https://t.me/{context.bot.username}?startgroup=botstart"
                ),
            ],
            [
                InlineKeyboardButton("👥 Groups", callback_data="groups"),
            ],
            [
                InlineKeyboardButton("❓ Help", callback_data="help"),
            ],
            [
                InlineKeyboardButton(
                    "👑 OWNER 👑", 
                    url="https://t.me/light_speedy",
                    style="danger"  # 🔴 RED BUTTON!
                ),
            ]
        ]
        await query.edit_message_caption(
            caption=custom_welcome,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(main_keyboard)
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send help message when /help command is issued"""
    help_text = """
🎮 <b>Game Bot Help</b> 🎮

✨ <b>Commands:</b>
/start - Start the bot

🎯 <b>About:</b>
This is a gaming bot with exciting features!

⚡ More games coming soon!
    """
    await update.message.reply_text(help_text, parse_mode="HTML")

def main():
    """Start the bot"""
    # Create Application
    application = Application.builder().token(TOKEN).build()
    
    # Add command handlers - sirf start aur help
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    # Add callback query handler for buttons
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Start the bot
    print("🎮 Game Bot is starting...")
    print("✅ Bot is running with RED Owner button!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
