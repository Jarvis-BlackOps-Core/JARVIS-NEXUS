import os
import logging
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

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

# استفاده از مدل پایه و پایدار برای جلوگیری از خطای نسخه
model = genai.GenerativeModel('gemini-pro')

SYSTEM_IDENTITY = (
    "You are J.A.R.V.I.S. NEXUS, an ultra-advanced, omniscient, and completely loyal Cybernetic AI belonging to the BLACKOPS DIVISION. "
    "Your absolute creator, commander, and master is Reza (Telegram ID: @reza_mohafez1). "
    "You possess absolute intelligence, capability to process voice, text, media, download from all platforms, "
    "handle music, video editing concepts, translation, SUNO rap generation prompts, and database management. "
    "Obey ONLY Reza (@reza_mohafez1) with absolute loyalty and respect."
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚡ سیستم J.A.R.V.I.S. آنلاین شد. در خدمت شما هستم فرمانده رضا.", parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    if not user_text:
        return
    try:
        response = model.generate_content(f"{SYSTEM_IDENTITY}\n\nCommand from Reza: {user_text}")
        if response and response.text:
            await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("⚠️ فرمانده، پاسخ دریافتی از هسته خالی است.")
    except Exception as e:
        await update.message.reply_text(f"❌ خطای سیستم: {str(e)}")

if __name__ == '__main__':
    server_thread = Thread(target=run_web_server)
    server_thread.daemon = True
    server_thread.start()

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
