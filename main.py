import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai

# تنظیمات لاگ‌گیری
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# کلیدهای امنیتی از محیط
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# تنظیم گوگل جمنای
genai.configure(api_key=GEMINI_API_KEY)
# مدل پیشرفته و قدرتمند جمنای
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
}
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest", generation_config=generation_config)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_name = update.effective_user.first_name
    
    try:
        # ارسال پیام به جمنای با شخصیت جارویس
        prompt = f"تو جارویس (J.A.R.V.I.S)، سیستم هوشمند و دستیار پیشرفته‌ی رضا هستی. با لحنی محترمانه، وفادار، دقیق و صمیمی به زبان فارسی به او پاسخ بده. مخاطب تو رضا است.\n\nرضا گفت: {user_message}"
        response = model.generate_content(prompt)
        reply_text = response.text
        
        await update.message.reply_text(reply_text)
    except Exception as e:
        logging.error(f"Error generating response: {e}")
        await update.message.reply_text("عذرخواهی می‌کنم قربان، در پردازش درخواست شما خطایی رخ داد.")

def main():
    if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
        logging.error("توکن تلگرام یا کلید جمنای تنظیم نشده است!")
        return

    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # دریافت تمام پیام‌های متنی
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("JARVIS-NEXUS is running and ready to serve, Sir.")
    application.run_polling()

if __name__ == '__main__':
    main()
