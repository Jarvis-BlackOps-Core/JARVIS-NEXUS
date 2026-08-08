import time
import json
from datetime import datetime, timedelta

# ----------------------------------------------------------
# ۱۰. سیستم پادشاهی کدهای هدیه و ردیم (JARVIS GOD-MODE REDEEM ENGINE)
# ----------------------------------------------------------
class QuantumRedeemEngine:
    def __init__(self, db_name="jarvis_infinite_cloud_5400.db"):
        self.db_name = db_name
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_name, check_same_thread=False)

    def init_db(self):
        with self.get_connection() as conn:
            # جدول کدهای پیشرفته
            conn.execute('''
                CREATE TABLE IF NOT EXISTS quantum_redeems (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT UNIQUE,
                    reward_type TEXT, -- TEXT, CONFIG, PRO_ACCESS, FILE
                    reward_content TEXT,
                    max_uses INTEGER DEFAULT 1,
                    used_count INTEGER DEFAULT 0,
                    expires_at DATETIME
                )
            ''')
            # جدول ثبت ردیم‌ها
            conn.execute('''
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
            with self.get_connection() as conn:
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
        with self.get_connection() as conn:
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

            # ۶. تولید پاسخ اختصاصی بر اساس نوع جایزه (Type Handling)
            if reward_type == "CONFIG":
                # ساخت کانفیگ هوشمند با نام کاربر
                user_tag = username if username else f"USER_{user_id}"
                generated_config = f"vless://jarvis-quantum-5400-{user_tag}@milan.jarvis-core.net:443?type=ws&security=tls#{user_tag}-REDEEM-VIP"
                msg = f"🎉 **هدایای کوانتومی ارباب رضا فعال شد!**\n\n🔑 **کانفیگ اختصاصی شما:**\n`{generated_config}`\n\n⚡ **ویژگی:** پینگ سبز گیمینگ + پهنای باند نامحدود."
                return msg, "voice_congratulations"

            elif reward_type == "PRO_ACCESS":
                msg = f"👑 **ارتقای هوش مصنوعی به سطح Gemini 2.5 Pro!**\n\nحساب شما با موفقیت به موتور قدرتمند پردازش عمیق متصل شد."
                return msg, "voice_prime"

            else:  # TEXT or Default
                msg = f"🎁 **کد هدیه با موفقیت اعمال شد!**\n\n✨ **جایزه شما:**\n{reward_content}"
                return msg, "voice_jarvis"

quantum_redeem = QuantumRedeemEngine()

# ----------------------------------------------------------
# دستورات تلگرامی سیستم ردیم خفن ۵۴۰۰
# ----------------------------------------------------------

@bot.message_handler(commands=['godredeem'])
async def make_god_redeem(message):
    if not is_master_user(message.from_user.username):
        await bot.reply_to(message, "❌ **پروتکل ۹۲۰:** فقط ارباب رضا مجاز به صدور هدیه است.")
        return
    
    # فرمت ساخت: /godredeem CODE TYPE CONTENT MAX_USES HOURS
    # مثال: /godredeem REZA920 CONFIG "کانفیگ دبی" 10 24
    parts = message.text.split(maxsplit=5)
    if len(parts) < 4:
        guide = (
            "👑 **راهنمای ساخت کدهای خفن ۵۴۰۰ (ارباب رضا):**\n\n"
            "`/godredeem [کد] [نوع] [محتوا/توضیح] [تعداد_نفرات] [ساعت_اعتبار]`\n\n"
            "📌 **انواع نوع جایزه (TYPE):**\n"
            "• `CONFIG`: ساخت اتوماتیک کانفیگ اختصاصی به اسم کاربر\n"
            "• `TEXT`: متن، لینک یا اکانت آماده\n"
            "• `PRO_ACCESS`: دسترسی پرو به جمنای"
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
    
    msg, action_voice = quantum_redeem.process_redeem(code, user_id, username)
    await bot.reply_to(message, msg, parse_mode="Markdown")
