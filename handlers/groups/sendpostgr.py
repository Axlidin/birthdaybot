from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import ADMINS
from keyboards.default.menu import Main_menu
from loader import dp, db
from states.sendpost import sendPostGR
from utils.db_api import postgresql as commands
from filters import IsPrivate

@dp.message_handler(IsPrivate(), chat_id=ADMINS , text=['Gr_post'])
async def start_sendPostGR(message: types.Message):
    await message.answer(f"Xabaringizni kiriting: ")
    await sendPostGR.text.set()

@dp.message_handler(IsPrivate(), state=sendPostGR.text)
async def send_text(message: types.Message, state: FSMContext):
    matn = message.text
    markup = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text="Rasm qo'shish", callback_data="add_hpoto"),
                                          InlineKeyboardButton(text="Hujjat qo'shish", callback_data="doc"),
                                          InlineKeyboardButton(text="Video qo'shish", callback_data="add_video"),
                                      ],
                                      [
                                          InlineKeyboardButton(text="Next", callback_data="next"),
                                          InlineKeyboardButton(text="Cancel", callback_data="quit_menu"),
                                      ]
                                  ])
    await state.update_data(text=matn)
    await message.answer(text=matn, reply_markup=markup)
    await sendPostGR.state.set()
@dp.callback_query_handler(text="quit_menu", state=[sendPostGR.text, sendPostGR.video, sendPostGR.state, sendPostGR.photo,
                                                    sendPostGR.document,])
async def quit_menu(call: types.ContentTypes, state: FSMContext):
    await state.finish()
    await call.message.answer("Tizim yuborishni bekor qildi!", reply_markup=Main_menu)

@dp.callback_query_handler(text='next', state=sendPostGR.state)
async def start_send_text(call: types.ContentTypes, state: FSMContext):
    users = await db.select_all_Guruhlar()
    data = await state.get_data()
    text = data.get('text')
    await state.finish()
    senddingMSG = 0
    for user in users:
        try:
            await dp.bot.send_message(chat_id=user[1], text=text)
            senddingMSG += 1
        except Exception:
            continue
    await dp.bot.send_message(chat_id=ADMINS[0], text=f"Xabaringiz {senddingMSG} ta guruhga muvofaqqiyatli yuborildi.")


@dp.callback_query_handler(text="add_hpoto", state=sendPostGR.state)
async def add_photo(call: types.CallbackQuery):
    await call.message.answer("Rasm yuboring!")
    await sendPostGR.photo.set()

@dp.message_handler(IsPrivate(), state=sendPostGR.photo, content_types=types.ContentTypes.PHOTO)
async def sending_text(message: types.Message, state: FSMContext):
    photo_file_id = message.photo[-1].file_id
    await state.update_data(photo=photo_file_id)
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    markup = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text="Next", callback_data="next"),
                                          InlineKeyboardButton(text="Cancel", callback_data="quit"),
                                      ]
                                  ])
    await message.answer_photo(photo=photo, caption=text, reply_markup=markup)

@dp.callback_query_handler(text="next", state=sendPostGR.photo)
async def start(call: types.ContentTypes, state: FSMContext):
    users = await db.select_all_Guruhlar()
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    await state.finish()
    senddingMSG = 0
    for user in users:
        try:
            await dp.bot.send_photo(chat_id=user[1], photo=photo, caption=text)
            await sleep(0.05)
            senddingMSG += 1
        except Exception:
            continue
    await dp.bot.send_message(chat_id=ADMINS[0],
                              text=f"Xabaringiz {senddingMSG} ta guruhga muvofaqqiyatli yuborildi.")


@dp.message_handler(IsPrivate(), state=sendPostGR.photo)
async def no_photo(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text="Cancel", callback_data="quit" )
                                      ]
                                  ])

    await message.answer("Rasm yuboring!", reply_markup=markup)

@dp.callback_query_handler(text="quit", state=[sendPostGR.text, sendPostGR.video, sendPostGR.state, sendPostGR.photo,
                                               sendPostGR.document,])
async def quit(call: types.ContentTypes, state: FSMContext):
    await state.finish()
    await call.message.answer("Tizim yuborishni bekor qildi!", reply_markup=Main_menu)
#document

@dp.callback_query_handler(text="doc", state=sendPostGR.state)
async def add_document(call: types.CallbackQuery):
    await call.message.answer("Hujjat yuboring!")
    await sendPostGR.document.set()

@dp.message_handler(IsPrivate(), state=sendPostGR.document, content_types=types.ContentTypes.DOCUMENT)
async def sending_doc(message: types.Message, state: FSMContext):
    document_file_id = message.document.file_id
    await state.update_data(document=document_file_id)
    data = await state.get_data()
    text = data.get('text')
    document = data.get('document')
    markup = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text="Next", callback_data="next_doc"),
                                          InlineKeyboardButton(text="Cancel", callback_data="quit_doc"),
                                      ]
                                  ])
    await message.answer_document(document=document, caption=text, reply_markup=markup)

@dp.callback_query_handler(text="next_doc", state=sendPostGR.document)
async def start_doc(call: types.ContentTypes, state: FSMContext):
    users = await db.select_all_Guruhlar()
    data = await state.get_data()
    text = data.get('text')
    document = data.get('document')
    await state.finish()
    senddingMSG = 0
    for user in users:
        try:
            await dp.bot.send_document(chat_id=user[1], document=document, caption=text)
            await sleep(0.05)
            senddingMSG += 1
        except Exception:
            continue
    await dp.bot.send_message(chat_id=ADMINS[0],
                              text=f"Xabaringiz {senddingMSG} ta guruhga muvofaqqiyatli yuborildi.")


@dp.message_handler(IsPrivate(), state=sendPostGR.document)
async def no_document(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text="Cancel", callback_data="quit_doc" )
                                      ]
                                  ])

    await message.answer_document("Hujjat yuboring!", reply_markup=markup)

@dp.callback_query_handler(text="quit_doc", state=[sendPostGR.text, sendPostGR.video, sendPostGR.state, sendPostGR.photo, sendPostGR.document,])
async def quit_doc(call: types.ContentTypes, state: FSMContext):
    await state.finish()
    await call.message.answer("Tizim yuborishni bekor qildi!", reply_markup=Main_menu)

#video

@dp.callback_query_handler(text="add_video", state=sendPostGR.state)
async def add_videoument(call: types.CallbackQuery):
    await call.message.answer("Video yuboring!")
    await sendPostGR.video.set()

@dp.message_handler(IsPrivate(), state=sendPostGR.video, content_types=types.ContentTypes.VIDEO)
async def sending_video(message: types.Message, state: FSMContext):
    video_file_id = message.video.file_id
    await state.update_data(video=video_file_id)
    data = await state.get_data()
    text = data.get('text')
    video = data.get('video')
    markup = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text="Next", callback_data="next_video"),
                                          InlineKeyboardButton(text="Cancel", callback_data="quit_video"),
                                      ]
                                  ])
    await message.answer_video(video=video, caption=text, reply_markup=markup)

@dp.callback_query_handler(text="next_video", state=sendPostGR.video)
async def start_video(call: types.ContentTypes, state: FSMContext):
    users = await db.select_all_Guruhlar()
    data = await state.get_data()
    text = data.get('text')
    video = data.get('video')
    await state.finish()
    senddingMSG = 0
    for user in users:
        try:
            await dp.bot.send_video(chat_id=user[1], video=video, caption=text)
            await sleep(0.05)
            senddingMSG += 1
        except Exception:
            continue
    await dp.bot.send_message(chat_id=ADMINS[0],
                              text=f"Xabaringiz {senddingMSG} ta guruhga muvofaqqiyatli yuborildi.")


@dp.message_handler(IsPrivate(), state=sendPostGR.video)
async def no_videoument(message: types.Message):
    markup = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text="Cancel", callback_data="quit_video" )
                                      ]
                                  ])

    await message.answer("Video yuboring!", reply_markup=markup)

@dp.callback_query_handler(text="quit_video", state=[sendPostGR.text, sendPostGR.video, sendPostGR.state, sendPostGR.photo, sendPostGR.document,])
async def quit_video(call: types.ContentTypes, state: FSMContext):
    await state.finish()
    await call.message.answer("Tizim yuborishni bekor qildi!", reply_markup=Main_menu)
