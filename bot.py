import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile

TOKEN = "8543852141:AAEfp9wJiLvacB3drRYfiOOTP3zIIe3gTkA"

bot = Bot(TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)


@dp.message(F.photo)
async def photo(message: Message):
    try:
        photo = message.photo[-1]
        await bot.download(photo, destination="temp.jpg")
        await message.answer_photo(FSInputFile("temp.jpg"))
    except Exception as e:
        await message.answer("Error occurred")


@dp.message()
async def echo(message: Message):
    await message.answer(message.text or "no text")


async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


asyncio.run(main())
