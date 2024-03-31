from aiogram import executor

from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # Birlamchi komandalar (/star va /help)
    await set_default_commands(dispatcher)
    await db.create()
    # await db.drop_birthday()
    # # await db.drop_FIO_state()
    # await db.drop_Guruhlar()
    # await db.drop_Gr_birthyday()
    await db.create_table_Guruhlar()
    await db.create_table_birthday()
    await db.create_table_FIO_state()
    await db.create_table_Gr_birthyday()


    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
