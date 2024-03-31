from aiogram import types

async def set_default_commands(dp):
    # Bot komandalarini alohida shaxsiy chatlar uchun o'rnatish
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Botni ishga tushurish"),
    ], scope=types.BotCommandScopeAllPrivateChats())  # Shaxsiy chatlar uchun

    # Bot komandalarini guruhlar uchun o'rnatish
    await dp.bot.set_my_commands([
        types.BotCommand("add_birthday", "Guruhingizga yangi tug'ilgan kunlar qo'shishing."),
        types.BotCommand("my_birthday", "Guruhingizdagi tug'ilganlar ro'yxati."),
        types.BotCommand("delete_birthday", "Guruhingizdagi tug'ilgan kunlarni o'chiring."),
    ], scope=types.BotCommandScopeAllGroupChats())  # Guruhlar uchun
