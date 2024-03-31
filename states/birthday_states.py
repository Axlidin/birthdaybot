from aiogram.dispatcher.filters.state import StatesGroup, State


# Shaxsiy ma'lumotlarni yig'sih uchun:
class Birthday(StatesGroup):
    # Foydalanuvchi buyerda 4 ta holatdan o'tishi kerak
    FullName = State()#fio
    Year = State()#year
    Month = State()#month
    Day = State()#Day

# GR Shaxsiy ma'lumotlarni yig'sih uchun:
class Birthday_gr(StatesGroup):
    # Foydalanuvchi buyerda 4 ta holatdan o'tishi kerak
    FullName = State()#fio
    Year = State()#year
    Month = State()#month
    Day = State()#Day
# startberganda ismini olish
class Check_fio(StatesGroup):
    fullname = State()

# startbergandagi ismini yangilash
class updateCheck_fio(StatesGroup):
    fullname = State()

class del_birthday(StatesGroup):
    birhtday_del = State()

    ##gr
class del_birthdayGR(StatesGroup):
    birhtday_del = State()

class photo_birthday(StatesGroup):
    photo = State()

class del_photo(StatesGroup):
    photo_del = State()