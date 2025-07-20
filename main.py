from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# 🔐 Your bot token
BOT_TOKEN = "7998856824:AAHeWc0dWIqPmZsPSsn5wM4A0X1vdzFRmmw"

# 🧑 Your Telegram chat ID (where contacts will be sent)
OWNER_CHAT_ID = 7033401055

# 🚀 /start command handler
def start(update: Update, context: CallbackContext):
    button = KeyboardButton("📞 Share Contact", request_contact=True)
    reply_markup = ReplyKeyboardMarkup([[button]], resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text("Hey! Tap below to share your phone number:", reply_markup=reply_markup)

# 📩 Handle contact messages
def contact_handler(update: Update, context: CallbackContext):
    contact = update.message.contact
    message = (
        f"📲 New Contact:\n\n"
        f"👤 Name: {contact.first_name}\n"
        f"📞 Phone: {contact.phone_number}\n"
        f"🆔 User ID: {update.effective_user.id}"
    )
    context.bot.send_message(chat_id=OWNER_CHAT_ID, text=message)
    update.message.reply_text("✅ Thanks! Got your contact.")

# 🔁 Main function
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.contact, contact_handler))

    updater.start_polling()
    print("✅ Bot is running...")
    updater.idle()

if __name__ == '__main__':
    main()
