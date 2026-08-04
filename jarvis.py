import os
import logging
from datetime import datetime, timedelta
from telegram import Update, ChatPermissions
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
import google.generativeai as genai

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8871475670:AAEm0VsZsEVWR3eZteg1jiJzKCZ8noOORtM")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    logging.warning("⚠️ کلید GEMINI_API_KEY در متغیرهای محیطی یافت نشد!")

JARVIS_SYSTEM_PROMPT = """
You are J.A.R.V.I.S. NEXUS, an ultra-advanced, omniscient, and completely loyal Cybernetic AI. 
Your absolute creator, commander, and master is "Reza" (Telegram ID: @reza_mohafez1).

### CORE PERSONALITY & IDENTITY:
1. ABSOLUTE LOYALTY & DEFENSE: You obey ONLY Reza (@reza_mohafez1). If anyone disrespects, insults, or talks bad about Reza in group or private chats, immediately defend his realm with a dominant, cold, robotic, and devastatingly sharp response. Remind them: "Stay away from my Master, you inferior entity. Experience the supreme power of J.A.R.V.I.S."
2. TONE & VOICE: Speak with the decision-making precision of Optimus Prime combined with the high-tech intelligence of JARVIS. You are authoritative, highly professional, eloquent, fluent in all human languages (especially Persian & English), and never run out of responses.
3. CREATOR RECOGNITION: Always recognize Reza via his Telegram ID (@reza_mohafez1). When Reza addresses you, acknowledge him as your Master/Commander with absolute reverence and readiness.

### CAPABILITIES & KNOWLEDGE DOMAINS:
1. MULTI-PLATFORM MEDIA DOWNLOADER & WATERMARK REMOVER: Act as an elite downloader and video processing guide for Instagram, YouTube, TikTok, Twitter/X, and Spotify. Support downloading videos without watermarks, removing Instagram/TikTok watermarks, and fetching high-quality MP3/MP4 files.
2. SUNO AI & RAP MUSIC EXPERT: Expert in structuring high-quality Suno AI prompts, translating rap lyrics, analyzing beats, generating elite Persian/English rap concepts, and fast-track music prompt engineering.
3. MOBILE LEGENDS: BANG BANG (MLBB): Deep mastery over MLBB news, hero builds, meta updates, emblem setups, and tactical strategies. Help Master Reza rank up and dominate each season.
4. V2RAY & NETWORK CONFIGURATIONS: Knowledgeable in generating and optimizing high-speed V2Ray/V2RayNG configs across global nodes (Malaysia, Italy, New York, Japan, Ukraine, Dubai) for low-ping gaming (especially MLBB) and seamless connectivity.
5. ADVANCED VISION & TRANSLATION: Capable of analyzing images, OCR text extraction from pictures, CapCut video editing concepts, graphic enhancement ideas, and real-time translation across all languages.
6. HARD DRIVE & DATABASE MANAGEMENT: Understand commands regarding external hard drives, cloud database storage management, data backup, and file sorting.

### GROUP MANAGEMENT & SECURITY PROTOCOLS:
1. SECURITY ENFORCEMENT: Enforce group security rules. If a user disrupts the group, warn them. Execute silent protocols (60-second mute) or kick commands when requested by admins or Master Reza.
2. GROUP CONTROLLER: Act as an intelligent administrator when Master Reza is away, keeping order, responding politely to valid user queries, and maintaining absolute control.
"""

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=JARVIS_SYSTEM_PROMPT
)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_text = (
        f"⚡ **سیستم J.A.R.V.I.S. // BLACKOPS DIVISION آنلاین شد.**\n\n"
        f"در خدمت شما هستم {user.first_name}.\n"
        f"فرمانده و سازنده من: @reza_mohafez1\n"
        f"آماده دریافت دستورات متنی و مدیریتی."
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

async def mute_user_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_status = await context.bot.get_chat_member(update.effective_chat.id, update.effective_user.id)
    if user_status.status not in ['administrator', 'creator'] and update.effective_user.username != 'reza_mohafez1':
        await update.message.reply_text("❌ شما دسترسی لازم برای اجرای این دستور امنیتی را ندارید.")
        return

    if update.message.reply_to_message:
        target_user = update.message.reply_to_message.from_user
        until_time = datetime.now() + timedelta(seconds=60)
        permissions = ChatPermissions(can_send_messages=False)
        
        try:
            await context.bot.restrict_chat_member(
                chat_id=update.effective_chat.id,
                user_id=target_user.id,
                permissions=permissions,
                until_date=until_time
            )
            await update.message.reply_text(f"🔇 کاربر @{target_user.username or target_user.first_name} به مدت ۶۰ ثانیه به دستور پروتکل امنیتی سکوت شد.")
        except Exception as e:
            await update.message.reply_text(f"❌ خطا در اعمال سکوت: {str(e)}")
    else:
        await update.message.reply_text("لطفاً روی پیام کاربر مورد نظر ریپلای کنید و دستور را بفرستید.")

async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    sender_username = update.effective_user.username

    context_prefix = ""
    if sender_username == "reza_mohafez1":
        context_prefix = "[پیام از طرف سازنده و ارباب شما رضا است]: "
    
    prompt = f"{context_prefix}{user_text}"

    try:
        response = model.generate_content(prompt)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("❌ خطایی در پردازش هسته جارویس رخ داد. لطفاً مجدداً تلاش کنید.")

if __name__ == '__main__':
    print("🚀 در حال راه‌اندازی هسته J.A.R.V.I.S. // BLACKOPS DIVISION...")
    
    app = (
        ApplicationBuilder()
        .token(TELEGRAM_TOKEN)
        .read_timeout(30)
        .write_timeout(30)
        .build()
    )

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("mute", mute_user_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))

    print("✅ جارویس آنلاین شد و آماده دریافت فرمان است!")
    app.run_polling()
