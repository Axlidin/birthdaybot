import psycopg2
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram import types

from data import config
from loader import bot, dp
from keyboards.default.menu import Main_menu, AdminMain_menu
import sqlite3
# Ma'lumotlar bazasi ulanishini o'rnating
conn = psycopg2.connect(
    user=config.DB_USER,
    password=config.DB_PASS,
    host=config.DB_HOST,
    database=config.DB_NAME,
    port=config.DB_PORT
)
PAGE_SIZE = 2
def get_items(page, tg_id):
    cur = conn.cursor()
    offset = (page - 1) * PAGE_SIZE
    cur.execute(
        f"SELECT * FROM birthday WHERE telegram_id=%s ORDER BY id LIMIT %s OFFSET %s",
        (tg_id, PAGE_SIZE, offset)
    )
    products = cur.fetchall()
    return products

# Orqaga va oldinga tugmalarini yaratish funksiyasini aniqlang
def create_page_buttons(page):
    back_button = InlineKeyboardButton(
        "⬅️",
        callback_data=f"back_{page-1}" if page > 1 else "back_1"
    )
    forward_button = InlineKeyboardButton(
        "➡️",
        callback_data=f"forward_{page+1}"
    )
    exit_button = InlineKeyboardButton(
        "❌", callback_data="page_exit"
    )
    return InlineKeyboardMarkup().row(back_button, exit_button, forward_button)

# Orqaga va oldinga tugmalarini yaratish funksiyasini aniqlang
def create_page_firts(page):
    forward_button = InlineKeyboardButton(
        "➡️",
        callback_data=f"forward_{page+1}"
    )
    exit_button = InlineKeyboardButton(
        "❌", callback_data="page_exit"
    )
    return InlineKeyboardMarkup().row(exit_button, forward_button)
@dp.callback_query_handler(text="cancel_admin")
async def cancelmenu_admin(call: CallbackQuery):
    await call.message.answer("<b>Asosiy bo'lim!</b>", reply_markup=AdminMain_menu)
    await call.answer(cache_time=30)

@dp.callback_query_handler(text="cancel")
async def cancelmenu(call: CallbackQuery):
    await call.message.answer("<b>Asosiy bo'lim!</b>", reply_markup=Main_menu)
    await call.message.delete()
    await call.answer(cache_time=30)
# Handler for "exit" button
@dp.callback_query_handler(lambda c: c.data == 'page_exit')
async def exit_button_handler(callback_query: types.CallbackQuery):
    if callback_query['from']['id'] == 5419118871:
        await bot.send_message(chat_id=callback_query.message.chat.id, text="<b>Ma'lumotlar olish tugatildi.</b>",
                               reply_markup=AdminMain_menu)
    else:
        await bot.send_message(chat_id=callback_query.message.chat.id, text="<b>Ma'lumotlar olish tugatildi.</b>",
                               reply_markup=Main_menu)
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)

# Sahifani o'zgartirish uchun foydalanuvchi so'rovlarini bajarish uchun funktsiyani belgilang
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('back_'))
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('forward_'))

async def process_page_callback(callback_query: types.CallbackQuery):
    # print(callback_query['from']['id'])
    tg_id = callback_query['from']['id']
    action = callback_query.data
    page = int(callback_query.data.split("_")[1])
    if action == "back_1":
        page -= 1
        page = 1
        products = get_items(page, tg_id)
        buttons = create_page_firts(page)
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=format_products(products),
            reply_markup=buttons
        )
    else:
        products = get_items(page, tg_id)
        buttons = create_page_buttons(page)
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=format_products(products),
            reply_markup=buttons
        )


#Mahsulotlarni matn sifatida formatlash funksiyasini aniqlang
def format_products(products):
    if not products:
        return "Tug'ilgan kunlar topilmadi."


    lines = [f"<b>Sizning Tug'ilgan kunlar ro'yxatingiz:</b>\n"]
    for p in products:

        lines.append(f"<b>🔰 Ism:</b>  <i>{p[1].upper()}</i>\n"
                    f"<b>🗓 Tug'ilgan Yili<i> (faqat raqamlarda)</i>:</b> {p[2]}\n"
                    f"<b>📅 Tug'ilgan Oyi<i> (faqat raqamlarda)</i>:</b> {str(p[3]).rjust(2, '0')}\n"
                    f"<b>📆 Tug'ilgan Kuni<i> (faqat raqamlarda)</i>:</b>{str(p[4]).rjust(2, '0')}\n\n"
                    f"**********\n")
    return "\n".join(lines)

# Define function to handle user requests to start browsing products
@dp.message_handler(text="📝My birthday")
async def process_start_command(message: types.Message):
    tg_id = message.from_user.id
    # get_me = show_me(tg_id=tg_id)
    # print(get_me)



    page = 1
    products = get_items(page, tg_id)
    buttons = create_page_buttons(page)
    await bot.send_message(
        chat_id=message.chat.id,
        text=format_products(products),
        reply_markup=buttons
    )
