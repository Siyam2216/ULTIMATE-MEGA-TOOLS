import os
import base64
import qrcode
import requests
import telebot
from telebot import types
import pyshorteners
from gtts import gTTS
from faker import Faker

# ১. Environment variable থেকে টোকেন নেওয়া হচ্ছে (Render এ এটাই সবচেয়ে নিরাপদ পদ্ধতি)
BOT_TOKEN = os.environ.get('BOT_TOKEN')

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable সেট করা হয়নি! Render Dashboard এ গিয়ে সেট করুন।")

bot = telebot.TeleBot(BOT_TOKEN)
shortener = pyshorteners.Shortener()
fake = Faker()

# ব্যবহারকারীর স্টেট ট্র্যাক করার জন্য ডিকশনারি
user_states = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "╔══════════════════════╗\n"
        "⚡   **ULTIMATE MEGA TOOLS**   ⚡\n"
        "╚══════════════════════╝\n\n"
        "👋 **স্বাগতম!**\n"
        "✨ নিচের মেনু থেকে আপনার প্রয়োজনীয় টুলটি সিলেক্ট করুন।"
    )

    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    btn_ip = types.KeyboardButton('🔍 IP Tracker')
    btn_url = types.KeyboardButton('🔗 URL Shortener')
    btn_expand = types.KeyboardButton('🌐 URL Expander')
    btn_qr = types.KeyboardButton('🖼️ QR Generator')
    btn_tts = types.KeyboardButton('📝 Text to Speech')
    btn_fake = types.KeyboardButton('👤 Fake Info Gen')
    btn_b64 = types.KeyboardButton('🔐 Base64 Tool')
    btn_extra = types.KeyboardButton('🔥 Extra Tools 🔥')

    markup.row(btn_ip, btn_url)
    markup.row(btn_expand, btn_qr)
    markup.row(btn_tts, btn_fake)
    markup.row(btn_b64)
    markup.row(btn_extra)

    bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown', reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    chat_id = message.chat.id
    current_state = user_states.get(chat_id)
    text = message.text.strip()

    # --- বাটন অ্যাকশনসমূহ ---
    if text == '🔗 URL Shortener':
        user_states[chat_id] = 'WAITING_FOR_URL'
        bot.send_message(chat_id, "🔗 আপনার বড় লিংকটি (URL) পাঠান যা ছোট করতে চান:")
        return

    elif text == '🌐 URL Expander':
        user_states[chat_id] = 'WAITING_FOR_SHORT_URL'
        bot.send_message(chat_id, "🌐 যেকোনো ছোট করা লিংক পাঠান, বট সেটির আসল গন্তব্য বের করে দেবে:")
        return

    elif text == '🔍 IP Tracker':
        user_states[chat_id] = 'WAITING_FOR_IP'
        bot.send_message(chat_id, "🔍 আইপি অ্যাড্রেসটি (IP Address) পাঠান (যেমন: 8.8.8.8):")
        return

    elif text == '🖼️ QR Generator':
        user_states[chat_id] = 'WAITING_FOR_QR_TEXT'
        bot.send_message(chat_id, "🔗 QR Code তৈরি করার জন্য লিংক বা টেক্সট পাঠান:")
        return

    elif text == '📝 Text to Speech':
        user_states[chat_id] = 'WAITING_FOR_TTS_TEXT'
        bot.send_message(chat_id, "✍️ যেকোনো ইংরেজি বা বাংলা টেক্সট পাঠান, বট সেটিকে ভয়েস মেসেজ বানিয়ে দেবে:")
        return

    elif text == '👤 Fake Info Gen':
        fake_profile = (
            "👤 **Fake Test Profile (Software Testing Only)**\n\n"
            f"📛 **Name:** {fake.name()}\n"
            f"🏠 **Address:** {fake.address().replace(chr(10), ', ')}\n"
            f"📧 **Email:** {fake.email()}\n"
            f"🏢 **Company:** {fake.company()}\n"
        )
        bot.send_message(chat_id, fake_profile, parse_mode='Markdown')
        return

    elif text == '🔐 Base64 Tool':
        inline_markup = types.InlineKeyboardMarkup()
        inline_markup.add(
            types.InlineKeyboardButton("Encode (টেক্সট ➡️ কোড)", callback_data="b64_encode"),
            types.InlineKeyboardButton("Decode (কোড ➡️ টেক্সট)", callback_data="b64_decode")
        )
        bot.send_message(chat_id, "🔐 আপনি টেক্সট বেস-৬৪ এ কনভার্ট করতে চান নাকি ডিকোড করতে চান?", reply_markup=inline_markup)
        return

    elif text == '🔥 Extra Tools 🔥':
        bot.send_message(chat_id, "🛠️ অল-ইন-ওয়ান মেগা টুলস বটের সব ফিচার সচল আছে।")
        return

    # --- ইনপুট প্রসেসিং (স্টেট অনুযায়ী) ---
    if current_state == 'WAITING_FOR_URL':
        if text.startswith('http://') or text.startswith('https://'):
            try:
                short_url = shortener.tinyurl.short(text)
                bot.send_message(chat_id, f"✅ **ছোট করা লিংক:**\n\n`{short_url}`", parse_mode='Markdown')
            except Exception:
                bot.send_message(chat_id, "❌ লিংকটি ছোট করতে সমস্যা হয়েছে।")
        else:
            bot.send_message(chat_id, "❌ ভুল ফরম্যাট! লিংকটি `http://` বা `https://` দিয়ে শুরু হতে হবে।")
        user_states[chat_id] = None

    elif current_state == 'WAITING_FOR_SHORT_URL':
        bot.send_message(chat_id, "⏳ লিংকের ভেতরের আসল ঠিকানা বের করা হচ্ছে...")
        try:
            response = requests.get(text, allow_redirects=True, timeout=10)
            bot.send_message(chat_id, f"🌐 **আসল বড় লিংক (Redirected Destination):**\n\n`{response.url}`", parse_mode='Markdown')
        except Exception:
            bot.send_message(chat_id, "❌ লিংকটি এক্সপ্যান্ড করা সম্ভব হয়নি বা ইউআরএলটি ভুল।")
        user_states[chat_id] = None

    elif current_state == 'WAITING_FOR_IP':
        try:
            res = requests.get(f"http://ip-api.com/json/{text}").json()
            if res.get('status') == 'success':
                ip_msg = (
                    f"🔍 **IP Details Found!**\n\n"
                    f"🏳️ **Country:** {res.get('country')}\n"
                    f"📍 **Region/City:** {res.get('regionName')} / {res.get('city')}\n"
                    f"🏢 **ISP:** {res.get('isp')}\n"
                    f"⏰ **Timezone:** {res.get('timezone')}"
                )
                bot.send_message(chat_id, ip_msg, parse_mode='Markdown')
            else:
                bot.send_message(chat_id, "❌ অবৈধ আইপি অ্যাড্রেস।")
        except Exception:
            bot.send_message(chat_id, "❌ সমস্যা হয়েছে।")
        user_states[chat_id] = None

    elif current_state == 'WAITING_FOR_QR_TEXT':
        try:
            qr_img = qrcode.make(text)
            f_path = f"qr_{chat_id}.png"
            qr_img.save(f_path)
            with open(f_path, 'rb') as photo:
                bot.send_photo(chat_id, photo, caption="✅ QR Code সম্পূর্ণ রেডি!")
            os.remove(f_path)
        except Exception:
            bot.send_message(chat_id, "❌ সমস্যা হয়েছে।")
        user_states[chat_id] = None

    elif current_state == 'WAITING_FOR_TTS_TEXT':
        try:
            lang = 'bn' if any('\u0980' <= c <= '\u09fa' for c in text) else 'en'
            tts = gTTS(text=text, lang=lang)
            a_path = f"voice_{chat_id}.ogg"
            tts.save(a_path)
            with open(a_path, 'rb') as audio:
                bot.send_voice(chat_id, audio, caption="🗣️ আপনার টেক্সটের ভয়েস নোট!")
            os.remove(a_path)
        except Exception:
            bot.send_message(chat_id, "❌ সমস্যা হয়েছে।")
        user_states[chat_id] = None

    elif current_state == 'WAITING_FOR_B64_ENC':
        encoded = base64.b64encode(text.encode('utf-8')).decode('utf-8')
        bot.send_message(chat_id, f"🔐 **Encoded Base64 Code:**\n\n`{encoded}`", parse_mode='Markdown')
        user_states[chat_id] = None

    elif current_state == 'WAITING_FOR_B64_DEC':
        try:
            decoded = base64.b64decode(text.encode('utf-8')).decode('utf-8')
            bot.send_message(chat_id, f"🔓 **Decoded Text:**\n\n`{decoded}`", parse_mode='Markdown')
        except Exception:
            bot.send_message(chat_id, "❌ অবৈধ বেস-৬৪ কোড! ডিকোড করা সম্ভব হয়নি।")
        user_states[chat_id] = None


@bot.callback_query_handler(func=lambda call: call.data.startswith('b64_'))
def handle_b64_callback(call):
    chat_id = call.message.chat.id
    if call.data == "b64_encode":
        user_states[chat_id] = 'WAITING_FOR_B64_ENC'
        bot.send_message(chat_id, "✍️ যে টেক্সটটি এনকোড করতে চান তা লিখে পাঠান:")
    elif call.data == "b64_decode":
        user_states[chat_id] = 'WAITING_FOR_B64_DEC'
        bot.send_message(chat_id, "🔓 যে বেস-৬৪ কোডটি ডিকোড করতে চান তা পাঠান:")


print("Ultimate Multi-Tool Bot is running...")
bot.infinity_polling()
