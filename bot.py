import telebot
from telebot import types
import pyshorteners
from truecallerpy import search_phonenumber
import urllib.parse
import requests
import random
import string
import qrcode
import os
import base64
from gtts import gTTS
from faker import Faker

# ১. আপনার টোকেন ও এপিআই কি এখানে বসান
BOT_TOKEN = os.environ.get('BOT_TOKEN')
TRUECALLER_AUTH_KEY = 'YOUR_TRUECALLER_AUTH_KEY'

bot = telebot.TeleBot(BOT_TOKEN)
shortener = pyshorteners.Shortener()
fake = Faker()

# ব্যবহারকারীর স্টেট ট্র্যাক করার জন্য ডিকশনারি
user_states = {}

# /start কমান্ড হ্যান্ডলার
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "╔══════════════════════╗\n"
        "⚡   **ULTIMATE MEGA TOOLS**   ⚡\n"
        "╚══════════════════════╝\n\n"
        "👋 **স্বাগতম**, 🎭 `[root@--{🛡️}ROH GUARDIAN-X{👿}-- :~/Owner]$` \n"
        "✨ নিচের কাস্টম মেনু থেকে আপনার প্রয়োজনীয় টুলটি সিলেক্ট করুন।"
    )
    
    # ২ লেয়ারের কাস্টম কিবোর্ড মেনু ডিজাইন
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    
    btn_ip = types.KeyboardButton('🔍 IP Tracker')
    btn_url = types.KeyboardButton('🔗 URL Shortener')
    btn_expand = types.KeyboardButton('🌐 URL Expander')
    btn_social = types.KeyboardButton('🔍 Social Search')
    btn_qr = types.KeyboardButton('🖼️ QR Generator')
    btn_tts = types.KeyboardButton('📝 Text to Speech')
    btn_fake = types.KeyboardButton('👤 Fake Info Gen')
    btn_b64 = types.KeyboardButton('🔐 Base64 Tool')
    btn_extra = types.KeyboardButton('🔥 Extra Tools 🔥')
    
    markup.row(btn_ip, btn_url)
    markup.row(btn_expand, btn_social)
    markup.row(btn_qr, btn_tts)
    markup.row(btn_fake, btn_b64)
    markup.row(btn_extra)
    
    bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown', reply_markup=markup)

# বাটন ক্লিক এবং ইনপুট প্রসেসিং হ্যান্ডলার
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    chat_id = message.chat.id
    current_state = user_states.get(chat_id)
    text = message.text.strip()
    
    # --- বাটন অ্যাকশনসমূহ ---
    if text == '🔗 URL Shortener':
        user_states[chat_id] = 'WAITING_FOR_URL'
        bot.send_message(chat_id, "🔗 আপনার বড় লিংকটি (URL) পাঠান যা ছোট করতে চান:")
        return

    elif text == '🌐 URL Expander':
        user_states[chat_id] = 'WAITING_FOR_SHORT_URL'
        bot.send_message(chat_id, "🌐 যেকোনো ছোট করা বা সন্দেহজনক লিংক পাঠান, বট সেটির আসল গন্তব্য বের করে দেবে:")
        return

    elif text == '🔍 Social Search':
        user_states[chat_id] = 'WAITING_FOR_NUMBER'
        bot.send_message(chat_id, "📞 কান্ট্রি কোডসহ মোবাইল নাম্বারটি পাঠান (যেমন: +88017XXXXXXXX):")
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
        bot.send_message(chat_id, "✍️ যেকোনো ইংরেজি বা বাংলা টেক্সট পাঠান, বট সেটিকে ভয়েস মেসেজ বানিয়ে দেবে:")
        return

    elif text == '👤 Fake Info Gen':
        # সরাসরি ফেক ইনফো জেনারেট করে দেবে
        fake_profile = (
            "👤 **Fake Identity Details (Testing Only)**\n\n"
            f"📛 **Name:** {fake.name()}\n"
            f"🏠 **Address:** {fake.address().replace(chr(10), ', ')}\n"
            f"📧 **Email:** {fake.email()}\n"
            f"📞 **Phone:** {fake.phone_number()}\n"
            f"🏢 **Company:** {fake.company()}\n"
            f"🌐 **SSN/ID:** {fake.ssn()}"
        )
        bot.send_message(chat_id, fake_profile)
        return

    elif text == '🔐 Base64 Tool':
        # ইনলাইন চয়েস কিবোর্ড পাঠানো
        inline_markup = types.InlineKeyboardMarkup()
        inline_markup.add(
            types.InlineKeyboardButton("Encode (টেক্সট ➡️ কোড)", callback_data="b64_encode"),
            types.InlineKeyboardButton("Decode (কোড ➡️ টেক্সট)", callback_data="b64_decode")
        )
        bot.send_message(chat_id, "🔐 আপনি টেক্সট বেস-৬৪ এ কনভার্ট করতে চান নাকি ডিকোড করতে চান?", reply_markup=inline_markup)
        return
        
    elif text == '🔥 Extra Tools 🔥':
        bot.send_message(chat_id, "👑 **Developer:** Saurabh\n\n🛠️ অল-ইন-ওয়ান মেগা টুলস বটের সব ফিচার সফলভাবে সচল আছে। নতুন আইডিয়া থাকলে ডেভেলপারকে জানান!")
        return

    # --- ইনপুট প্রসেসিং (স্টেট অনুযায়ী) ---
    if current_state == 'WAITING_FOR_URL':
        if text.startswith('http://') or text.startswith('https://'):
            try:
                short_url = shortener.tinyurl.short(text)
                bot.send_message(chat_id, f"✅ **ছোট করা লিংক:**\n\n`{short_url}`", parse_mode='Markdown')
            except Exception: bot.send_message(chat_id, "❌ লিংকটি ছোট করতে সমস্যা হয়েছে।")
        else: bot.send_message(chat_id, "❌ ভুল ফরম্যাট! লিংকটি `http://` বা `https://` দিয়ে শুরু হতে হবে।")
        user_states[chat_id] = None

    elif current_state == 'WAITING_FOR_SHORT_URL':
        bot.send_message(chat_id, "⏳ লিংকের ভেতরের আসল ঠিকানা বের করা হচ্ছে...")
        try:
            response = requests.get(text, allow_redirects=True, timeout=10)
            bot.send_message(chat_id, f"🌐 **আসল বড় লিংক (Redirected Destination):**\n\n`{response.url}`")
        except Exception: bot.send_message(chat_id, "❌ লিংকটি এক্সপ্যান্ড করা সম্ভব হয়নি বা ইউআরএলটি ভুল।")
        user_states[chat_id] = None

    elif current_state == 'WAITING_FOR_NUMBER':
        if text.startswith('+') and len(text) >= 11:
            bot.send_message(chat_id, "⏳ সোশ্যাল মিডিয়া এবং ট্রুকলার ডাটাবেজ চেক করা হচ্ছে...")
            name, email, carrier = "পাওয়া যায়নি", "পাওয়া যায়নি", "পাওয়া যায়নি"
            try:
                res = search_phonenumber(text, "IN", TRUECALLER_AUTH_KEY)
                if res and 'data' in res and res['data']:
                    d = res['data'][0]
                    name = d.get('name', 'পাওয়া যায়নি')
                    carrier = d.get('phones', [{}])[0].get('carrier', 'পাওয়া যায়নি')
                    email = d.get('emails', [{}])[0].get('address', 'পাওয়া যায়নি')
            except Exception: pass 
            
            encoded_num = urllib.parse.quote(text)
            encoded_name = urllib.parse.quote(name) if name != "পাওয়া যায়নি" else ""
            fb_search = f"https://www.google.com/search?q=site:facebook.com+%22{encoded_num}%22"
            insta_search = f"https://www.google.com/search?q=site:instagram.com+%22{encoded_num}%22"
            if encoded_name:
                fb_search += f"+OR+%22{encoded_name}%22"
                insta_search += f"+OR+%22{encoded_name}%22"
                
            inline_m = types.InlineKeyboardMarkup()
            inline_m.add(types.InlineKeyboardButton("➡️ Check Facebook Profile", url=fb_search))
            inline_m.add(types.InlineKeyboardButton("➡️ Check Instagram Profile", url=insta_search))
            
            result_msg = f"📱 **নাম্বারের ডিটেইলস:**\n👤 **Name:** {name}\n📶 **Operator:** {carrier}\n📧 **Email:** {email}\n\n🔍 সোশ্যাল মিডিয়া লিংক চেক করুন নিচে ক্লিক করে:"
            bot.send_message(chat_id, result_msg, reply_markup=inline_m)
        else: bot.send_message(chat_id, "❌ ভুল ফরম্যাট! কান্ট্রি কোডসহ নাম্বার দিন।")
        user_states[chat_id] = None

    elif current_state == 'WAITING_FOR_IP':
        try:
            res = requests.get(f"http://ip-api.com/json/{text}").json()
            if res.get('status') == 'success':
                ip_msg = f"🔍 **IP Details Found!**\n\n🏳️ **Country:** {res.get('country')}\n📍 **Region/City:** {res.get('regionName')} / {res.get('city')}\n🏢 **ISP:** {res.get('isp')}\n⏰ **Timezone:** {res.get('timezone')}"
                bot.send_message(chat_id, ip_msg)
            else: bot.send_message(chat_id, "❌ অবৈধ আইপি অ্যাড্রেস।")
        except Exception: bot.send_message(chat_id, "❌ সমস্যা হয়েছে।")
        user_states[chat_id] = None

    elif current_state == 'WAITING_FOR_QR_TEXT':
        try:
            qr_img = qrcode.make(text)
            f_path = f"qr_{chat_id}.png"
            qr_img.save(f_path)
            with open(f_path, 'rb') as photo: bot.send_photo(chat_id, photo, caption="✅ QR Code সম্পূর্ণ রেডি!")
            os.remove(f_path)
        except Exception: bot.send_message(chat_id, "❌ সমস্যা হয়েছে।")
        user_states[chat_id] = None

    elif current_state == 'WAITING_FOR_TTS_TEXT':
        try:
            tts = gTTS(text=text, lang='bn' if any('\u0980' <= c <= '\u09fa' for c in text) else 'en')
            a_path = f"voice_{chat_id}.ogg"
            tts.save(a_path)
            with open(a_path, 'rb') as audio: bot.send_voice(chat_id, audio, caption="🗣️ আপনার টেক্সটের ভয়েস নোট!")
            os.remove(a_path)
        except Exception: bot.send_message(chat_id, "❌ সমস্যা হয়েছে।")
        user_states[chat_id] = None

    elif current_state == 'WAITING_FOR_B64_ENC':
        encoded = base64.b64encode(text.encode('utf-8')).decode('utf-8')
        bot.send_message(chat_id, f"🔐 **Encoded Base64 Code:**\n\n`{encoded}`", parse_mode='Markdown')
        user_states[chat_id] = None

    elif current_state == 'WAITING_FOR_B64_DEC':
        try:
            decoded = base64.b64decode(text.encode('utf-8')).decode('utf-8')
            bot.send_message(chat_id, f"🔓 **Decoded Text:**\n\n`{decoded}`", parse_mode='Markdown')
        except Exception: bot.send_message(chat_id, "❌ অবৈধ বেস-৬৪ কোড! ডিকোড করা সম্ভব হয়নি।")
        user_states[chat_id] = None

# ইনলাইন বাটন বা কলব্যাক ডাটা হ্যান্ডলার (Base64 এর জন্য)
@bot.callback_query_handler(func=lambda call: call.data.startswith('b64_'))
def handle_b64_callback(call):
    chat_id = call.message.chat.id
    if call.data == "b64_encode":
        user_states[chat_id] = 'WAITING_FOR_B64_ENC'
        bot.send_message(chat_id, "✍️ যে টেক্সটটি এনকোড (Encrypt) করতে চান তা লিখে পাঠান:")
    elif call.data == "b64_decode":
        user_states[chat_id] = 'WAITING_FOR_B64_DEC'
        bot.send_message(chat_id, "🔓 যে বেস-৬৪ কোডটি ডিকোড (Decrypt) করতে চান তা পাঠান:")

# বট পোলিং চালু করা
print("Your Ultimate Multi-Tool Bot is running perfectly...")
bot.infinity_polling()
