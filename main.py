import logging

from PIL import Image
import io

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Command, CommandStart
from asyncio import sleep

from config import BOT_TOKEN, ADMIN_ID, HOST, PORT, PASSWORD, USER, DATABESE
from create import images_create
from db import DataBase

# Configure logging
logging.basicConfig(level=logging.INFO)

bottons = types.InlineKeyboardMarkup()
btn = types.InlineKeyboardButton(text="Kanal", url="https://t.me/moorfo_uz")
confirm_btn = types.InlineKeyboardButton(text="Tastiqlash", callback_data='t')

bottons.add(btn)
bottons.add(confirm_btn)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
db = DataBase(host=HOST, port=PORT, database=DATABESE, user="postgres", password=PASSWORD)

channel_id = "@moorfo_uz"

def check_sub_channel(chat_member):
    if chat_member['status'] != 'left':
        return True
    else:
        return False

@dp.message_handler(CommandStart())
async def send_welcome(message: types.Message):
    user = message.from_user.id
    chat_id = message.from_user.id
    if check_sub_channel(await bot.get_chat_member(chat_id=channel_id, user_id=user)):
        await message.reply(f"Assalomu aleykum {message.from_user.first_name}\n"
                        f"siz qanday rasm chizishimni hohlaysiz.")
    else:
        await bot.send_message(chat_id, f"Assalomu aleykum {message.from_user.first_name}\n botda foydalish uchun homiy kanalga azo bo'ling.", reply_markup=bottons)
        
    
    user_id = message.from_user.id
    username = message.from_user.full_name
    if not db.user_exists(user_id):
        db.create_user(user_id)
        await bot.send_message(ADMIN_ID, "🆕 Yangi Foydalanuvchi! \n"
                                         f"Umumiy: [{len(db.get_users())}] \n"
                                         f"Ismi: {username}")


@dp.message_handler(Command('admin'))
async def send_admin(msg: types.Message):
    users = db.get_users()
    chat_id = msg.chat.id
    await msg.answer(f'Foydalanuvchilar: {len(users)}')

@dp.message_handler(Command('token'))
async def send_admin(msg: types.Message):
    text = msg.text
    if text.startswith('/token '):
       token = text.split('/token ')[1]
    
    if len(token) > 11:
        db.create_token(token=token)
        await msg.answer("token qo'shidi.")

@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def send_photo(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.full_name
    
    if check_sub_channel(await bot.get_chat_member(chat_id=channel_id, user_id=user_id)):
        if not db.user_exists(user_id):
            db.create_user(user_id)
            await bot.send_message(ADMIN_ID, "🆕 Yangi Foydalanuvchi! \n"
                                            f"Umumiy: [{len(db.get_users())}] \n"
                                            f"Ismi: {username}")
        passbar = await bot.send_message(message.from_user.id, text="Rasm yaratilmoqda... \n 2 ta rasm yaratmoda. Bu biroz vaqt olishi mumkin.")
        await bot.send_chat_action(chat_id=user_id, action=types.ChatActions.UPLOAD_PHOTO)
        go = True
        image_group = types.MediaGroup()
        for i in range(2):
            await bot.send_chat_action(chat_id=user_id, action=types.ChatActions.UPLOAD_PHOTO)
            img = images_create(message.text, file=i)
            image_group.attach_photo(open(f"image{i}.png", 'rb'))
            await passbar.delete()
            await message.answer_media_group(image_group)
    else:
        await message.answer(f"Botda foydalish uchun homiy kanalga azo bo'ling.", reply_markup=bottons)


@dp.message_handler(content_types=types.ContentTypes.ANY)
async def send_err(msg: types.Message):
    user_id = msg.from_user.id
    username = msg.from_user.full_name
    if not db.user_exists(user_id):
        db.create_user(user_id)
        await bot.send_message(ADMIN_ID, "🆕 Yangi Foydalanuvchi! \n"
                                         f"Umumiy: [{len(db.get_users())}] \n"
                                         f"Ismi: {username}")
    await msg.answer("Siz mavjud bolmagan buyruq berdigiz.")


@dp.callback_query_handler(text='t')
async def confirm(call: types.CallbackQuery):
    user = call.from_user.id
    if check_sub_channel(await bot.get_chat_member(chat_id=channel_id, user_id=user)):
        await call.message.delete()
        await call.message.answer(f"Siz qanday rasm chizishimni hohlaysiz.")
    else:
        await call.message.answer(f"Botda foydalish uchun homiy kanalga azo bo'ling.", reply_markup=bottons)
        

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
