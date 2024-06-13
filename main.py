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
receiver_email = None
message1 = None


def send_button():
    design = [
        [KeyboardButton(text="Send message")],
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Hello {message.from_user.first_name}, enter email address')


@dp.message(F.text.endswith(".com"))
async def get_email(message: Message):
    global receiver_email
    receiver_email = message.text
    await message.answer('Enter the message to send')


@dp.message(lambda message: receiver_email is not None and message.text != receiver_email)
async def send_email(message: Message):
    global message1
    message1 = message.text
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "relaxmusic701@gmail.com"
    password = "xhehnfusvcaomlbu"
    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message1)
        await message.answer('Email sent successfully', reply_markup=send_button())
    except Exception as e:
        await message.answer(f'Failed to send email: {e}')


@dp.message(F.text == "Send message")
async def resend_message(message: Message):
    if receiver_email and message1:
        await send_email(message)


async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
