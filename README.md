# ----------------------------------------------------------
# ۱۰. سیستم مدیریت کدهای هدیه و ردیم (Add Redeem System)
# ----------------------------------------------------------
class RedeemSystem:
    def __init__(self, db_name="jarvis_infinite_cloud_5400.db"):
        self.db_name = db_name
        self.init_redeem_db()

    def get_connection(self):
        return sqlite3.connect(self.db_name, check_same_thread=False)

    def init_redeem_db(self):
        with self.get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS redeem_codes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT UNIQUE,
                    reward TEXT,
                    is_used INTEGER DEFAULT 0
                )
            ''')
            conn.commit()

    def add_code(self, code, reward):
        try:
            with self.get_connection() as conn:
                conn.execute("INSERT INTO redeem_codes (code, reward) VALUES (?, ?)", (code, reward))
                conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def use_code(self, code):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT reward, is_used FROM redeem_codes WHERE code = ?", (code,))
            row = cursor.fetchone()
            if not row:
                return "❌ کد ردیم نامعتبر است."
            if row[1] == 1:
                return "⚠️ این کد قبلاً استفاده شده است."
            
            conn.execute("UPDATE redeem_codes SET is_used = 1 WHERE code = ?", (code,))
            conn.commit()
            return f"✅ کد با موفقیت اعمال شد! جایزه: {row[0]}"

redeem_manager = RedeemSystem()

# دستورات تلگرامی سیستم ردیم
@bot.message_handler(commands=['addredeem'])
async def add_redeem_command(message):
    if not is_master_user(message.from_user.username):
        await bot.reply_to(message, "❌ دسترسی غیرمجاز.")
        return
    
    # فرمت: /addredeem CODE REWARD
    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
        await bot.reply_to(message, "⚠️ فرمت اشتباه! استفاده:\n`/addredeem [کد] [عنوان جایزه]`", parse_mode="Markdown")
        return
    
    code, reward = parts[1], parts[2]
    if redeem_manager.add_code(code, reward):
        await bot.reply_to(message, f"✨ کد ردیم `{code}` با موفقیت ثبت شد، ارباب!", parse_mode="Markdown")
    else:
        await bot.reply_to(message, "❌ این کد از قبل وجود دارد.")

@bot.message_handler(commands=['redeem'])
async def redeem_command(message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await bot.reply_to(message, "⚠️ لطفاً کد ردیم را وارد کنید:\n`/redeem [کد_شما]`", parse_mode="Markdown")
        return
    
    code = parts[1].strip()
    result_msg = redeem_manager.use_code(code)
    await bot.reply_to(message, result_msg)
