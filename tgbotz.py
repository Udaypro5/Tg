import logging
import random
import string
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Set up logging for debugging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# In-memory storage for users and referral mapping
# In production, replace these with a persistent database.
users = {}           # Maps user_id to a dict: {'referral_code': str, 'referrals': int, 'points': int}
referral_to_user = {}  # Maps referral_code to the user_id who owns it

def generate_referral_code(length=6):
    """Generate a random referral code."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def start(update: Update, context: CallbackContext) -> None:
    """Handle the /start command. Accept an optional referral code as argument."""
    user = update.message.from_user
    user_id = user.id

    # Register new user if not already in the system
    if user_id not in users:
        referral_code = generate_referral_code()
        users[user_id] = {'referral_code': referral_code, 'referrals': 0, 'points': 0}
        referral_to_user[referral_code] = user_id
        logger.info("Registered new user: %s with code %s", user.first_name, referral_code)

    message = f"Hello, {user.first_name}!\n"
    message += "Welcome to the Refer & Earn Bot.\n"
    message += f"Your referral code is: {users[user_id]['referral_code']}\n"
    message += "Share this code with your friends to earn rewards!\n"

    # Check if the user started the bot with a referral code argument (e.g., /start REF123)
    if context.args:
        provided_code = context.args[0].strip().upper()
        # Validate referral code and ensure user is not self-referring
        if provided_code in referral_to_user and referral_to_user[provided_code] != user_id:
            referrer_id = referral_to_user[provided_code]
            users[referrer_id]['referrals'] += 1
            users[referrer_id]['points'] += 10  # Award 10 points per referral (adjust as needed)
            message += "\nReferral bonus applied for your referrer!\n"
            logger.info("User %s referred by %s", user.first_name, referrer_id)
        else:
            message += "\nInvalid or self referral code provided.\n"

    update.message.reply_text(message)

def refer(update: Update, context: CallbackContext) -> None:
    """Send the user their unique referral code."""
    user = update.message.from_user
    user_id = user.id

    if user_id in users:
        referral_code = users[user_id]['referral_code']
        update.message.reply_text(f"Your referral code is: {referral_code}")
    else:
        update.message.reply_text("You are not registered. Please use /start to register.")

def earn(update: Update, context: CallbackContext) -> None:
    """Show the user their earned points and referral count."""
    user = update.message.from_user
    user_id = user.id

    if user_id in users:
        points = users[user_id]['points']
        referrals = users[user_id]['referrals']
        update.message.reply_text(
            f"You have earned {points} points from {referrals} successful referrals."
        )
    else:
        update.message.reply_text("You are not registered. Please use /start to register.")

def main():
    # Replace 'YOUR_TELEGRAM_BOT_API_TOKEN' with your actual Telegram Bot API token.
    updater = Updater("7574244377:AAHWv4GgJNXzob1XMuUJBCvLZ-rbgSTzpj8", use_context=True)
    dispatcher = updater.dispatcher

    # Command handlers
    dispatcher.add_handler(CommandHandler("start", start, pass_args=True))
    dispatcher.add_handler(CommandHandler("refer", refer))
    dispatcher.add_handler(CommandHandler("earn", earn))

    # Start the bot
    updater.start_polling()
    logger.info("Bot started polling...")
    updater.idle()

if __name__ == '__main__':
    main()