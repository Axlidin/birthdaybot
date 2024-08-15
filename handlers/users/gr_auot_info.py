import datetime
import psycopg2
import pytz
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor, exceptions
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from data import config
from loader import bot, db

dp = Dispatcher(bot)

# Joylashuvingiz uchun vaqt mintaqasini sozlang
timezone = pytz.timezone("Asia/Tashkent")
# print(timezone)

# Ma'lumotlar bazasi ulanishini o'rnating
conn = psycopg2.connect(
    user=config.DB_USER,
    password=config.DB_PASS,
    host=config.DB_HOST,
    database=config.DB_NAME,
    port=config.DB_PORT
)
###############gr
# Joylashuvingiz uchun vaqt mintaqasini sozlang
timezone2 = pytz.timezone("Asia/Tashkent")
# print(timezone)

# Ma'lumotlar bazasi ulanishini o'rnating
# Joriy sanaga mos keladigan tug'ilgan kunlarni olish uchun funktsiyani belgilang
def get_birthdays_gr():
    today = datetime.datetime.now(timezone2)
    month = today.month
    day = today.day
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM Gr_birthyday WHERE Month = '{month}' AND Day = '{day}'")
    rows = cur.fetchall()
    unique_telegram_ids = set(row[6] for row in rows)
    for telegram_id in unique_telegram_ids:
        yield telegram_id


# Define the message to send
# Belgilangan Telegram foydalanuvchisiga xabar yuborish funksiyasini belgilang
async def send_message_gr(guruh_id):
    my_birthday = await db.my_user_seeGR_gr(guruh_id=guruh_id)
    today = datetime.datetime.now(timezone2)
    month = today.month
    day = today.day
    month_day = f"{month} {day}"
    for data in my_birthday:
        today = datetime.datetime.now(timezone2)
        year = today.year
        db_month_day = f"{data[3]} {data[4]}"
        if db_month_day == month_day:
            message = f"<b>Hurmatli, <i>{data[5].upper()}</i> guruhi admini</b> bugun guruhingizda o'z tug'ilgan kunini nishonlayotgan foydalanuvchi bor" \
                      f"... \n🎉 🎉 🎉Tabriklaymiz\n" \
                      f"Tug'ilgan kuningiz bilan <b><i>{data[1].upper()}\n🎉 🎉 🎉" \
                      f"{year - int(data[2])}</i></b> yoshingiz muborak bo'lsin"
            try:
                await bot.send_message(chat_id=guruh_id, text=message)
            except exceptions.BotBlocked:
                pass



# Xabarlarni yuborish uchun ishni belgilang
async def send_messages_job_gr():
    birthdays = get_birthdays_gr()
    for guruh_id in birthdays:
        await send_message_gr(guruh_id)

# Har kuni yarim tunda ishni bajarish uchun rejalashtiruvchini sozlang
scheduler = AsyncIOScheduler(timezone=timezone2)
scheduler.add_job(send_messages_job_gr, 'cron', hour=17, minute=12, second=0)

# Start the scheduler / Rejalashtiruvchini ishga tushiring
scheduler.start()
