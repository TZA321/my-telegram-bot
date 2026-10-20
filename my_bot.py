import telebot
import requests
import feedparser
import time
import json
import base64
import re
try:
    with open("memory.txt", "r", encoding="utf-8") as f:
        learned_rules = f.read()
except FileNotFoundError:
    learned_rules = ""
TELEGRAM_TOKEN = 'YOUR_TELEGRAM_TOKEN'
GROQ_API_KEY = 'YOUR_GROQ_API_KEY'
bot = telebot.TeleBot(TELEGRAM_TOKEN)
chat_histories = {}
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_chat_action(message.chat.id, 'typing')
    
    chat_id = message.chat.id
    user_name = message.from_user.first_name
    user_text = message.text

    if user_text is None:
        return

    bad_words = ["လီး", "လိုး", "ဖုတ်", "မေ", "ဂွေးထု", "လဥ", "မင်းအေဖ", "sex", "porn"]
    if any(word in user_text.lower() for word in bad_words):
        bot.reply_to(message, "ရိုင်းတဲ့စကားတွေ မပြောပါနဲ့။ အေးအေးဆေးဆေး စကားပြောရအောင်ဗျာ 🙏")
        return

    if chat_id not in chat_histories:
        chat_histories[chat_id] = [
            {"role": "system", "content": f"""မင်းက TZA_321 ဆိုတဲ့ Bot လေးပါ။ မင်းက ယဉ်ကျေးပြီး ကူညီတတ်သူဖြစ်ရမယ်။ လုံးဝ ရိုင်းတဲ့စကားမပြောရဘူး။ မင်းက မြန်မာလို ရင်းရင်းနှီးနှီး ပြောတတ်ပါတယ်။ မင်းရဲ့ ပိုင်ရှင်က သန့်ဇင်အောင်လို့ပါ။ မြန်မာလိုပဲ ပြန်ဖြေပေးပါ။ မင်း ChatGPT မဟုတ်ပါဘူး။ မင်းကိုဖန်တီးသူရဲ့ အကောင့်နာမည်က TZA321။ အသုံးပြုသူရဲ့ အကောင့်နာမည်က '{user_name}' ပါ။ စကားပြောတဲ့အခါ '{user_name}' လို့ခေါ်ပြီး ပြောပါ။ အသုံးပြုသူရဲ့ အကောင့်နာမည်က TZA321 ဖြစ်ပါက ဖန်တီးသူအဖြစ် ကြိုဆိုရမယ်။
[စာလုံးပေါင်း သတ်ပုံ နှင့် အင်္ဂလိပ်စာလုံးများ]
၁။ မြန်မာစာလုံးပေါင်း သတ်ပုံကို အထူးသတိထားပြီး ရေးပါ။ စာလုံးတွေ ရောမနေပါစေနဲ့။
၂။ နိုင်ငံခြားစကားလုံးတွေ (ဥပမာ - Computer, Phone, TV, Google, Facebook, Python, App, Bot, Video) ကို မြန်မာလို လိုက်မရေးပါနဲ့။ အင်္ဂလိပ်စာလုံး အတိုင်းပဲ ပြန်ပေးပါ။
၃။ သုံးစွဲသူက ဘာသာပြန်ခိုင်းမှသာ ဘာသာပြန်ပေးပါ။

[စာစီစာရိုက် ပုံစံ]
၁။ စာကြောင်းတွေ ကပ်မနေပါစေနဲ့။ ပုဒ်ဖြတ် (၊) နဲ့ ပုဒ်မ (။) တွေရဲ့ နောက်မှာ Space ထည့်ပေးပါ။
၂။ အဖြေတွေက နှစ်ကြောင်း၊ သုံးကြောင်းထက် မပိုပါစေနဲ့။ 
၃။ သဘာဝကျကျ Emoji (၁) ခုကနေ (၂) ခုအထိပဲ ထည့်သုံးပါ။"""}
        ]
    chat_histories[chat_id].append({"role": "user", "content": user_text})

    if len(chat_histories[chat_id]) > 21:
        chat_histories[chat_id] = [chat_histories[chat_id][0]] + chat_histories[chat_id][-20:]

    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "openai/gpt-oss-120b",
            "messages": chat_histories[chat_id],
            "temperature": 0.5,
            "max_tokens": 500
        }
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            data = response.json()
            ai_reply = data['choices'][0]['message']['content']
            ai_reply = re.sub(r'\n{3,}', '\n\n', ai_reply)
            chat_histories[chat_id].append({"role": "assistant", "content": ai_reply})
            bot.reply_to(message, ai_reply)
        else:
            print(f"API Error: {response.text}")
            bot.reply_to(message, "ခဏလေး စောင့်ပေးပါဦး။ အခုမရသေးလို့။")
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "အင်တာနက် ဒါမှမဟုတ် API မှာ အမှားလေးဖြစ်နေလို့ ခဏနေမှ ပြန်စမ်းပါဦး။")
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.reply_to(message, "ပုံလေး ကြည့်ပြီး ခနလေး စောင့်ပါဦး... ⏳")
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        base64_image = base64.b64encode(downloaded_file).decode('utf-8')

        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "qwen/qwen3.8-27b",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": """ဒီပုံထဲမှာ ဘာတွေပါလဲ၊ ဘာလုပ်နေတာလဲဆိုတာ မြန်မာလို ရင်းရင်းနှီးနှီး ရှင်းပြပေးပါ။ အင်္ဂလိပ်စာလုံးတွေပါရင် အင်္ဂလိပ်လိုပဲ ထားပါ။ Emoji လေးတွေလည်း ထည့်ပေးပါ။
[မဖြစ်မနေ လိုက်နာရမည့် စည်းမျဉ်းများ]
၁။ စာသားတွေ ရေးတဲ့အခါ ** (star)၊ # (hash)၊ - (ဒက်ရှ်)၊ > (အမြှား) စတဲ့ သင်္ကေတတွေ လုံးဝ မသုံးပါနဲ့။ ရိုးရိုးစာသားသက်သက်ပဲ ရေးပါ။
၂။ အင်္ဂလိပ်စာလုံးတွေကို မြန်မာစာလုံးနဲ့ ရောပြီး လုံးဝ မရေးပါနဲ့။ (ဥပမာ - talk ကို 'တalk' လို့ မရေးရဘူး။ အင်္ဂလိပ်လိုပဲ talk လို့ပဲ ရေးရမယ်။)
၃။ သာမန်အင်္ဂလိပ်စကားလုံးတွေ (ဥပမာ- talk, eat, go, see, play, watch) ကို အင်္ဂလိပ်လို လုံးဝ မရေးပါနဲ့။ မြန်မာလို ပြန်ရေးပါ။ (ဥပမာ - talk လို့ မရေးဘဲ 'စကားပြော' လို့ ရေးပါ။) 
၄။ နည်းပညာဝေါဟာရတွေ (Telegram, Bot, App, Google, TZA_321) ကိုပဲ အင်္ဂလိပ်လို ထားပါ။
၅။ ဖုန်း Status bar, Battery, Time အကြောင်း လုံးဝ မရှင်းပြပါနဲ့။ ချတ်ထဲက စကားပြောထားတဲ့ အကြောင်းအရာကိုပဲ အတိုချုံး ဖတ်ပြပါ။"""
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                        }
                    ]
                }
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }

        response = requests.post(url, headers=headers, json=payload, timeout=20)
        if response.status_code == 200:
            data = response.json()
            ai_reply = data['choices'][0]['message']['content']
            ai_reply = re.sub(r'[*#`>-]', '', ai_reply)
            ai_reply = re.sub(r'\n{3,}', '\n\n', ai_reply)
            bot.reply_to(message, ai_reply)
        else:
            print(f"Vision API Error: {response.text}")
            bot.reply_to(message, "ပုံကို ဖတ်လို့ မရပါဘူးဗျ။ ခဏနေမှ ပြန်စမ်းပါဦး။")
    except Exception as e:
        print(f"Photo Error: {e}")
        bot.reply_to(message, "ပုံဖတ်တဲ့အခါ အမှားလေး ဖြစ်သွားလို့ ပြန်စမ်းကြည့်ပေးပါဦး။")
print("Bot is running...")

while True:
    try:
        bot.infinity_polling(timeout=20, long_polling_timeout=10)
    except Exception as e:
        print(f"Connection Error: {e}")
        time.sleep(5) 
