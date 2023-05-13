import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Command, CommandStart
from asyncio import sleep

from config import BOT_TOKEN, ADMIN_ID, HOST, PORT, PASSWORD, USER, DATABESE
from create import images_create
from db import DataBase

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
db = DataBase(host=HOST, port=PORT, database=DATABESE, user="postgres", password=PASSWORD)


@dp.message_handler(CommandStart())
async def send_welcome(message: types.Message):
    await message.reply(f"Assalomu aleykum {message.from_user.first_name}\n"
                        f"siz qanday rasm chizishimni hohlaysiz")
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


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def send_photo(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.full_name
    if not db.user_exists(user_id):
        db.create_user(user_id)
        await bot.send_message(ADMIN_ID, "🆕 Yangi Foydalanuvchi! \n"
                                         f"Umumiy: [{len(db.get_users())}] \n"
                                         f"Ismi: {username}")
    passbar = await bot.send_message(message.from_user.id, text=10*'⬜'+'0%')
    img = images_create(message.text)
    for i in range(1, 11):
        green = i*'🟩'
        white = (10-i) * '⬜'
        await bot.send_chat_action(message.from_user.id, types.ChatActions.UPLOAD_PHOTO)
        await passbar.edit_text(f"{green}{white} {i*10}%")
    await passbar.delete()
    await message.answer_photo(img,
                               caption='Sizning rasmigiz.\n \nAgar rasm siz hohlaganday'
                                       ' bo\'lmasa matn Ingliz tilida yozing.')


@dp.message_handler(content_types=types.ContentTypes.ANY)
async def send_err(msg: types.Message):
    user_id = message.from_user.id
    username = message.from_user.full_name
    if not db.user_exists(user_id):
        db.create_user(user_id)
        await bot.send_message(ADMIN_ID, "🆕 Yangi Foydalanuvchi! \n"
                                         f"Umumiy: [{len(db.get_users())}] \n"
                                         f"Ismi: {username}")
    await msg.answer("Siz mavjud bolmagan buyruq berdigiz.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
