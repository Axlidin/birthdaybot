from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

cancel = InlineKeyboardMarkup(
        inline_keyboard=[
       [
           InlineKeyboardButton(text='Yashirish', callback_data="cancel"),
       ]])
cancel_admin = InlineKeyboardMarkup(
        inline_keyboard=[
       [
           InlineKeyboardButton(text='Yashirish', callback_data="cancel_admin"),
       ]])

from aiogram.utils.callback_data import CallbackData

cancel_callback = CallbackData("cancel", "item_name")
cancel_callback_ADMIN = CallbackData("cancel_admin", "item_name")
