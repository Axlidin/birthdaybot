import sqlite3
from asyncio import sleep
from calendar import monthrange

import asyncpg
from aiogram.types import KeyboardButton, ReplyKeyboardRemove, CallbackQuery
from filters import IsGroup
from loader import bot, db
from states.birthday_states import Birthday_gr, del_birthday, del_birthdayGR
# /form komandasi uchun handler yaratamiz. Bu yerda foydalanuvchi hech qanday holatda emas, state=None
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup
from loader import dp

# Admin komandasi
@dp.message_handler(IsGroup(), commands=['Add_birthday'])
async def add_birthday_gr(message: types.Message):
    msg_id = message.message_id
    await sleep(2)
    await bot.delete_message(chat_id=message.chat.id, message_id=msg_id)
    # Foydalanuvchini ID raqami va ismi
    user_id = message.from_user.id
    user_name = message.from_user.username

    # Guruh ID raqami va nomi
    group_id = message.chat.id
    group_name = message.chat.title

    # Foydalanuvchini guruhda admin bo'lishini tekshiramiz
    chat_member = await bot.get_chat_member(group_id, user_id)
    if chat_member.is_chat_admin():
        Mk = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        Mk.add("🛑 To'xtatish")
        await message.answer("Ism kiriting", reply_markup=Mk)
        await Birthday_gr.FullName.set()
    else:
        pass

@dp.message_handler(text="🛑 To'xtatish", state=Birthday_gr)
async def cancel_see_gr(message: types.Message, state: FSMContext):
    await message.answer("Siz Tug'ilgan kun qo'shishni bekor qildingiz",
                         reply_markup=ReplyKeyboardRemove())
    #, reply_markup=AdminMain_menu)
    await state.reset_state()

@dp.callback_query_handler(text="stop", state=Birthday_gr)
async def cancel_saw_inline_gr(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()# , reply_markup=AdminMain_menu)
    await call.message.answer("Siz Tug'ilgan kun qo'shishni bekor qildingiz")
    await state.reset_state()

@dp.message_handler(state=Birthday_gr.FullName)
async def answer_fullname_gr(message: types.Message, state: FSMContext):
    fullname = message.text.upper()
    await state.update_data(
        {"name": fullname}
    )
    Mk = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    Mk.add("🛑 To'xtatish")
    await message.answer("Tug'ilgan yil kiriting! (<b>1996</b>)", reply_markup=Mk)

    await Birthday_gr.next()

@dp.message_handler(lambda message: not message.text.isdigit(), state=Birthday_gr.Year)
async def process_year_gr(message: types.Message):
    """
    If year is invalid
    """
    Mk = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    Mk.add("🛑 To'xtatish")
    return await message.answer("yil faqat raqamlarda kiritilishi kerak!!<b>1996</b>", reply_markup=Mk)

@dp.message_handler(state=Birthday_gr.Year)
async def answer_year_gr(message: types.Message, state: FSMContext):
    year = str(message.text)
    if len(year) == 4:
        await state.update_data(
            {"year": int(year)}
        )
        days_buttons = []
        for day in range(1, 13):
            days_buttons.append(InlineKeyboardButton(text=str(day), callback_data=str(day)))
        days_inline_keyboard = [days_buttons[i:i + 4] for i in range(0, len(days_buttons), 4)]
        months = InlineKeyboardMarkup(inline_keyboard=days_inline_keyboard)

        stop_button = InlineKeyboardButton(text="🛑 To'xtatish", callback_data="stop")
        months.add(stop_button)
        await message.answer("<b>Tug'ilgan oyni tanlang.</b>", reply_markup=months)
        await Birthday_gr.next()
    else:
        Mk = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        Mk.add("🛑 To'xtatish")
        await message.answer("Tug'ilgan yil 4 ta raqamdan iborat bo'ladi (<b>xxxx</b>)", reply_markup=Mk)
        await Birthday_gr.Year.set()

@dp.callback_query_handler(state=Birthday_gr.Month)
async def answer_month_gr(call: CallbackQuery, state: FSMContext):
    month = int(call.data)
    await call.message.delete()
    await state.update_data({"month": month})
    data = await state.get_data()
    year = int(data.get("year"))
    month_days = monthrange(year, month)[1]
    days_buttons = []
    for day in range(1, month_days + 1):
        days_buttons.append(InlineKeyboardButton(text=str(day), callback_data=str(day)))
    days_inline_keyboard = [days_buttons[i:i + 4] for i in range(0, len(days_buttons), 4)]
    days = InlineKeyboardMarkup(inline_keyboard=days_inline_keyboard)
    stop_button = InlineKeyboardButton(text="🛑 To'xtatish", callback_data="stop")
    days.add(stop_button)
    await call.message.answer(f"✅ {call.data}")
    await call.message.answer("<b>Tug'ilgan kun tanglang.</b>", reply_markup=days)
    await Birthday_gr.next()

@dp.callback_query_handler(state=Birthday_gr.Day)
async def answer_month_gr(call: CallbackQuery, state: FSMContext):
    day = int(call.data)
    await call.message.delete()
    await call.message.answer(f"✅ {call.data}")
    # print(day)
    await state.update_data(
        {"day": day}
    )
    # Ma`lumotlarni qayta o'qiymiz
    data = await state.get_data()
    await state.finish()  # malumotlar ochib ketadi
    group_id = call.message.chat.id
    guruh_name = call.message.chat.title
    chat_id = call.message.chat.id
    # print(f"chat id {chat_id}")
    # print(f"gr id {group_id}")
    # print(f"gr name {guruh_name}")
    chatttt = await db.my_user_seeGuruhlar_user(chat_id=int(chat_id))
    # print(chatttt)
    if chatttt:
        pass

    else:
        try:
            await db.add_Guruhlar(chat_id=chat_id,
                            GroupName=call.message.chat.title)
        except asyncpg.exceptions.UniqueViolationError:
            await state.reset_state(with_data=True)

    try:
        await db.add_Gr_birthyday(guruh_name=guruh_name,
                          full_name=data['name'],
                          Year=data['year'],
                          Month=data['month'],
                          Day=data['day'],
                          guruh_id=group_id),
    except asyncpg.exceptions.UniqueViolationError as sasa:
        # print(sasa)
        await state.reset_state(with_data=True)
    messageGr = (f"<b>Ism</b>: {data['name']}\n"
                 f"<b>Yil</b>: {data['year']}\n"
                 f"<b>Oy</b>: {data['month']}\n"
                 f"<b>Kun</b>: {data['day']}")
    await call.message.answer(f"Tabriklaymiz,siz muvaffaqiyatli tug'ilgan kun kiritdingiz.\n{messageGr}", reply_markup=ReplyKeyboardRemove())


 ###delete
#tug'ilgan kun o'chirish
@dp.message_handler(IsGroup(), commands=["Delete_birthday"])
async def delete_birthday_gr(message: types.Message):
    msg_id = message.message_id
    await sleep(2)
    await bot.delete_message(chat_id=message.chat.id, message_id=msg_id)
    guruh_id = message.chat.id
    my_birthday = await db.my_user_seeGR_gr(guruh_id=guruh_id)
    # Foydalanuvchini ID raqami va ismi
    user_id = message.from_user.id
    user_name = message.from_user.username

    # Guruh ID raqami va nomi
    group_id = message.chat.id
    group_name = message.chat.title

    # Foydalanuvchini guruhda admin bo'lishini tekshiramiz
    chat_member = await bot.get_chat_member(group_id, user_id)
    Mk = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    if chat_member.is_chat_admin():
        if my_birthday:
            for menu in my_birthday:
                fan_name_menu = menu[1]
                Mk.insert(KeyboardButton(text=fan_name_menu, resize_keyboard=True))
            Mk.add("🛑 To'xtatish")
            await message.answer(f"Kerakli Odamni tanlang! yoki tugmani bosing", reply_markup=Mk)
            await del_birthdayGR.next()
        else:
            await message.answer(
                "❌ Sizda Tug'ilgan kunlar hozirda mavjud emas.\n"
                    "Tug'ilgan kun qo'shish uchun <i>/add_birthday@happyMybirthday_bot</i> tugmasini bosing")
    else:
        pass

@dp.message_handler(text=["🛑 To'xtatish"], state=del_birthdayGR)
async def cancel_deletebirthday_gr(message: types.Message, state: FSMContext):
    await message.answer("Siz Tug'ilgan kunni o'chirishni bekor qildingiz", reply_markup=ReplyKeyboardRemove())
    await state.reset_state()

@dp.message_handler(state=del_birthdayGR.birhtday_del)
async def data_delbirthday_gr(message: types.Message, state: FSMContext):
    del_birthday = message.text.upper()
    # print(del_birthday)
    await state.update_data(
        {"del_birthday": del_birthday}
    )
    deletes = await db.delete_birhdaygr(del_name=del_birthday)
    if deletes:
        await message.answer("Hozirda bunday ismli odam yo'q.", reply_markup=ReplyKeyboardRemove())
        await state.finish()
    else:
        await message.answer(f"Siz tug'ilgan kun o'chirdinggiz\n\nDelete: {del_birthday}",
                             reply_markup=ReplyKeyboardRemove())
        await state.reset_state(with_data=True)
import psycopg2
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram import types

from data import config
from loader import bot, dp
# Ma'lumotlar bazasi ulanishini o'rnating
conn = psycopg2.connect(
    user=config.DB_USER,
    password=config.DB_PASS,
    host=config.DB_HOST,
    database=config.DB_NAME,
    port=config.DB_PORT
)
PAGE_SIZE = 2
def get_itemsgr(page, tg_id):
    cur = conn.cursor()
    offset = (page - 1) * PAGE_SIZE
    cur.execute(
        f"SELECT * FROM Gr_birthyday WHERE guruh_id=%s ORDER BY id LIMIT %s OFFSET %s",
        (tg_id, PAGE_SIZE, offset)
    )
    products = cur.fetchall()
    return products


# Orqaga va oldinga tugmalarini yaratish funksiyasini aniqlang
def create_page_buttonsgr(page):
    back_button = InlineKeyboardButton(
        "⬅️",
        callback_data=f"ortga_{page-1}" if page > 1 else "ortga_1"
    )
    forward_button = InlineKeyboardButton(
        "➡️",
        callback_data=f"oldinga_{page+1}"
    )
    exit_button = InlineKeyboardButton(
        "❌", callback_data="saxifadanChiqish"
    )
    return InlineKeyboardMarkup().row(back_button, exit_button, forward_button)

# Orqaga va oldinga tugmalarini yaratish funksiyasini aniqlang
def create_page_firtsgr(page):
    forward_button = InlineKeyboardButton(
        "➡️",
        callback_data=f"oldinga_{page+1}"
    )
    exit_button = InlineKeyboardButton(
        "❌", callback_data="saxifadanChiqish"
    )
    return InlineKeyboardMarkup().row(exit_button, forward_button)

@dp.callback_query_handler(lambda c: c.data == 'saxifadanChiqish')
async def exit_button_handlergr(callback_query: types.CallbackQuery):
    await bot.send_message(chat_id=callback_query.message.chat.id, text="<b>Ma'lumotlar olish tugatildi.</b>",
                               reply_markup=ReplyKeyboardRemove())
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)

# Sahifani o'zgartirish uchun foydalanuvchi so'rovlarini bajarish uchun funktsiyani belgilang
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('ortga_'))
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('oldinga_'))
async def process_page_callbackgr(callback_query: types.CallbackQuery):
    tg_id = callback_query["message"]['chat']['id']
    action = callback_query.data
    page = int(callback_query.data.split("_")[1])
    if action == "ortga_1":
        page -= 1
        page = 1
        products = get_itemsgr(page, tg_id)
        buttons = create_page_firtsgr(page)
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=format_productsgr(products),
            reply_markup=buttons
        )
    else:
        products = get_itemsgr(page, tg_id)
        buttons = create_page_buttonsgr(page)
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=format_productsgr(products),
            reply_markup=buttons
        )

#Mahsulotlarni matn sifatida formatlash funksiyasini aniqlang
def format_productsgr(products):
    if not products:
        return "Tug'ilgan kunlar topilmadi."

    lines = [f"<b>Sizning Guruhingizdagi tug'ilgan kunlar ro'yxati:</b>\n"]
    for p in products:

        lines.append(f"<b>🔰 Ism:</b>  <i>{p[1].upper()}</i>\n"
                    f"<b>🗓 Tug'ilgan Yili<i> (faqat raqamlarda)</i>:</b> {p[2]}\n"
                    f"<b>📅 Tug'ilgan Oyi<i> (faqat raqamlarda)</i>:</b> {str(p[3]).rjust(2, '0')}\n"
                    f"<b>📆 Tug'ilgan Kuni<i> (faqat raqamlarda)</i>:</b>{str(p[4]).rjust(2, '0')}\n\n"
                    f"**********\n")
    return "\n".join(lines)

# Define function to handle user requests to start browsing products
@dp.message_handler(IsGroup(), commands=["My_birthday"])
async def process_start_commandgr(message: types.Message):
    msg_id = message.message_id
    await sleep(2)
    await bot.delete_message(chat_id=message.chat.id, message_id=msg_id)
    chat_id = message.chat.id
    # print(chat_id)

    page = 1
    products = get_itemsgr(page, chat_id)
    buttons = create_page_buttonsgr(page)
    # Foydalanuvchini ID raqami va ismi
    user_id = message.from_user.id
    user_name = message.from_user.username

    # Guruh ID raqami va nomi
    group_id = message.chat.id
    group_name = message.chat.title

    # Foydalanuvchini guruhda admin bo'lishini tekshiramiz
    chat_member = await bot.get_chat_member(group_id, user_id)
    if chat_member.is_chat_admin():
        await bot.send_message(
            chat_id=message.chat.id,
            text=format_productsgr(products),
            reply_markup=buttons
        )
    else:
        pass
    chat_id = message.chat.id
    chatttt = await db.my_user_seeGuruhlar_user(chat_id=chat_id)
    if chatttt:
        pass

    else:
        try:
            await db.add_Guruhlar(chat_id=chat_id,
                            GroupName=message.chat.title)
        except asyncpg.exceptions.UniqueViolationError:
            pass