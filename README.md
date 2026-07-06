# Deploy Steps

1. এই ফোল্ডারের ফাইলগুলো GitHub repo তে push করুন (bot.py, requirements.txt, Procfile).
2. Render.com এ যান → New → **Background Worker** (Web Service না, কারণ এটা polling bot).
3. Repo connect করুন।
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `python bot.py`
6. Environment → Environment Variables এ যোগ করুন:
   - Key: `BOT_TOKEN`
   - Value: আপনার BotFather থেকে পাওয়া টোকেন
7. Deploy করুন।

BOT_TOKEN কখনো কোডে/GitHub এ hardcode করবেন না, শুধু Render এর Environment Variable এ রাখুন।
