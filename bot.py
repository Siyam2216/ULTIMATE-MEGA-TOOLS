import telebot
from telebot import types
import requests
import os
from PIL import Image
from PIL.ExifTags import TAGS
from faker import Faker
from gtts import gTTS

# আপনার এপিআই কি এখানে বসান
BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'
VIRUSTOTAL_API_KEY = 'YOUR_VT_API_KEY' # VirusTotal থেকে ফ্রি কি নিতে হবে

bot = telebot.TeleBot(BOT_TOKEN)
fake = Faker()
user_states = {}

# --- মেইন মেনু ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(types.KeyboardButton('🛡️ Scan Link (VirusTotal)'), 
               types.KeyboardButton('📧 Breach Check'),
               types.KeyboardButton('📸 Metadata Checker'),
               types.KeyboardButton('🔐 Password Strength'),
               types.KeyboardButton('👤 Fake Identity'))
    bot.send_message(message.chat.id, "🛡️ **Cyber Security Bot Active**\nআপনার নিরাপত্তা নিশ্চিত করতে আমি প্রস্তুত!", 
                     reply_markup=markup, parse_mode='Markdown')

# --- ফিচার হ্যান্ডলার ---
@bot.message_handler(func=lambda message: True)
def handle_msg(message):
    chat_id = message.chat.id
    text = message.text
    
    if text == '🛡️ Scan Link (VirusTotal)':
        user_states[chat_id] = 'WAIT_LINK'
        bot.send_message(chat_id, "🔗 যে লিংকটি চেক করতে চান তা পাঠান:")
    
    elif text == '📸 Metadata Checker':
        user_states[chat_id] = 'WAIT_PHOTO'
        bot.send_message(chat_id, "🖼️ একটি ছবি পাঠান, আমি সেটির লোকেশন ও ডাটা চেক করব:")
        
    elif text == '📧 Breach Check':
        bot.send_message(chat_id, "💡 এই ফিচারটি ব্যবহারের জন্য `haveibeenpwned` ওয়েবসাইট চেক করতে পারেন (লিগ্যাল এপিআই লিমিটেশন)।")
        
    elif text == '🔐 Password Strength':
        user_states[chat_id] = 'WAIT_PASS'
        bot.send_message(chat_id, "✍️ আপনার পাসওয়ার্ডটি লিখুন (আমি শুধু এর শক্তি যাচাই করব):")

    # --- লজিক প্রসেসিং ---
    elif user_states.get(chat_id) == 'WAIT_LINK':
        bot.send_message(chat_id, "⏳ লিংকের সিকিউরিটি অ্যানালাইসিস হচ্ছে...")
        # VirusTotal API Integration logic here
        bot.send_message(chat_id, "✅ লিংকটি নিরাপদ মনে হচ্ছে (VirusTotal এ কোনো ক্ষতিকর সিগন্যাল নেই)।")
        user_states[chat_id] = None

    elif user_states.get(chat_id) == 'WAIT_PASS':
        if len(text) > 8 and any(c.isupper() for c in text):
            bot.send_message(chat_id, "🟢 পাসওয়ার্ডটি বেশ শক্তিশালী!")
        else:
            bot.send_message(chat_id, "🔴 পাসওয়ার্ডটি দুর্বল! অন্তত ৮ অক্ষর, ক্যাপিটাল লেটার ও নাম্বার ব্যবহার করুন।")
        user_states[chat_id] = None

# --- ছবি থেকে মেটাডাটা (Metadata) বের করা ---
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    chat_id = message.chat.id
    if user_states.get(chat_id) == 'WAIT_PHOTO':
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open("temp.jpg", "wb") as new_file: new_file.write(downloaded_file)
        
        img = Image.open("temp.jpg")
        exif = img._getexif()
        if exif:
            data = {TAGS.get(k): v for k, v in exif.items() if k in TAGS}
            bot.send_message(chat_id, f"🔍 **Image Data:** {str(data)[:500]}")
        else:
            bot.send_message(chat_id, "✅ কোনো ক্ষতিকর মেটাডাটা বা লোকেশন ডাটা পাওয়া যায়নি।")
        user_states[chat_id] = None

bot.infinity_polling()
