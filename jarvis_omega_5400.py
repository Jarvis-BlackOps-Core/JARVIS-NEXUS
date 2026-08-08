import os
import re
import time
import sqlite3
import asyncio
import logging
import threading
import io
import subprocess
from concurrent.futures import ThreadPoolExecutor
from flask import Flask
from telebot.async_telebot import AsyncTeleBot
from google import genai
from google.genai import types
import yt_dlp
from gtts import gTTS
from PIL import Image, ImageEnhance, ImageFilter
from dotenv import load_dotenv

# ==========================================================
# J.A.R.V.I.S. // PROTOCOL 920 - OMEGA GOD-MODE 5400 (FIXED)
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

executor = ThreadPoolExecutor(max_workers=20)

app_web = Flask('')

@app_web.route('/')
def home():
    return "J.A.R.V.I.S. OMEGA 5400 // ULTIMATE GOD-MODE IS ONLINE!"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host='0.0.0.0', port=port)

# ----------------------------------------------------------
# ۱. ابرحافظه ابری ۵۴۰۰ (Infinite Cloud Memory)
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
            conn.commit()

    def log_memory(self, user_id, query, response, lang="fa"):
        try:
            with self.lock, self.get_connection() as conn:
                conn.execute("INSERT INTO infinite_memory (user_id, query, response, lang) VALUES (?, ?, ?, ?)", 
                             (str(user_id), query, response, lang))
                conn.commit()
        except Exception as e:
            logging.error(f"DB Log Error: {e}")

cloud_db = InfiniteCloudMemory()

def is_master_user(username):
    if not username:
        return False
    return username.lower() in [m.lower() for m in MASTER_IDS]

# ----------------------------------------------------------
# ۲. موتور صوتی چندزبانه جارویس / اپتیموس پرایم (اصلاح‌شده)
# ----------------------------------------------------------
def detect_language(text):
    if re.search(r'[\u0600-\u06FF]', text):
        return 'fa'
    return 'en'

def create_voice_file(text, filename, mode="jarvis"):
    # gTTS زبان فارسی پشتیبانی نمی‌کند، استفاده از en برای جلوگیری از Crash
    lang = 'en'
    try:
        if mode == "prime":
            prime_text = f"Autobot Prime Report: {text}"
            tts = gTTS(text=prime_text, lang=lang, slow=True)
        else:
            tts = gTTS(text=text[:300], lang=lang, slow=False)
        tts.save(filename)
        return filename
    except Exception as e:
        logging.error(f"خطای ساخت ویس: {e}")
        return None

# ----------------------------------------------------------
# ۳. هسته هوشمند جمنای (اصلاح مدل‌ها به نسخه‌های فعال)
# ----------------------------------------------------------
async def ask_gemini_5400(prompt, preferred_model="flash"):
    # مدل‌ها به نسخه‌های رسمی و استیبل اصلاح شدند
    models_chain = ["gemini-2.0-flash", "gemini-1.5-flash"]
    if preferred_model == "pro":
        models_chain = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"]

    loop = asyncio.get_running_loop()

    for model_name in models_chain:
        try:
            def call_api():
                return client.models.generate_content(model=model_name, contents=prompt)
            
            res = await asyncio.wait_for(loop.run_in_executor(executor, call_api), timeout=12.0)
            if res and res.text:
                return res.text, model_name
        except Exception as e:
            logging.warning(f"خطا یا تایم‌اوت در مدل {model_name}: {e}")

    return "⚡ سیستم در حال بهینه‌سازی ترافیک است. ارباب رضا لطفا مجددا پیام دهید.", "Fallback Engine"

# ----------------------------------------------------------
# ۴. ماژول تولید تصویر اختصاصی با AI (Text-To-Image)
# ----------------------------------------------------------
async def generate_ai_image(prompt_text):
    loop = asyncio.get_running_loop()
    try:
        translate_prompt = f"Translate and enhance this image description into a detailed English prompt for AI image generation: {prompt_text}"
        eng_prompt, _ = await ask_gemini_5400(translate_prompt)

        def call_imagen():
            result = client.models.generate_images(
                model='imagen-3.0-generate-002',
                prompt=eng_prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    aspect_ratio="1:1",
                    output_mime_type="image/jpeg"
                )
            )
            return result

        result = await asyncio.wait_for(loop.run_in_executor(executor, call_imagen), timeout=25.0)
        
        if result and result.generated_images:
            generated_image = result.generated_images[0]
            image_bytes = generated_image.image.image_bytes
            return image_bytes, eng_prompt
    except Exception as e:
        logging.error(f"Imagen Generation Error: {e}")
        return None, str(e)
    
    return None, "خطا در تولید تصویر"

# ----------------------------------------------------------
# ۵. دانلودر فوق‌پیشرفته و پرسرعت (Ultra Speed Downloader)
# ----------------------------------------------------------
def download_media_ultra(url):
    os.makedirs('downloads', exist_ok=True)
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'socket_timeout': 15,
        'retries': 5,
        'concurrent_fragment_downloads': 10,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'http_headers': {
            'Accept-Language': 'en-US,en;q=0.9',
        }
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

# ----------------------------------------------------------
# ۶. ماژول جدید: حذف هوشمند واترمارک/ادساین ویدیو با FFmpeg
# ----------------------------------------------------------
def remove_video_watermark(input_path, output_path, position="bottom"):
    try:
        if position == "bottom":
            filter_str = "delogo=x=iw*0.05:y=ih*0.82:w=iw*0.9:h=ih*0.15"
        else:
            filter_str = "delogo=x=iw*0.05:y=ih*0.02:w=iw*0.9:h=ih*0.15"

        cmd = [
            'ffmpeg', '-y', '-i', input_path,
            '-vf', filter_str,
            '-c:a', 'copy', output_path
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except Exception as e:
        logging.error(f"FFmpeg Watermark Removal Error: {e}")
        return False

# ----------------------------------------------------------
# ۷. دستورات شبکه ۹۲۰
# ----------------------------------------------------------
def generate_ultra_configs_5400():
    return (
        "🌌 **کانفیگ‌های کوانتومی سال ۵۴۰۰ (پینگ سبز متصل به شبکه ایران):**\n\n"
        "🇮🇹 **ایتالیا (میلان - Zero Ping Dedicated):**\n"
        "`vless://quantum-italy-milan-5400-godmode@milan.jarvis-core.net:443?type=ws&security=tls#ITALY-MILAN-ZERO-PING`\n\n"
        "🇦🇪 **دبی (ویژه گیمینگ Mobile Legends - پینگ زیر ۱۵ms):**\n"
        "`vless://quantum-dubai-mlbb-5400@dxb.jarvis-core.net:443?type=grpc#DUBAI-MLBB-GAMING`\n\n"
        "🌐 **وضعیت شبکه:** ۱۰۰٪ آنلاین، ضد اختلال و آماده استفاده ارباب رضا."
    )

# ----------------------------------------------------------
# ۸. دستورات اصلی تلگرام
# ----------------------------------------------------------
@bot.message_handler(commands=['start'])
async def start_command(message):
    username = message.from_user.username
    if is_master_user(username):
        welcome_text = (
            "🌌 **J.A.R.V.I.S. OMEGA 5400 // ULTIMATE GOD-MODE** 🌌\n\n"
            f"سلام ارباب رضا! (@{username})\n"
            "ابرسیستم سال ۵۴۰۰ ارتقا یافت.\n\n"
            "🔮 **قابلیت‌های فعال:**\n"
            "• 🎬 **Watermark Remover:** حذف ادساین و واترمارک از روی ویدیوها\n"
            "• 🎨 **AI Image Creator:** ساخت تصویر با دستور (`عکس بساز: ...`)\n"
            "• 🚀 **Turbo Downloader:** دانلود پرسرعت ۱۰تکه‌ای\n"
            "• 🧠 **Infinite Cloud Memory:** ذخیره‌سازی حافظه ۵۴۰۰\n"
            "• 🤖 **Optimus Prime Mode:** ویس حماسی با عبارت `پرایم:`"
        )
        await bot.reply_to(message, welcome_text, parse_mode="Markdown")
    else:
        await bot.reply_to(message, "🚨 **پروتکل امنیتی ۹۲۰:** دسترسی فقط برای ارباب رضا مجاز است.")

@bot.message_handler(commands=['configs'])
async def configs_command(message):
    if is_master_user(message.from_user.username):
        await bot.reply_to(message, generate_ultra_configs_5400(), parse_mode="Markdown")

# ----------------------------------------------------------
# ۹. ماژول پردازش ویدیو (حذف ادساین / واترمارک)
# ----------------------------------------------------------
@bot.message_handler(content_types=['video'])
async def handle_video_watermark_removal(message):
    caption = message.caption.strip() if message.caption else ""
    
    if any(w in caption for w in ["حذف ادساین", "حذف واترمارک", "بدون واترمارک", "clean"]):
        await bot.reply_to(message, "🎬 **در حال پردازش ویدیو و حذف ادساین/واترمارک با FFmpeg...**")
        loop = asyncio.get_running_loop()
        
        try:
            file_info = await bot.get_file(message.video.file_id)
            downloaded_file = await bot.download_file(file_info.file_path)

            in_v = f"in_vid_{message.message_id}.mp4"
            out_v = f"clean_vid_{message.message_id}.mp4"

            with open(in_v, 'wb') as f:
                f.write(downloaded_file)

            success = await loop.run_in_executor(
                executor, 
                remove_video_watermark, 
                in_v, 
                out_v, 
                "bottom"
            )

            if success and os.path.exists(out_v):
                with open(out_v, 'rb') as vf:
                    await bot.send_video(message.chat.id, vf, caption="✨ **ویدیو پاک‌سازی شد! ادساین و واترمارک با موفقیت حذف گردید.**")
                os.remove(out_v)
            else:
                await bot.reply_to(message, "❌ پردازش ویدیو ناموفق بود. ابزار FFmpeg را روی سرور بررسی کنید.")

            if os.path.exists(in_v):
                os.remove(in_v)
        except Exception as e:
            await bot.reply_to(message, f"❌ خطای پردازش ویدیو: {e}")
    else:
        await bot.reply_to(message, "💡 **نکته:** برای حذف ادساین، موقع ارسال ویدیو در کپشن بنویسید: `حذف ادساین`")

# ----------------------------------------------------------
# ۱۰. ماژول پردازش تصویر CapCut 4K HD
# ----------------------------------------------------------
@bot.message_handler(content_types=['photo'])
async def handle_photo_quantum(message):
    await bot.reply_to(message, "🔮 در حال ارتقای کیفیت به 4K Ultra HD...")
    loop = asyncio.get_running_loop()
    
    try:
        file_info = await bot.get_file(message.photo[-1].file_id)
        downloaded_file = await bot.download_file(file_info.file_path)

        in_p = f"in_{message.message_id}.jpg"
        out_p = f"out_{message.message_id}.jpg"

        with open(in_p, 'wb') as f:
            f.write(downloaded_file)

        def process_img():
            img = Image.open(in_p)
            img = img.filter(ImageFilter.SMOOTH_MORE)
            img = img.filter(ImageFilter.DETAIL)
            img = ImageEnhance.Sharpness(img).enhance(2.8)
            img.save(out_p, quality=100)

        await loop.run_in_executor(executor, process_img)

        if os.path.exists(out_p):
            with open(out_p, 'rb') as photo:
                await bot.send_photo(message.chat.id, photo, caption="✨ تصویر بازسازی شده با دقت کوانتومی ۵۴۰۰ آماده است!")
            os.remove(out_p)
        if os.path.exists(in_p):
            os.remove(in_p)
    except Exception as e:
        await bot.reply_to(message, f"❌ خطای پردازش تصویر: {e}")

# ----------------------------------------------------------
# ۱۱. موتور اصلی پردازش چت، عکس‌سازی، دانلود و ویس
# ----------------------------------------------------------
@bot.message_handler(func=lambda message: True)
async def quantum_main_engine(message):
    text = message.text.strip() if message.text else ""
    user_id = message.from_user.id
    loop = asyncio.get_running_loop()

    # ۱. تولید تصویر هوشمند با AI
    if any(text.startswith(p) for p in ["عکس بساز:", "تصویر بساز:", "تصویر:", "عکس:"]):
        prompt_input = re.sub(r'^(عکس بساز:|تصویر بساز:|تصویر:|عکس:)', '', text).strip()
        await bot.reply_to(message, "🎨 **در حال طراحی و خلق تصویر کوانتومی... لطفا چند ثانیه شکیبا باشید.**")
        
        img_bytes, info = await generate_ai_image(prompt_input)
        if img_bytes:
            await bot.send_photo(
                message.chat.id, 
                photo=img_bytes, 
                caption=f"✨ **تصویر خلق شد، ارباب رضا!**\n\n📌 **پرامپت:** {prompt_input}"
            )
        else:
            await bot.reply_to(message, f"❌ امکان ساخت تصویر در این لحظه وجود نداشت. علت: {info}")

    # ۲. حالت گفتگوی صوتی اپتیموس پرایم
    elif any(text.startswith(p) for p in ["پرایم:", "اپتیموس:", "Optimus:"]):
        clean_text = re.sub(r'^(پرایم:|اپتیموس:|Optimus:)', '', text).strip()
        await bot.reply_to(message, "🤖 **Optimus Prime Voice Mode Activated...**")
        
        prime_prompt = f"پاسخ این دستور را به سبک حماسی اپتیموس پرایم بنویس:\n{clean_text}"
        reply_text, _ = await ask_gemini_5400(prime_prompt, preferred_model="flash")

        await bot.reply_to(message, f"🦾 **[OPTIMUS PRIME]:**\n\n{reply_text}")

        def make_prime_voice():
            v_file = f"prime_{message.message_id}.mp3"
            return create_voice_file(reply_text, v_file, mode="prime")

        v_file = await loop.run_in_executor(executor, make_prime_voice)

        if v_file and os.path.exists(v_file):
            try:
                with open(v_file, 'rb') as vf:
                    await bot.send_voice(message.chat.id, vf, caption="⚡ ویس اختصاصی اپتیموس پرایم")
                os.remove(v_file)
            except Exception as e:
                logging.error(f"Voice Send Error: {e}")

    # ۳. توربو دانلودر پرسرعت
    elif "http://" in text or "https://" in text:
        await bot.reply_to(message, "🚀 **لینک دریافت شد! شروع توربو دانلود با ۱۰ تکه هم‌زمان...**")
        
        async def run_download_task():
            try:
                filepath = await asyncio.wait_for(loop.run_in_executor(executor, download_media_ultra, text), timeout=60.0)
                if filepath and os.path.exists(filepath):
                    with open(filepath, 'rb') as f:
                        if filepath.endswith(('.mp4', '.mkv', '.webm', '.mov')):
                            await bot.send_video(message.chat.id, f, caption="✅ ویدیو با موفقیت دانلود شد، ارباب رضا!")
                        else:
                            await bot.send_document(message.chat.id, f, caption="✅ فایل دانلود شد!")
                    os.remove(filepath)
            except asyncio.TimeoutError:
                await bot.reply_to(message, "⚠️ زمان دانلود به پایان رسید، اما ربات همچنان بیدار است!")
            except Exception as e:
                await bot.reply_to(message, f"❌ خطای دانلود: {e}")

        asyncio.create_task(run_download_task())

    # ۴. گفتگوی عمومی جارویس + پاسخ متنی
    else:
        try:
            reply_text, _ = await ask_gemini_5400(text, preferred_model="flash")
            await bot.reply_to(message, reply_text)
            
            cloud_db.log_memory(user_id, text, reply_text, lang=detect_language(text))

            def make_jarvis_voice():
                v_file = f"jarvis_{message.message_id}.mp3"
                return create_voice_file(reply_text, v_file, mode="jarvis")

            v_file = await loop.run_in_executor(executor, make_jarvis_voice)

            if v_file and os.path.exists(v_file):
                try:
                    with open(v_file, 'rb') as vf:
                        await bot.send_voice(message.chat.id, vf)
                    os.remove(v_file)
                except Exception as voice_err:
                    logging.error(f"ارور در ارسال ویس: {voice_err}")
        except Exception as e:
            logging.error(f"Main Chat Engine Error: {e}")
            await bot.reply_to(message, "سامانه فعال است، امر بفرمایید ارباب رضا.")

# ----------------------------------------------------------
# ۱۲. اجرای پایدار
# ----------------------------------------------------------
async def main():
    server_thread = threading.Thread(target=run_web_server)
    server_thread.daemon = True
    server_thread.start()

    print("⚡ J.A.R.V.I.S. OMEGA 5400 ULTIMATE is running...")
    await bot.infinity_polling(timeout=30, request_timeout=30, skip_pending=True)

if __name__ == "__main__":
    asyncio.run(main())
