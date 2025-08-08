import asyncio
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, ContextTypes, MessageHandler, CommandHandler, filters

# Your bot token from BotFather
BOT_TOKEN = "8224719724:AAH3koXkHsyNgy2ZTeLfkwASSjaHGtSRW-I"

# Your Telegram ID (get from @userinfobot)
ADMIN_CHAT_ID = 1237435256

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact_button = KeyboardButton("📱 Share Contact", request_contact=True)
    reply_markup = ReplyKeyboardMarkup([[contact_button]], resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text("Please share your contact to continue:", reply_markup=reply_markup)

# Handler when user shares contact
async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    user = update.message.from_user

    # Prepare message for admin
    msg = f"📩 New Contact Received:\n\n"
    msg += f"👤 Name: {contact.first_name or user.full_name}\n"
    msg += f"📞 Phone: {contact.phone_number}\n"
    msg += f"🆔 Username: @{user.username}\n"
    msg += f"🆔 User ID: {user.id}"

    # Send details to admin
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=msg)

    # Acknowledge to user
    await update.message.reply_text("✅ Thank you! Your contact has been shared.")

# Run the bot using asyncio (for Pydroid 3)
async def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))

    print("🤖 Bot is running...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()  # Keeps the bot running

# For Pydroid 3: Run this inside asyncio loop
try:
    asyncio.get_event_loop().run_until_complete(main())
except RuntimeError:
    # If loop already running (e.g. in Pydroid 3), then use create_task
    asyncio.create_task(main())