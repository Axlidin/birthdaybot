from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

Main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Add birthday"),
            KeyboardButton(text="📝My birthday"),
        ],
        [
            KeyboardButton(text="Delete birthday"),
            KeyboardButton(text="🛠 Sozlamalar"),
        ],
        [
            KeyboardButton(text="Support service"),
        ],
    ],
    resize_keyboard=True, one_time_keyboard=True
)
# admins
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

AdminMain_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Add birthday"),
            KeyboardButton(text="📝My birthday"),
        ],
        [
            KeyboardButton(text="Delete birthday"),
            KeyboardButton(text="📊 Statistika"),
        ],
        [
            KeyboardButton(text="Sendpost"),
            KeyboardButton(text="🛠 Sozlamalar"),
        ],
        [KeyboardButton(text="Gr_post")],
    ],
    resize_keyboard=True, one_time_keyboard=True
)

