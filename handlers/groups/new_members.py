import sqlite3

import asyncpg
from aiogram import types
from loader import dp, db
import logging

# Loggerni sozlash
logging.basicConfig(level=logging.ERROR,
                    filename='error.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)
@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def add_member(message: types.Message):
    chat_id = message.chat.id
    is_bot = message.new_chat_members[0].is_bot
    if not is_bot:  # Agar qo'shilgan foydalanuvchi bot bo'lmasa
        try:
            await db.add_Guruhlar(chat_id=chat_id,
                         GroupName=message.chat.title)
        except asyncpg.exceptions.UniqueViolationError:
            pass