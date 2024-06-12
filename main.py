import asyncio
import logging
import smtplib
import ssl
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html, F

from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup
from dotenv import load_dotenv

load_dotenv()
TOKEN = getenv('TOKEN')
dp = Dispatcher()
global receiver_email, message1


def send_button():
    design = [
        [
            KeyboardButton(text="Send message" ,callback_data="sended"),
        ],
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'hello {message.from_user.first_name} enter email address')


@dp.message(F.text.endswith(".com"))
async def send_email(message: Message):
    await message.answer(f'enter message email')


@dp.message(F.text, message=F.text)
async def send_message(message: Message):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "relaxmusic701@gmail.com"
    password = "lebhyylfazaggiri"
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
    await message.answer(f'push ', reply_markup=send_button())
@dp.callback_query(F.callback.send_button())
async def send_button(message: CallbackQuery):
    await message.answer(f'seded message', reply_markup=send_button())


async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
