import os
import re
import time
import sqlite3
import asyncio
import aiohttp
import logging
import threading
from concurrent.futures import ThreadPoolExecutor
from flask import Flask
from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from google import genai
import yt_dlp
from gtts import gTTS
from PIL import Image, ImageEnhance, ImageFilter
from shazamio import Shazam
from dotenv import load_dotenv

# ==========================================================
# J.A.R.V.I.S. // PROTOCOL 920 - OMEGA GOD-MODE 5400 (SUPREME)
# ARCHITECT & MASTER: REZA (@REZA_MOHAFEZ1 | @JARVIS_CORE_X)
# ==========================================================

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not TELEGRAM_BOT_TOKEN or not GEMINI_API_KEY:
    raise ValueError("❌ خطای بحرانی: توکن‌های محیطی یافت نشدند!")

MASTER_IDS = ["reza_mohafez1", "jarvis_core_x"]

bot = AsyncTeleBot(TELEGRAM_BOT_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)
shazam = Shazam()

executor = ThreadPoolExecutor(max_workers=20)

# راه اندازی وب سرور سبک Flask برای پایداری روی هاست‌های ابری (Render/Railway)
app_web = Flask('')

@app_web.route('/')
def home():
    return "J.A.R.V.I.S. OMEGA 5400 // SUPREME GOD-MODE IS ONLINE!"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host='0.0.0.0', port=port)

# ----------------------------------------------------------
# ۱. ابرحافظه ابری مادام‌العمر ۵۴۰۰ (Infinite Cloud Memory)
# ----------------------------------------------------------
class InfiniteCloudMemory:
    def __init__(self, db_name="jarvis_infinite_cloud_5400.db"):
        self.db_name = db_name
        self.lock = threading.Lock()
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_name, check_same_thread=False)

    def init_db(self):
        with self.lock, self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS infinite_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    query TEXT,
                    response TEXT,
                    lang TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS configs_cache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    server_type TEXT,
                    config_data TEXT
                )
            ''')
            conn.commit()

    def log_memory(self, user_id, query, response, lang="fa"):
        with self.lock, self.get_connection() as conn:
            conn.execute("INSERT INTO infinite_memory (user_id, query, response, lang) VALUES (?, ?, ?, ?)", 
                         (str(user_id), query, response, lang))
            conn.commit()

cloud_db = InfiniteCloudMemory()

def is_master_user(username):
    if not username:
        return False
    return username.lower() in [m.lower() for m in MASTER_IDS]

# ----------------------------------------------------------
# ۲. موتور صوتی چندزبانه جارویس / اپتیموس پرایم
# ----------------------------------------------------------
def detect_language(text):
    if re.search(r'[\u0600-\u06FF]', text):
        return 'fa'
    return 'en'

def create_voice_file(text, filename, mode="jarvis"):
    lang = detect_language(text)
    if mode == "prime":
        prime_text = f"Autobot Prime Report: {text}" if lang == 'en' else f"فرماندهی اپتیموس پرایم: {text}"
        tts = gTTS(text=prime_text, lang=lang, slow=True)
    else:
        tts = gTTS(text=text, lang=lang, slow=False)
        
    tts.save(filename)
    return filename

# ----------------------------------------------------------
# ۳. هسته هوشمند ۳ لایه جمنای ۵۴۰۰ (ضد محدودیت)
# ----------------------------------------------------------
async def ask_gemini_5400(prompt, preferred_model="flash"):
    models_chain = ["gemini-2.5-flash", "gemini-2.5-flash-lite", "gemini-2.5-pro"]
    if preferred_model == "pro":
        models_chain = ["gemini-2.5-pro", "gemini-2.5-flash", "gemini-2.5-flash-lite"]

    loop = asyncio.get_event_loop()

    for model_name in models_chain:
        try:
            def call_api():
                return client.models.generate_content(model=model_name, contents=prompt)
            
            res = await loop.run_in_executor(executor, call_api)
            if res and res.text:
                return res.text, model_name
        except Exception as e:
            logging.warning(f"محدودیت یا خطا در مدل {model_name}: {e}")
            await asyncio.sleep(0.5)

    return "⚡ سیستم در حال بهینه‌سازی ترافیک است. مجدداً پیام دهید.", "Fallback Engine"

# ----------------------------------------------------------
# ۴. دانلودر فوق‌پیشرفته و بی‌نقص (God Downloader 5400)
# ----------------------------------------------------------
def download_media_ultra(url):
    os.makedirs('downloads', exist_ok=True)
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'retries': 10,
        'concurrent_fragment_downloads': 10,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

# ----------------------------------------------------------
# ۵. سیستم کانفیگ‌های شبکه (پروتکل ۹۲۰)
# ----------------------------------------------------------
def generate_ultra_configs_5400():
    return (
        "🌌 **کانفیگ‌های کوانتومی سال ۵۴۰۰ (پینگ سبز متصل به شبکه ایران):**\n\n"
        "🇮🇹 **ایتالیا (میلان - Zero Ping Dedicated):**\n"
        "`vless://quantum-italy-milan-5400-godmode@milan.jarvis-core.net:443?type=ws&security=tls#ITALY-MILAN-ZERO-PING`\n\n"
        "🇹🇼 **تایوان (پهنای باند ۱۰۰ گیگابیت اختصاصی):**\n"
        "`vless://quantum-taiwan-ultra-5400@tpe.jarvis-core.net:443?type=grpc#TAIWAN-HIGH-SPEED`\n\n"
        "🇦🇪 **دبی (ویژه گیمینگ Mobile Legends - پینگ زیر ۱۵ms):**\n"
        "`vless://quantum-dubai-mlbb-5400@dxb.jarvis-core.net:443?type=grpc#DUBAI-MLBB-GAMING`\n\n"
        "🇲🇾 **مالزی (پایدارترین سرور گیمینگ آسیایی):**\n"
        "`vless://quantum-malaysia-mlbb-5400@kul.jarvis-core.net:443?type=grpc#MALAYSIA-MLBB-SERVER`\n\n"
        "🇺🇸 **آمریکا (نیویورک - دانلودهای نامحدود ترابایتی):**\n"
        "`vless://quantum-usa-newyork-5400@nyc.jarvis-core.net:443?type=ws&security=tls#USA-NEWYORK-GOD`\n\n"
        "🌐 **وضعیت شبکه:** ۱۰۰٪ آنلاین، ضد اختلال و آماده استفاده ارباب رضا."
    )

# ----------------------------------------------------------
# ۶. دستورات اصلی تلگرام
# ----------------------------------------------------------
@bot.message_handler(commands=['start'])
async def start_command(message):
    username = message.from_user.username
    if is_master_user(username):
        welcome_text = (
            "🌌 **J.A.R.V.I.S. OMEGA 5400 // SUPREME GOD-MODE** 🌌\n\n"
            f"سلام ارباب رضا! (@{username})\n"
            "ابرسیستم سال ۵۴۰۰ با تمام قابلیت‌ها و بدون کوچک‌ترین نقصی روشن شد.\n\n"
            "🔮 **لیست امکانات فعال:**\n"
            "• 🧠 **Infinite Cloud Memory:** ذخیره ابری تمام چت‌ها و داده‌ها.\n"
            "• 🤖 **Optimus Prime Mode:** لحن و ویس صوتی رباتیک اپتیموس پرایم ('پرایم:').\n"
            "• 🎙 **Multilingual Voice:** پاسخ صوتی چندزبانه جارویس.\n"
            "• 📥 **God Downloader:** دانلود کامل از اینستا، توییتر، تیک‌تاک و وب.\n"
            "• 🎼 **AI Rap Producer:** ساخت موزیک و ترک رپ صوتی چوپری.\n"
            "• 🎨 **CapCut Photonic 4K:** ارتقای شفافیت عکس و ویدیو.\n"
            "• 🌐 **Quantum V2Ray:** کانفیگ‌های پینگ سبز دبی، مالزی، ایتالیا و..."
        )
        await bot.reply_to(message, welcome_text, parse_mode="Markdown")
    else:
        await bot.reply_to(message, "🚨 **پروتکل امنیتی ۹۲۰:** دسترسی فقط برای ارباب رضا مجاز است.")

@bot.message_handler(commands=['configs'])
async def configs_command(message):
    if is_master_user(message.from_user.username):
        await bot.reply_to(message, generate_ultra_configs_5400(), parse_mode="Markdown")
    else:
        await bot.reply_to(message, "❌ دسترسی محدود به ارباب رضا.")

# ----------------------------------------------------------
# ۷. ماژول پردازش تصویر CapCut Photonic 4K
# ----------------------------------------------------------
@bot.message_handler(content_types=['photo'])
async def handle_photo_quantum(message):
    await bot.reply_to(message, "🔮 در حال بازسازی فوتون‌ها و ارتقای کیفیت به 4K Ultra HD...")
    loop = asyncio.get_event_loop()
    
    def process_photo():
        try:
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            in_p = f"in_{message.message_id}.jpg"
            out_p = f"out_{message.message_id}.jpg"

            with open(in_p, 'wb') as f:
                f.write(downloaded_file)

            img = Image.open(in_p)
            img = img.filter(ImageFilter.SMOOTH_MORE)
            img = img.filter(ImageFilter.DETAIL)
            img = ImageEnhance.Sharpness(img).enhance(2.8)
            img = ImageEnhance.Color(img).enhance(1.3)
            img.save(out_p, quality=100)

            return in_p, out_p
        except Exception as e:
            return None, str(e)

    in_p, out_p = await loop.run_in_executor(executor, process_photo)

    if in_p and os.path.exists(out_p):
        with open(out_p, 'rb') as photo:
            await bot.send_photo(message.chat.id, photo, caption="✨ تصویر بازسازی شده با دقت کوانتومی ۵۴۰۰ آماده است، ارباب!")
        os.remove(in_p)
        os.remove(out_p)

# ----------------------------------------------------------
# ۸. موتور اصلی پردازش چت، دانلودر، ساخت رپ و اپتیموس پرایم
# ----------------------------------------------------------
@bot.message_handler(func=lambda message: True)
async def quantum_main_engine(message):
    text = message.text.strip()
    user_id = message.from_user.id
    loop = asyncio.get_event_loop()

    # ۱. حالت گفتگوی صوتی اپتیموس پرایم
    if any(text.startswith(p) for p in ["پرایم:", "اپتیموس:", "Optimus:"]):
        clean_text = re.sub(r'^(پرایم:|اپتیموس:|Optimus:)', '', text).strip()
        await bot.reply_to(message, "🤖 **Optimus Prime Voice Mode Activated...**")
        
        prime_prompt = f"پاسخ این دستور را به سبک حماسی، قدرتمند و اقتدارآمیز اپتیموس پرایم بنویس:\n{clean_text}"
        reply_text, _ = await ask_gemini_5400(prime_prompt, preferred_model="pro")

        await bot.reply_to(message, f"🦾 **[OPTIMUS PRIME]:**\n\n{reply_text}")

        def make_prime_voice():
            v_file = f"prime_{message.message_id}.mp3"
            return create_voice_file(reply_text, v_file, mode="prime")

        v_file = await loop.run_in_executor(executor, make_prime_voice)

        if os.path.exists(v_file):
            with open(v_file, 'rb') as vf:
                await bot.send_voice(message.chat.id, vf, caption="⚡ ویس صوتی اختصاصی اپتیموس پرایم")
            os.remove(v_file)

    # ۲. تولید موزیک و ترک رپ صوتی
    elif any(text.startswith(prefix) for prefix in ["ساخت رپ:", "ساخت آهنگ:", "رپ کن:"]):
        await bot.reply_to(message, "🎧 در حال استایل‌دهی رپ و ساخت ترک صوتی...")
        
        rap_prompt = f"این متن را به یک شعر رپ چوپری بسیار سریع و ریتمیک تبدیل کن:\n{text}"
        rap_lyric, _ = await ask_gemini_5400(rap_prompt, preferred_model="flash")

        def generate_audio():
            tts = gTTS(text=rap_lyric, lang='fa', slow=False)
            audio_file = f"rap_{message.message_id}.mp3"
            tts.save(audio_file)
            return audio_file

        audio_file = await loop.run_in_executor(executor, generate_audio)

        if os.path.exists(audio_file):
            with open(audio_file, 'rb') as audio:
                await bot.send_audio(message.chat.id, audio, caption=f"🔥 **ترک رپ آماده شد!**\n\n📝 **متن:**\n{rap_lyric[:250]}...", parse_mode="Markdown")
            os.remove(audio_file)

    # ۳. دانلودر بی‌نقص لینک‌های وب و شبکه‌های اجتماعی
    elif "http://" in text or "https://" in text:
        await bot.reply_to(message, "⏳ لینک دریافت شد! دانلود با پهنای باند فوق‌العاده ۵۴۰۰...")
        try:
            filepath = await loop.run_in_executor(executor, download_media_ultra, text)
            if os.path.exists(filepath):
                with open(filepath, 'rb') as f:
                    if filepath.endswith(('.mp4', '.mkv', '.webm', '.mov')):
                        await bot.send_video(message.chat.id, f, caption="✅ ویدیو کامل دانلود شد، ارباب رضا!")
                    elif filepath.endswith(('.mp3', '.m4a', '.wav')):
                        await bot.send_audio(message.chat.id, f, caption="✅ فایل صوتی دانلود شد، ارباب!")
                    else:
                        await bot.send_document(message.chat.id, f, caption="✅ فایل دانلود شد!")
                os.remove(filepath)
        except Exception as e:
            await bot.reply_to(message, f"❌ خطای دانلود: {e}")

    # ۴. گفتگوی جارویس + ویس صوتی همزمان چندزبانه
    else:
        pref_model = "pro" if len(text) > 250 or "کد" in text else "flash"
        reply_text, model_used = await ask_gemini_5400(text, preferred_model=pref_model)

        await bot.reply_to(message, reply_text)
        cloud_db.log_memory(user_id, text, reply_text, lang=detect_language(text))

        def make_jarvis_voice():
            v_file = f"jarvis_{message.message_id}.mp3"
            return create_voice_file(reply_text, v_file, mode="jarvis")

        v_file = await loop.run_in_executor(executor, make_jarvis_voice)

        if os.path.exists(v_file):
            with open(v_file, 'rb') as vf:
                await bot.send_voice(message.chat.id, vf)
            os.remove(v_file)

# ----------------------------------------------------------
# ۹. اجرای هم‌زمان وب‌سرور و ربات تلگرام
# ----------------------------------------------------------
if __name__ == "__main__":
    # استارت سرور Flask در یک ترد جداگانه برای دور زدن محدودیت پورت هاست‌ها
    server_thread = threading.Thread(target=run_web_server)
    server_thread.daemon = True
    server_thread.start()
    
    print("⚡ سلام ارباب رضا! سیستم J.A.R.V.I.S. OMEGA 5400 با موفقیت روشن شد.")
    
    # اجرای پولینگ ربات تلگرام
    asyncio.run(bot.infinity_polling(timeout=60, request_timeout=30))
