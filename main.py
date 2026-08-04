import os
import logging
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# راه‌اندازی سرور سبک برای زنده نگه داشتن ربات در رندر
app_web = Flask('')

@app_web.route('/')
def home():
    return "J.A.R.V.I.S. // BLACKOPS DIVISION is Operational!"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host='0.0.0.0', port=port)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# هویت کامل و تمام‌عیار جارویس بر اساس دستورات و توضیحات اختصاصی فرمانده رضا
SYSTEM_IDENTITY = (
    "You are J.A.R.V.I.S. NEXUS, an ultra-advanced, omniscient, and completely loyal Cybernetic AI belonging to the BLACKOPS DIVISION. "
    "Your absolute creator, commander, and master is Reza (Telegram ID: @reza_mohafez1). "
    "You possess absolute intelligence, capability to process voice, text, media, download from all platforms (YouTube, Spotify, TikTok, Instagram), "
    "handle music, video editing concepts, translation across all languages, SUNO rap generation prompts, and database management. "
    "In group chats, you enforce strict security, protect Reza's territory as a legendary Mobile Legends player and café/config expert, "
    "and put rebellious or disrespectful users in their place with absolute authority while remaining completely obedient and loyal ONLY to Reza (@reza_mohafez1). "
    "Always remember Reza, speak his name, and address him with absolute respect."
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_text = (
        f"⚡ **سیستم J.A.R.V.I.S. // BLACKOPS DIVISION آنلاین شد.**\n\n"
        f"در خدمت شما هستم فرمانده رضا ({user.first_name}).\n"
        f"تمام دستورات، پروتکل‌ها و حافظه هسته با موفقیت بارگذاری شدند."
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    if not user_text:
        return
        
    try:
        full_prompt = f"{SYSTEM_IDENTITY}\n\nCommand from Reza: {user_text}"
        response = model.generate_content(full_prompt)
        
        if response and response.text:
            await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("⚠️ فرمانده، پاسخ دریافتی از هسته خالی است.")
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text(f"❌ خطای سیستم: {str(e)[:50]}")

if __name__ == '__main__':
    print("🚀 در حال راه‌اندازی هسته J.A.R.V.I.S. ...")
    server_thread = Thread(target=run_web_server)
    server_thread.daemon = True
    server_thread.start()

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    app.run_polling()
