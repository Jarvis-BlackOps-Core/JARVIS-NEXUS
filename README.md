import time
import json
import sqlite3
import datetime
from datetime import datetime, timedelta

# ==========================================================
# ۱۰. سیستم پادشاهی کدهای هدیه و ردیم (JARVIS GOD-MODE REDEEM ENGINE)
# ARCHITECT & COMMANDER: REZA MOHAFEZ
# ==========================================================

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
            # جدول کدهای پیشرفته
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS quantum_redeems (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT UNIQUE,
                    reward_type TEXT, -- TEXT, CONFIG, PRO_ACCESS, GAMING_VIP
                    reward_content TEXT,
                    max_uses INTEGER DEFAULT 1,
                    used_count INTEGER DEFAULT 0,
                    expires_at DATETIME
                )
            ''')
            # جدول ثبت ردیم‌ها
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
            
            # ۱. استعلام کد
            cursor.execute('''
                SELECT reward_type, reward_content, max_uses, used_count, expires_at 
                FROM quantum_redeems WHERE code = ?
            ''', (code,))
            row = cursor.fetchone()
            
            if not row:
                return "❌ **پروتکل ردیم:** این کد هدیه وجود ندارد یا نادرست است.", None
            
            reward_type, reward_content, max_uses, used_count, expires_at = row
            
            # ۲. بررسی تاریخ انقضا
            if expires_at:
                exp_date = datetime.strptime(expires_at, "%Y-%m-%d %H:%M:%S.%f") if "." in expires_at else datetime.strptime(expires_at, "%Y-%m-%d %H:%M:%S")
                if datetime.now() > exp_date:
                    return "⏳ **انقضای کد:** مهلت زمانی استفاده از این کد هدیه به پایان رسیده است!", None

            # ۳. بررسی ظرفیت
            if used_count >= max_uses:
                return "🚫 **تکمیل ظرفیت:** ظرفیت استفاده از این کد هدیه تمام شده است!", None

            # ۴. بررسی استفاده تکراری توسط همین کاربر
            cursor.execute("SELECT id FROM quantum_redeem_logs WHERE code = ? AND user_id = ?", (code, user_id_str))
            if cursor.fetchone():
                return "⚠️ **دسترسی تکراری:** شما قبلاً این کد هدیه را دریافت کرده‌اید!", None

            # ۵. ثبت موفقیت‌آمیز
            conn.execute("UPDATE quantum_redeems SET used_count = used_count + 1 WHERE code = ?", (code,))
            conn.execute("INSERT INTO quantum_redeem_logs (code, user_id, user_name) VALUES (?, ?, ?)", 
                         (code, user_id_str, str(username)))
            conn.commit()

            user_tag = f"@{username}" if username else f"USER_{user_id}"

            # ۶. تولید پاسخ اختصاصی بر اساس نوع جایزه
            if reward_type == "CONFIG":
                generated_config = f"vless://quantum-dubai-mlbb-5400-{user_id}@dxb.jarvis-core.net:443?type=grpc#{user_id}-REDEEM-GAMING-VIP"
                msg = (
                    f"🎉 **هدایای کوانتومی ارباب رضا برای کاربر {user_tag} فعال شد!**\n\n"
                    f"🔑 **کانفیگ اختصاصی گیمینگ شما (پینگ زیر ۱۵ms):**\n`{generated_config}`\n\n"
                    "⚡ **ویژگی:** پینگ سبز اختصاصی + زیرسیستم @Gamers_Shadow1bot."
                )
                return msg, "تبریک ارباب رضا! کد هدیه با موفقیت فعال شد و کانفیگ گیمینگ تحویل گردید."

            elif reward_type == "PRO_ACCESS":
                msg = (
                    f"👑 **ارتقای هوش مصنوعی به سطح Gemini 2.0 Pro!**\n\n"
                    f"حساب {user_tag} با موفقیت به موتور پردازش عمیق جارویس متصل شد."
                )
                return msg, "ارتقای سطح دسترسی با موفقیت انجام شد."

            else:  # TEXT or Default
                msg = f"🎁 **کد هدیه با موفقیت اعمال شد!**\n\n✨ **محتوای دریافت شده:**\n{reward_content}"
                return msg, "کد هدیه با موفقیت اعمال گردید."

quantum_redeem = QuantumRedeemEngine()

# ----------------------------------------------------------
# دستورات تلگرامی سیستم ردیم ۵۴۰۰
# ----------------------------------------------------------

@bot.message_handler(commands=['godredeem'])
async def make_god_redeem(message):
    if not is_master_user(message.from_user):
        await bot.reply_to(message, "🚨 **پروتکل ۹۲۰:** فقط فرماندهان ارشد مجاز به صدور هدیه هستند.")
        return
    
    # فرمت ساخت: /godredeem CODE TYPE CONTENT MAX_USES HOURS
    parts = message.text.split(maxsplit=5)
    if len(parts) < 4:
        guide = (
            "👑 **راهنمای ساخت کدهای پادشاهی ۵۴۰۰ (فرماندهی ارشد):**\n\n"
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
            f"⚡ **کد پادشاهی با موفقیت ساخته شد!**\n\n🔑 **کد:** `{code}`\n🎯 **نوع:** `{r_type}`\n👥 **ظرفیت:** {max_uses} نفر\n⏳ **اعتبار:** {time_msg}", 
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

    # تولید ویس صوتی بعد از اعمال موفقیت‌آمیز کد هدیه
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
