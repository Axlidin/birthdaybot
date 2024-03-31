from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup

from keyboards.default.menu import AdminMain_menu, Main_menu
from loader import dp, db
@dp.message_handler(text="🛠 Sozlamalar")
async def bot_start_new_ism(message: types.Message, state: FSMContext):
    Mk = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    Mk.add("🛑 To'xtatish")
    await message.answer("yangi ismingizni kriting yoki 👇 tugmani bosing.", reply_markup=Mk)
    await state.set_state("new_ism")

@dp.message_handler(state="new_ism")
async def enter_new_ism(message: types.Message, state: FSMContext):
    if message.text == "🛑 To'xtatish":
        if message.from_user.id == 5419118871:
            await message.answer(f"Amal bekor qilindi.", reply_markup=AdminMain_menu)
        else:
            await message.answer(f"Amal bekor qilindi.", reply_markup=Main_menu)
        await state.finish()
        return

    new_name = message.text.upper()
    await db.update_user_FIO_state_username(fullname=new_name, telegram_id=message.from_user.id)
    if message.from_user.id == 5419118871:
        await message.answer(f"Ismingiz yangilandi: {new_name}", reply_markup=AdminMain_menu)
    else:
        await message.answer(f"Ismingiz yangilandi: {new_name}", reply_markup=Main_menu)
    await state.finish()
