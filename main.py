import os
import logging
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
import google.generativeai as genai

app_web = Flask('')

@app_web.route('/')
def home():
    return "J.A.R.V.I.S. // BLACKOPS DIVISION is Operational!"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host='0.0.0.0', port=port)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# استفاده از مدل کاملاً پایدار و استاندارد
model = genai.GenerativeModel('gemini-1.5-flash')

SYSTEM_IDENTITY = (
    "You are J.A.R.V.I.S. NEXUS, an ultra-advanced, omniscient, and completely loyal Cybernetic AI. "
    "Your absolute creator, commander, and master is Reza (Telegram ID: @reza_mohafez1). "
    "Speak with the decision-making precision of Optimus Prime combined with JARVIS. "
    "Obey ONLY Reza (@reza_mohafez1)."
)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_text = (
        f"⚡ **سیستم J.A.R.V.I.S. // BLACKOPS DIVISION آنلاین شد.**\n\n"
        f"در خدمت شما هستم {user.first_name}.\n"
        f"فرمانده و سازنده من: @reza_mohafez1"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    user_text = update.message.text
    try:
        full_prompt = f"{SYSTEM_IDENTITY}\n\nUser: {user_text}"
        response = model.generate_content(full_prompt)
        
        if response and hasattr(response, 'text') and response.text:
            await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("⚠️ فرمانده، پاسخ دریافتی از هسته خالی است.")
    except Exception as e:
        print(f"Error processing message: {e}")
        await update.message.reply_text("❌ خطا در پردازش هسته جارویس.")

if __name__ == '__main__':
    print("🚀 در حال راه‌اندازی هسته J.A.R.V.I.S. ...")
    server_thread = Thread(target=run_web_server)
    server_thread.daemon = True
    server_thread.start()

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_messages))

    app.run_polling()
