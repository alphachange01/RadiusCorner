import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile

from config import TOKEN
from image_processor import ImageProcessor

bot = Bot(token=TOKEN)
dp = Dispatcher()

# 📁 temp folder create
os.makedirs("temp", exist_ok=True)

# ---------------------------
# PHOTO HANDLER (FIXED)
# ---------------------------
@dp.message(F.photo)
async def handle_photo(message: Message):
    print("PHOTO RECEIVED")

    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)

    input_path = "temp/input.jpg"

    await bot.download_file(file.file_path, input_path)

    await message.answer("Processing...")

    try:
        result = ImageProcessor.process(input_path)

        await message.answer_photo(FSInputFile(result))

    except Exception as e:
        await message.answer(f"Error: {e}")


# ---------------------------
# TEXT DEBUG (optional)
# ---------------------------
@dp.message()
async def debug(message: Message):
    print("MSG:", message.content_type)


# ---------------------------
# START BOT
# ---------------------------
async def main():
    print("BOT STARTED 🚀")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
