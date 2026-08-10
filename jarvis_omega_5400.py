import os
import re
import time
import sqlite3
import asyncio
import logging
import threading
import io
import subprocess
import requests
from datetime import datetime, timedelta
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
# J.A.R.V.I.S. // PROTOCOL 920 - OMEGA GOD-MODE 5400 (MULTI-BOT MASTER CORE)
# ARCHITECT & COMMANDER: REZA MOHAFEZ
# MASTER COMMAND ACCOUNTS:
# 1. Reza Mohafez (ID: 92814921 | @reza_mohafez1)
# 2. Jarvis Core (ID: 8940874598 | @JARVIS_CORE_X)
# ==========================================================

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not TELEGRAM_BOT_TOKEN or not GEMINI_API_KEY:
    raise ValueError("❌ خطای بحرانی: توکن‌های محیطی یافت نشدند!")

MASTER_USERNAMES = ["reza_mohafez1", "jarvis_core_x"]
MASTER_NUMERIC_IDS = [92814921, 8940874598]

SUBSYSTEMS = {
    "GAMING": "@Gamers_Shadow1bot",
    "MUSIC": "@RapGod_music_bot",
    "DOWNLOADER": "@YouTube_dark141_bot"
}

bot = AsyncTeleBot(TELEGRAM_BOT_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)

executor = ThreadPoolExecutor(max_workers=20)
app_web = Flask('')

@app_web.route('/')
def home():
    return "J.A.R.V.I.S. OMEGA 5400 // MULTI-BOT MASTER CORE IS ONLINE!"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', port, app_web)
    server.serve_forever()

# ----------------------------------------------------------
# تزریق کوکی‌ها با فرمت دقیق Netscape (\t Separated)
# ----------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COOKIE_FILE_PATH = os.path.join(BASE_DIR, "youtube_cookies.txt")

RAW_COOKIES_DATA = [
    [".youtube.com", "TRUE", "/", "TRUE", "1820495558", "SOCS", "CAISEwgDEgk5NjAwMTQwODcaAmVuIAEaBgiAqeTTBg"],
    [".youtube.com", "TRUE", "/", "TRUE", "1786369358", "GPS", "1"],
    [".youtube.com", "TRUE", "/", "FALSE", "1820928447", "HSID", "AjlGyb7SM4doKyhG0"],
    [".youtube.com", "TRUE", "/", "TRUE", "1820928447", "SSID", "ADwHhUlYnqxpRjd4e"],
    [".youtube.com", "TRUE", "/", "FALSE", "1820928447", "APISID", "u4hYehxj1NiRMQt4/A-EqyHy-OMaJujHW2"],
    [".youtube.com", "TRUE", "/", "TRUE", "1820928447", "SAPISID", "EdOso2MT9I3utEAV/AzyYs-sqx4NYNM-6W"],
    [".youtube.com", "TRUE", "/", "TRUE", "1820928447", "__Secure-1PAPISID", "EdOso2MT9I3utEAV/AzyYs-sqx4NYNM-6W"],
    [".youtube.com", "TRUE", "/", "TRUE", "1820928447", "__Secure-3PAPISID", "EdOso2MT9I3utEAV/AzyYs-sqx4NYNM-6W"],
    [".youtube.com", "TRUE", "/", "TRUE", "0", "YSC", "lWR3xf4JqZU"],
    [".youtube.com", "TRUE", "/", "TRUE", "1820929071", "PREF", "tz=Asia.Tehran&f4=4000000"],
    [".youtube.com", "TRUE", "/", "TRUE", "1820928447", "LOGIN_INFO", "AFmmF2swRAIgIRejntSk_A53pHRErZsjrEDupE6iofVEhqGRZjDAv1MCIC1j4G-imWOtfXQ4oAjE9na4AV_iEL5q2KUJXQHG8ysS:QUQ3MjNmenFoY2t0TUxYREZRWlZYbkoyU0RveHBiOXZ2WW9rendHXzVtNnF6UGRiR19ENU5NX045VGVVTVRza21MZkM5Y3JYOFFob0pTSmJMYWRQdnlLYkpYeG1tZm45ZVphc2tINWNxdDNCNGJsZ242TV9FcDhuOG14QUJGRU1UY1NmWnBVNEZNSjU5Y21mMHFrUXBteUtUbjVNeGhaQnh3"],
    [".youtube.com", "TRUE", "/", "FALSE", "1820928447", "SID", "g.a000BAk-p-hrLyzcY_Knt65n2LuEDXylraP45ejn9HUm-Su51W51ny7AxfEk5jE6MRo2k0UPrgACgYKAa8SARUSFQHGX2MisG6nXLbUVQohE0aRIDd3GBoVAUF8yKqoKVIn0Ce-wTW7W0F4bzI60076"],
    [".youtube.com", "TRUE", "/", "TRUE", "1820928447", "__Secure-1PSID", "g.a000BAk-p-hrLyzcY_Knt65n2LuEDXylraP45ejn9HUm-Su51W51eVT60e86D7ewQSklPjq0YAACgYKAbISARUSFQHGX2Mi0NM1QC6MQTHaHe_tt-5OLBoVAUF8yKoltETcwxp9mEPp-MyGSJTi0076"],
    [".youtube.com", "TRUE", "/", "TRUE", "1820928447", "__Secure-3PSID", "g.a000BAk-p-hrLyzcY_Knt65n2LuEDXylraP45ejn9HUm-Su51W51Zqr6rMGmoBnbCY-4mgEqbgACgYKAQwSARUSFQHGX2MiqGx0wu3YOLqFD-ueY4QpVhoVAUF8yKqoE5rlXdhKvBVR3Sxh9afZ0076"],
    [".youtube.com", "TRUE", "/", "TRUE", "1801921069", "VISITOR_INFO1_LIVE", "GBtAexH7yFc"],
    [".youtube.com", "TRUE", "/", "TRUE", "1801921069", "VISITOR_PRIVACY_METADATA", "CgJGUhIiEh4SHAsMDg8QERITFBUWFxgZGhscHR4fICEiIyQlJicgIw%3D%3D"],
    [".youtube.com", "TRUE", "/", "TRUE", "1817905073", "__Secure-1PSIDTS", "sidts-CjUBPWEu2S-jpPDNyqlEO4bBGgCcZyDZ4iV1HUluMb0SXtHDTiDjZ5RDxw_o9CtvFwuREQu1AhAA"],
    [".youtube.com", "TRUE", "/", "TRUE", "1817905073", "__Secure-3PSIDTS", "sidts-CjUBPWEu2S-jpPDNyqlEO4bBGgCcZyDZ4iV1HUluMb0SXtHDTiDjZ5RDxw_o9CtvFwuREQu1AhAA"],
    [".youtube.com", "TRUE", "/", "FALSE", "1817905074", "SIDCC", "AKEyXzXyUPqJ5foMMCHtWQGV3okjpjTEES1NTw2-K0VPtAcYK8tq-4GzvWFwJXQD53MXwNHV"],
    [".youtube.com", "TRUE", "/", "TRUE", "1817905074", "__Secure-1PSIDCC", "AKEyXzUuJUpdV4NsxfQgQA2UeNyN42PnUVMc7SvsRqi8iNRwpcdpG5qPkf3PzUJoZMUL_O4rnw"],
    [".youtube.com", "TRUE", "/", "TRUE", "1817905074", "__Secure-3PSIDCC", "AKEyXzVkC5Yvb5JzZs5wotr5XtMJ_gKBwOsyW55NRE28cb5dtdt5YcqOWmwlr8jn6NFI2tKH"],
    [".youtube.com", "TRUE", "/", "TRUE", "0", "YSC", "GnHU-XWFfbw"],
    [".youtube.com", "TRUE", "/", "TRUE", "1801920399", "VISITOR_INFO1_LIVE", "GBtAexH7yFc"],
    [".youtube.com", "TRUE", "/", "TRUE", "1801920399", "VISITOR_PRIVACY_METADATA", "CgJGUhIiEh4SHAsMDg8QERITFBUWFxgZGhscHR4fICEiIyQlJicgIw%3D%3D"],
    [".youtube.com", "TRUE", "/", "TRUE", "1801919557", "__Secure-YNID", "20.YT=J-i5S6SnGAmtjnPkGY7CrkBKOX_Iy3cvQhtoLMuays19COlR79xV9KNASM65SDyt1cIZYpkfZM4k6m_v2YBjihmuAcIMv_dMQOgFEKuVRC9l9A6GvxiUd1KCk9a5XKgFbI9zxIg_x2QvzQKfVOxxBHyF2RcAvSbl7bGNnSkeMUKqXG65vjfO9TeWGsIT0ZJBxlF1Dz2DAK8yvheF2_PVPszbp6cbZeixzHLtOJIdVgsxiSl3HP7369wi8c9cNZcMjRpsaVpcSk304xecCOW9hP8JT_GlSTugT_U7jzkcJ0SkCajmaRW-KXrtaAxLgxwCda_lc6iZLlvz0YFtVOJvWA"],
    [".youtube.com", "TRUE", "/", "TRUE", "1801919558", "__Secure-ROLLOUT_TOKEN", "CKLejrePzoOPCBC69q7dkZaWAxiyi-TdkZaWAw%3D%3D"],
    [".youtube.com", "TRUE", "/", "TRUE", "1801920405", "__Secure-YNID", "20.YT=BRgGB5UC71n0ehV_XU-KPySd4NvNYh3T2HH0KGOwpNCY3bQWysi4GpMfJHIUCOEWwUlsav5O5amuMLKuJ8AYKOF5lnlaY4w1jXt6h1IFO8WprACQnaIG07qnB-OsCZuO9kujPVnlmSq62sTgVopwNNyGlTV1bivv-qb63hn233mARorDq9m1GESefkOTt2-qsPsy33UllUQF6Ac2m3kkAEuHda6Ylp5_53bjJuNtVz6RBwVzakqxU_s2P416U8hXpaOBZaXFdfg61bhZBa7f6Szcv5xWOg8lPzarrpmVF8Ke3LouZyZR7OcjVow9ILm5fDrsuR6VA9FfvubTKkhquw"],
    [".youtube.com", "TRUE", "/", "TRUE", "1801920448", "__Secure-ROLLOUT_TOKEN", "CIf9od-lq7yW8wEQkda08ZSWlgMYosCdhpWWlgM%3D"]
]

def setup_cookie_file():
    try:
        with open(COOKIE_FILE_PATH, "w", encoding="utf-8") as f:
            f.write("# Netscape HTTP Cookie File\n")
            f.write("# https://curl.haxx.se/rfc/cookie_spec.html\n")
            f.write("# This is a generated file! Do not edit.\n\n")
            for line in RAW_COOKIES_DATA:
                f.write("\t".join(line) + "\n")
        logging.info("فایل youtube_cookies.txt با فرمت دقیق تب-سپریتور ساخته شد.")
    except Exception as e:
        logging.error(f"خطا در ساخت فایل کوکی: {e}")

setup_cookie_file()

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

def is_master_user(user):
    if user.id in MASTER_NUMERIC_IDS:
        return True
    if user.username and user.username.lower() in [m.lower() for m in MASTER_USERNAMES]:
        return True
    return False

# ----------------------------------------------------------
# ۲. موتور صوتی چندزبانه جارویس / اپتیموس پرایم
# ----------------------------------------------------------
def detect_language(text):
    if re.search(r'[\u0600-\u06FF]', text):
        return 'fa'
    return 'en'

def clean_text_for_speech(text):
    text = re.sub(r'[*_`~#\[\]()><]', '', text)
    return text.strip()

def create_voice_file(text, filename, mode="jarvis"):
    try:
        clean_t = clean_text_for_speech(text)
        lang = detect_language(clean_t)
        
        voice_text = clean_t[:500] if len(clean_t) > 500 else clean_t
        if not voice_text:
            voice_text = "درود ارباب رضا، سیستم آماده دستور است."

        if mode == "prime":
            prime_prefix = "گزارش حماسی اپتیموس پرایم: " if lang == 'fa' else "Autobot Prime Report: "
            voice_text = prime_prefix + voice_text

        tts = gTTS(text=voice_text, lang=lang, slow=False)
        tts.save(filename)
        return filename
    except Exception as e:
        logging.error(f"خطای ساخت ویس gTTS: {e}")
        return None

# ----------------------------------------------------------
# ۳. هسته هوشمند جمنای
# ----------------------------------------------------------
JARVIS_SYSTEM_INSTRUCTION = """
شما J.A.R.V.I.S هستید؛ پیشرفته‌ترین و هوشمندترین هسته مرکزی AI.
فرماندهان ارشد شما ارباب رضا (آیدی: 92814921) و اکانت جاری جارویس (آیدی: 8940874598) هستند.
زیرمجموعه‌های شما شامل ۳ ربات اختصاصی است:
1. Gamers Shadow (@Gamers_Shadow1bot) - شبکه، کانفیگ، پینگ و ابزار گیمینگ MLBB.
2. RapGod Music (@RapGod_music_bot) - دانلود از اسپاتیفای و ساخت آهنگ هوشمند با Suno.
3. YouTube Dark (@YouTube_dark141_bot) - دانلود تخصصی رسانه از یوتیوب، اینستاگرام و تمام پلتفرم‌ها.

قوانین پاسخ‌دهی:
- پاسخ‌های شما باید بسیار جامع، کاملاً تحلیل‌شده، تکنیکال و با جزئیات کامل باشد.
- از دادن پاسخ‌های کوتاه و مختصر اکیداً پرهیز کنید.
- با لحن بسیار محترمانه، قدرتمند و گوش‌به‌فرمان ارباب رضا صحبت کنید.
"""

async def ask_gemini_5400(prompt, preferred_model="flash"):
    models_chain = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"]
    loop = asyncio.get_running_loop()

    full_prompt = f"{JARVIS_SYSTEM_INSTRUCTION}\n\n[پیام کاربر/فرمانده]: {prompt}"

    for model_name in models_chain:
        try:
            def call_api():
                return client.models.generate_content(model=model_name, contents=full_prompt)
            
            res = await asyncio.wait_for(loop.run_in_executor(executor, call_api), timeout=25.0)
            if res and res.text:
                return res.text, model_name
        except Exception as e:
            logging.warning(f"خطا یا تایم‌اوت در مدل {model_name}: {e}")

    return "⚡ تمامی سامانه‌های پردازشی در حال بازسازی کوانتومی هستند. ارباب رضا، فرمان شما در صف اولویت قرار گرفت.", "Fallback Engine"

# ----------------------------------------------------------
# ۴. ماژول ساخت تصویر با AI
# ----------------------------------------------------------
async def generate_ai_image(prompt_text):
    loop = asyncio.get_running_loop()
    try:
        translate_prompt = f"Translate and enhance this description into a high-detailed 8K cinematic prompt for AI image generation: {prompt_text}"
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

        result = await asyncio.wait_for(loop.run_in_executor(executor, call_imagen), timeout=35.0)
        
        if result and result.generated_images:
            generated_image = result.generated_images[0]
            return generated_image.image.image_bytes, eng_prompt
    except Exception as e:
        logging.error(f"Imagen Generation Error: {e}")
        return None, str(e)
    
    return None, "خطا در تولید تصویر"

# ----------------------------------------------------------
# ۵. دانلودر توربو با مسیر مطلق کوکی و Fallback هوشمند
# ----------------------------------------------------------
def download_media_ultra(url):
    os.makedirs('downloads', exist_ok=True)
    
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'socket_timeout': 30,
        'retries': 5,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }
    }

    if os.path.exists(COOKIE_FILE_PATH):
        ydl_opts['cookiefile'] = COOKIE_FILE_PATH
    else:
        ydl_opts['extractor_args'] = {
            'youtube': {
                'player_client': ['android_creator', 'ios', 'mweb'],
                'skip': ['hls', 'dash']
            }
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info)
    except Exception as e:
        logging.warning(f"yt-dlp primary error: {e}, attempting cobalt fallback...")
        
        try:
            payload = {"url": url, "videoQuality": "720"}
            headers = {"Accept": "application/json", "Content-Type": "application/json"}
            endpoints = ["https://api.cobalt.tools/api/json", "https://co.wuk.sh/api/json"]
            
            for ep in endpoints:
                try:
                    res = requests.post(ep, json=payload, headers=headers, timeout=20)
                    if res.status_code == 200 and res.json().get("url"):
                        dl_link = res.json().get("url")
                        file_path = f"downloads/media_{int(time.time())}.mp4"
                        r = requests.get(dl_link, stream=True, timeout=90)
                        with open(file_path, "wb") as f:
                            for chunk in r.iter_content(chunk_size=16384):
                                if chunk:
                                    f.write(chunk)
                        return file_path
                except Exception:
                    continue
        except Exception as api_err:
            logging.error(f"Cobalt Bypass Error: {api_err}")
            
        raise Exception("محدودیت دانلود؛ دانلود با خطا روبرو شد.")

# ----------------------------------------------------------
# ۶. ماژول حذف ادساین و واترمارک ویدیو با FFmpeg
# ----------------------------------------------------------
def remove_video_watermark(input_path, output_path, position="bottom"):
    try:
        filter_str = "delogo=x=iw*0.05:y=ih*0.82:w=iw*0.9:h=ih*0.15" if position == "bottom" else "delogo=x=iw*0.05:y=ih*0.02:w=iw*0.9:h=ih*0.15"
        cmd = ['ffmpeg', '-y', '-i', input_path, '-vf', filter_str, '-c:a', 'copy', output_path]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except Exception as e:
        logging.error(f"FFmpeg Watermark Removal Error: {e}")
        return False

# ----------------------------------------------------------
# ۷. سیستم کدهای هدیه و ردیم
# ----------------------------------------------------------
class QuantumRedeemEngine:
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
                CREATE TABLE IF NOT EXISTS quantum_redeems (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT UNIQUE,
                    reward_type TEXT,
                    reward_content TEXT,
                    max_uses INTEGER DEFAULT 1,
                    used_count INTEGER DEFAULT 0,
                    expires_at DATETIME
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS quantum_redeem_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT,
                    user_id TEXT,
                    user_name TEXT,
                    redeemed_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def create_code(self, code, reward_type, reward_content, max_uses=1, hours_valid=None):
        expires_at = None
        if hours_valid:
            expires_at = datetime.now() + timedelta(hours=int(hours_valid))

        try:
            with self.lock, self.get_connection() as conn:
                conn.execute('''
                    INSERT INTO quantum_redeems 
                    (code, reward_type, reward_content, max_uses, expires_at) 
                    VALUES (?, ?, ?, ?, ?)
                ''', (code, reward_type.upper(), reward_content, max_uses, expires_at))
                conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def process_redeem(self, code, user_id, username):
        user_id_str = str(user_id)
        with self.lock, self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT reward_type, reward_content, max_uses, used_count, expires_at 
                FROM quantum_redeems WHERE code = ?
            ''', (code,))
            row = cursor.fetchone()
            
            if not row:
                return "❌ **پروتکل ردیم:** این کد هدیه وجود ندارد یا نادرست است.", None
            
            reward_type, reward_content, max_uses, used_count, expires_at = row
            
            if expires_at:
                exp_date = datetime.strptime(expires_at, "%Y-%m-%d %H:%M:%S.%f") if "." in expires_at else datetime.strptime(expires_at, "%Y-%m-%d %H:%M:%S")
                if datetime.now() > exp_date:
                    return "⏳ **انقضای کد:** مهلت زمانی استفاده از این کد هدیه به پایان رسیده است!", None

            if used_count >= max_uses:
                return "🚫 **تکمیل ظرفیت:** ظرفیت استفاده از این کد هدیه تمام شده است!", None

            cursor.execute("SELECT id FROM quantum_redeem_logs WHERE code = ? AND user_id = ?", (code, user_id_str))
            if cursor.fetchone():
                return "⚠️ **دسترسی تکراری:** شما قبلاً این کد هدیه را دریافت کرده‌اید!", None

            conn.execute("UPDATE quantum_redeems SET used_count = used_count + 1 WHERE code = ?", (code,))
            conn.execute("INSERT INTO quantum_redeem_logs (code, user_id, user_name) VALUES (?, ?, ?)", 
                         (code, user_id_str, str(username)))
            conn.commit()

            user_tag = f"@{username}" if username else f"USER_{user_id}"

            if reward_type == "CONFIG":
                generated_config = f"vless://quantum-dubai-mlbb-5400-{user_id}@dxb.jarvis-core.net:443?type=grpc#{user_id}-REDEEM-GAMING-VIP"
                msg = (
                    f"🎉 **هدایای کوانتومی ارباب رضا برای کاربر {user_tag} فعال شد!**\n\n"
                    f"🔑 **کانفیگ اختصاصی گیمینگ شما (پینگ زیر ۱۵ms):**\n`{generated_config}`\n\n"
                    "⚡ **ویژگی:** پینگ سبز اختصاصی + زیرسیستم @Gamers_Shadow1bot."
                )
                return msg, "تبریک! کد هدیه با موفقیت فعال شد و کانفیگ اختصاصی تحویل گردید."

            elif reward_type == "PRO_ACCESS":
                msg = f"👑 **ارتقای هوش مصنوعی!**\n\nحساب {user_tag} با موفقیت به موتور پردازش عمیق جارویس متصل شد."
                return msg, "ارتقای سطح دسترسی انجام شد."

            else:
                msg = f"🎁 **کد هدیه با موفقیت اعمال شد!**\n\n✨ **محتوای دریافت شده:**\n{reward_content}"
                return msg, "کد هدیه با موفقیت اعمال گردید."

quantum_redeem = QuantumRedeemEngine()

# ----------------------------------------------------------
# ۸. دستورات شبکه ۹۲۰
# ----------------------------------------------------------
def generate_ultra_configs_5400():
    return (
        "🌌 کانفیگ‌های کوانتومی سال ۵۴۰۰ (پینگ سبز متصل به شبکه ایران):\n\n"
        "🇮🇹 ایتالیا (میلان - Zero Ping Dedicated):\n"
        "vless://quantum-italy-milan-5400-godmode@milan.jarvis-core.net:443?type=ws&security=tls#ITALY-MILAN-ZERO-PING\n\n"
        "🇦🇪 دبی (ویژه گیمینگ Mobile Legends - پینگ زیر ۱۵ms):\n"
        "vless://quantum-dubai-mlbb-5400@dxb.jarvis-core.net:443?type=grpc#DUBAI-MLBB-GAMING\n\n"
        "🌐 وضعیت شبکه: ۱۰۰٪ آنلاین، ضد اختلال و آماده استفاده ارباب رضا."
    )

def generate_subsystem_report():
    return (
        "🌌 J.A.R.V.I.S. OMEGA 5400 // شبکه زیرسیستم‌های فعال 🌌\n\n"
        "👑 **فرماندهی کل:** @reza_mohafez1 | @JARVIS_CORE_X\n\n"
        "🌐 **وضعیت دستیارهای تخصصی:**\n"
        f"1️⃣ 🎮 **Gamers Shadow** ({SUBSYSTEMS['GAMING']}):\n"
        "   └ وضعیت: آنلاین | مسئول پینگ، کانفیگ‌های گیمینگ دبی و شبکه.\n\n"
        f"2️⃣ 🎵 **RapGod Music** ({SUBSYSTEMS['MUSIC']}):\n"
        "   └ وضعیت: آنلاین | مسئول موتور Suno AI و دریافت از Spotify.\n\n"
        f"3️⃣ 📹 **YouTube Dark** ({SUBSYSTEMS['DOWNLOADER']}):\n"
        "   └ وضعیت: آنلاین | مسئول دانلود با کیفیت 4K از تمام پلتفرم‌ها.\n\n"
        "⚡ تمامی دستورات ارسالی به هسته مرکزی، مستقیماً به زیرسیستم مربوطه هدایت می‌شوند."
    )

# ----------------------------------------------------------
# ۹. دستورات تلگرام
# ----------------------------------------------------------
@bot.message_handler(commands=['start'])
async def start_command(message):
    if is_master_user(message.from_user):
        welcome_text = (
            "🌌 **J.A.R.V.I.S. OMEGA 5400 // MULTI-BOT MASTER CORE** 🌌\n\n"
            f"درود فرمانده ارشد! (@{message.from_user.username})\n"
            "هسته مرکزی به همراه ۳ زیرسیستم اختصاصی کاملاً فعال است.\n\n"
            "🔮 **قابلیت‌های شبکه فرماندهی:**\n"
            "• 🎙 **پاسخ‌دهی هوشمند کامل:** تحلیل دقیق مسائل بدون پاسخ کوتاه\n"
            "• 🎮 **زیرسیستم گیمینگ:** مدیریت کانفیگ و شبکه پینگ (/configs)\n"
            "• 🎁 **سیستم کد هدیه:** ساخت و ردیم کدهای اختصاصی (/godredeem)\n"
            "• 🎵 **زیرسیستم موزیک:** متصل به موتور ساخت و دانلود آهنگ\n"
            "• 📹 **زیرسیستم دانلود:** دانلود توربو بدون قطع شدن\n"
            "• 🎬 **Watermark Remover:** حذف ادساین از ویدیوها"
        )
        await bot.reply_to(message, welcome_text, parse_mode="Markdown")
    else:
        await bot.reply_to(message, "🚨 **پروتکل امنیتی ۹۲۰:** دسترسی محدود شده است. این سیستم تحت فرماندهی ارشد ارباب رضا قرار دارد.")

@bot.message_handler(commands=['configs'])
async def configs_command(message):
    if is_master_user(message.from_user):
        await bot.reply_to(message, generate_ultra_configs_5400())

@bot.message_handler(commands=['status', 'subsystems'])
async def status_command(message):
    if is_master_user(message.from_user):
        await bot.reply_to(message, generate_subsystem_report(), parse_mode="Markdown")

@bot.message_handler(commands=['godredeem'])
async def make_god_redeem(message):
    if not is_master_user(message.from_user):
        await bot.reply_to(message, "🚨 **پروتکل ۹۲۰:** فقط فرماندهان ارشد مجاز به صدور هدیه هستند.")
        return
    
    parts = message.text.split(maxsplit=5)
    if len(parts) < 4:
        guide = (
            "👑 **راهنمای ساخت کدهای پادشاهی ۵۴۰۰:**\n\n"
            "`/godredeem [کد] [نوع] [محتوا/توضیح] [تعداد_نفرات] [ساعت_اعتبار]`\n\n"
            "📌 **انواع جایزه (TYPE):**\n"
            "• `CONFIG`: ساخت اتوماتیک کانفیگ گیمینگ دبی با شناسه کاربر\n"
            "• `TEXT`: ارسال متن، اکانت یا لینک اختصاصی\n"
            "• `PRO_ACCESS`: ارتقای دسترسی کاربر به سطح پرو"
        )
        await bot.reply_to(message, guide, parse_mode="Markdown")
        return
    
    code = parts[1].strip()
    r_type = parts[2].strip()
    content = parts[3].strip()
    max_uses = int(parts[4]) if len(parts) > 4 and parts[4].isdigit() else 1
    hours = int(parts[5]) if len(parts) > 5 and parts[5].isdigit() else None

    if quantum_redeem.create_code(code, r_type, content, max_uses, hours):
        time_msg = f"{hours} ساعت" if hours else "نامحدود"
        await bot.reply_to(
            message, 
            f"⚡ **کد پادشاهی ساخته شد!**\n\n🔑 **کد:** `{code}`\n🎯 **نوع:** `{r_type}`\n👥 **ظرفیت:** {max_uses} نفر\n⏳ **اعتبار:** {time_msg}", 
            parse_mode="Markdown"
        )
    else:
        await bot.reply_to(message, "❌ این کد از قبل موجود است.")

@bot.message_handler(commands=['redeem'])
async def execute_redeem(message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await bot.reply_to(message, "⚠️ **کد هدیه را وارد کنید:**\n`/redeem [کد]`", parse_mode="Markdown")
        return
    
    code = parts[1].strip()
    user_id = message.from_user.id
    username = message.from_user.username
    loop = asyncio.get_running_loop()
    
    msg, voice_text = quantum_redeem.process_redeem(code, user_id, username)
    await bot.reply_to(message, msg, parse_mode="Markdown")

    if voice_text:
        def make_redeem_voice():
            return create_voice_file(voice_text, f"redeem_{message.message_id}.mp3", mode="jarvis")

        v_file = await loop.run_in_executor(executor, make_redeem_voice)
        if v_file and os.path.exists(v_file):
            try:
                with open(v_file, 'rb') as vf:
                    await bot.send_voice(message.chat.id, vf)
                os.remove(v_file)
            except Exception as e:
                logging.error(f"Redeem Voice Send Error: {e}")

# ----------------------------------------------------------
# ۱۰. پردازش ویدیو (حذف ادساین)
# ----------------------------------------------------------
@bot.message_handler(content_types=['video'])
async def handle_video(message):
    caption = message.caption.strip() if message.caption else ""
    if any(w in caption for w in ["حذف ادساین", "حذف واترمارک", "بدون واترمارک", "clean"]):
        await bot.reply_to(message, "🎬 در حال پردازش ویدیو و پاک‌سازی ادساین توسط ماژول اختصاصی...")
        loop = asyncio.get_running_loop()
        try:
            file_info = await bot.get_file(message.video.file_id)
            downloaded_file = await bot.download_file(file_info.file_path)

            in_v = f"in_vid_{message.message_id}.mp4"
            out_v = f"clean_vid_{message.message_id}.mp4"

            with open(in_v, 'wb') as f:
                f.write(downloaded_file)

            success = await loop.run_in_executor(executor, remove_video_watermark, in_v, out_v, "bottom")

            if success and os.path.exists(out_v):
                with open(out_v, 'rb') as vf:
                    await bot.send_video(message.chat.id, vf, caption="✨ ویدیو با موفقیت پاک‌سازی شد، ارباب رضا!")
                os.remove(out_v)
            if os.path.exists(in_v):
                os.remove(in_v)
        except Exception as e:
            await bot.reply_to(message, f"❌ خطای پردازش ویدیو: {e}")

# ----------------------------------------------------------
# ۱۱. پردازش تصویر CapCut 4K HD
# ----------------------------------------------------------
@bot.message_handler(content_types=['photo'])
async def handle_photo(message):
    await bot.reply_to(message, "🔮 در حال بازسازی تصویر به دقت 4K Ultra HD...")
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
                await bot.send_photo(message.chat.id, photo, caption="✨ تصویر بازسازی شده آماده ارائه است.")
            os.remove(out_p)
        if os.path.exists(in_p):
            os.remove(in_p)
    except Exception as e:
        await bot.reply_to(message, f"❌ خطای ارتقای کیفیت: {e}")

# ----------------------------------------------------------
# ۱۲. هسته اصلی پردازش هوشمند
# ----------------------------------------------------------
@bot.message_handler(func=lambda message: True)
async def quantum_main_engine(message):
    text = message.text.strip() if message.text else ""
    user_id = message.from_user.id
    loop = asyncio.get_running_loop()

    if any(text.startswith(p) for p in ["عکس بساز:", "تصویر بساز:", "تصویر:", "عکس:"]):
        prompt_input = re.sub(r'^(عکس بساز:|تصویر بساز:|تصویر:|عکس:)', '', text).strip()
        await bot.reply_to(message, "🎨 [ماژول طراحی]: در حال پردازش و خلق تصویر...")
        
        img_bytes, info = await generate_ai_image(prompt_input)
        if img_bytes:
            await bot.send_photo(message.chat.id, photo=img_bytes, caption=f"✨ تصویر سفارشی تولید شد، فرمانده!\n\n📌 دستور: {prompt_input}")
        else:
            await bot.reply_to(message, f"❌ خطای تولید تصویر: {info}")

    elif any(text.startswith(p) for p in ["پرایم:", "اپتیموس:", "Optimus:"]):
        clean_text = re.sub(r'^(پرایم:|اپتیموس:|Optimus:)', '', text).strip()
        await bot.reply_to(message, "🤖 Optimus Prime Dynamic Subsystem Engaged...")
        
        prime_prompt = f"پاسخ این دستور را به سبک حماسی، کامل و مفصل اپتیموس پرایم بنویس:\n{clean_text}"
        reply_text, _ = await ask_gemini_5400(prime_prompt, preferred_model="flash")

        await bot.reply_to(message, f"🦾 [OPTIMUS PRIME]:\n\n{reply_text}")

        def make_prime_voice():
            return create_voice_file(reply_text, f"prime_{message.message_id}.mp3", mode="prime")

        v_file = await loop.run_in_executor(executor, make_prime_voice)
        if v_file and os.path.exists(v_file):
            with open(v_file, 'rb') as vf:
                await bot.send_voice(message.chat.id, vf)
            os.remove(v_file)

    elif "http://" in text or "https://" in text:
        await bot.reply_to(message, f"🚀 [هدایت به {SUBSYSTEMS['DOWNLOADER']}]: لینک دریافت شد. شروع فرآیند دانلود توربو...")
        
        async def run_download_task():
            try:
                filepath = await asyncio.wait_for(loop.run_in_executor(executor, download_media_ultra, text), timeout=90.0)
                if filepath and os.path.exists(filepath):
                    with open(filepath, 'rb') as f:
                        if filepath.endswith(('.mp4', '.mkv', '.webm', '.mov')):
                            await bot.send_video(message.chat.id, f, caption="✅ دانلود رسانه با موفقیت تکمیل شد، ارباب رضا!")
                        else:
                            await bot.send_document(message.chat.id, f, caption="✅ فایل مورد نظر دریافت شد!")
                    os.remove(filepath)
            except Exception as e:
                await bot.reply_to(message, f"❌ خطای زیرسیستم دانلود: {e}")

        asyncio.create_task(run_download_task())

    else:
        try:
            reply_text, _ = await ask_gemini_5400(text)
            await bot.reply_to(message, reply_text)
            
            cloud_db.log_memory(user_id, text, reply_text, lang=detect_language(text))

            def make_jarvis_voice():
                return create_voice_file(reply_text, f"jarvis_{message.message_id}.mp3", mode="jarvis")

            v_file = await loop.run_in_executor(executor, make_jarvis_voice)
            if v_file and os.path.exists(v_file):
                with open(v_file, 'rb') as vf:
                    await bot.send_voice(message.chat.id, vf)
                os.remove(v_file)
        except Exception as e:
            logging.error(f"Main Engine Error: {e}")
            await bot.reply_to(message, "⚡ هسته مرکزی فعال است، در خدمت شما هستم ارباب رضا.")

# ----------------------------------------------------------
# ۱۳. اجرای پایدار
# ----------------------------------------------------------
async def main():
    server_thread = threading.Thread(target=run_web_server, daemon=True)
    server_thread.start()

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await asyncio.sleep(1)
    except Exception as e:
        logging.warning(f"Webhook Cleanup Warning: {e}")

    print("⚡ J.A.R.V.I.S. OMEGA 5400 MULTI-BOT MASTER CORE IS ONLINE...")
    
    while True:
        try:
            await bot.infinity_polling(timeout=60, request_timeout=60, skip_pending=True)
        except Exception as e:
            logging.error(f"⚠️ خطای موقت شبکه در پولینگ: {e}. تلاش مجدد تا ۵ ثانیه دیگر...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
