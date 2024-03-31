import asyncpg
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from filters import IsPrivate
from keyboards.default.menu import Main_menu, AdminMain_menu
from loader import dp
# Get current month and day
from loader import db
from states.birthday_states import Check_fio
@dp.message_handler(IsPrivate(), CommandStart())
async def bot_start(message: types.Message):
    telegram_id = message.from_user.id
    db_fios = await db.my_bithday_see(tg_id=telegram_id)
    # print(db_fios)
    if telegram_id == 5419118871:
        if not db_fios:
            await message.answer("Xush kelibsiz bot creator!")
            await message.answer("Ismingizni kiriting!")
            await Check_fio.next()
        else:
            await message.answer("❕ Kerakli bo'limni tanlang.", reply_markup=AdminMain_menu)
    else:
        if not db_fios:
            await message.answer("Ismingizni kiriting!")
            await Check_fio.next()
        else:
            await message.answer("❕ Kerakli bo'limni tanlang.", reply_markup=Main_menu)

@dp.message_handler(state=Check_fio.fullname)
async def fullname(message: types.Message, state: FSMContext):
    fullname = message.text.upper()
    await state.update_data(
        {"fullname": fullname}
    )
    # ma'lumotlarni qayta o'qish
    data = await state.get_data()
    fullname = data.get("fullname")

    msg = "Quyidagi ma'lumotlar qabul qilindi:\n"
    msg += f"🔰 fullname ---- {fullname}\n"

    await state.finish()
    #Admin_menu
    telegram_id = message.from_user.id
    if telegram_id == 5419118871:
        await message.answer("❕ Kerakli bo'limni tanlang.", reply_markup=AdminMain_menu)
    else:
        await message.answer("❕ Kerakli bo'limni tanlang.", reply_markup=Main_menu)
    try:
        await db.add_FIO_state(
            telegram_id=message.from_user.id,
            fullname=data["fullname"],
        )
    except asyncpg.exceptions.UniqueViolationError:
        await state.reset_state(with_data=True)
