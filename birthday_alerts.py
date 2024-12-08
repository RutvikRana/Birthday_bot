import telegram
import datetime
from datetime import timedelta
import json
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot Configuration
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHANNEL_ID = '-1002362859032'

try:
    bot = telegram.Bot(token=BOT_TOKEN)
except Exception as e:
    logger.error(f"Bot initialization failed: {e}")
    raise

def load_birthdays():
    """Load birthdays from JSON file"""
    try:
        with open('birthdays.json', 'r') as file:
            return json.load(file)['birthdays']
    except FileNotFoundError:
        logger.warning("birthdays.json not found, using default data")
        return [
            {"name": "Friend1", "date": "12-25", "nickname": "buddy"},
            {"name": "Friend2", "date": "01-15", "nickname": "bestie"}
        ]

def send_message(person, message_type):
    """Send formatted message based on time"""
    messages = {
        "morning": f"⚠️ REMINDER: Tomorrow is {person['name']}'s birthday! 🎂\n\nDon't forget to wish your {person['nickname']}! 🎉",
        "evening": f"🔔 Evening Alert: Get ready! {person['name']}'s birthday is tomorrow! 🎈\n\nSet your notifications on! 📱",
        "night": f"🌙 Final Reminder: {person['name']}'s birthday starts in 1 hour!\n\nDon't miss being the first to wish! ⭐"
    }
    
    try:
        bot.send_message(
            chat_id=CHANNEL_ID,
            text=messages[message_type],
            parse_mode='HTML'
        )
        logger.info(f"Successfully sent {message_type} alert for {person['name']}")
    except Exception as e:
        logger.error(f"Failed to send message: {e}")

def check_upcoming():
    """Check and send birthday alerts"""
    try:
        today = datetime.datetime.now()
        tomorrow = (today + timedelta(days=1)).strftime('%m-%d')
        current_hour = today.hour
        
        birthdays = load_birthdays()
        
        for person in birthdays:
            if person['date'] == tomorrow:
                if current_hour == 10:
                    send_message(person, "morning")
                elif current_hour == 18:
                    send_message(person, "evening")
                elif current_hour == 23:
                    send_message(person, "night")
                    
    except Exception as e:
        logger.error(f"Error in check_upcoming: {e}")

def test_bot():
    """Test bot connectivity"""
    try:
        bot.send_message(
            chat_id=CHANNEL_ID,
            text="🤖 Bot is operational! Test message successful!"
        )
        logger.info("Bot test successful")
        return True
    except Exception as e:
        logger.error(f"Bot test failed: {e}")
        return False

if __name__ == "__main__":
    logger.info("Starting birthday alert script")
    check_upcoming()    
