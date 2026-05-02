import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from aiogram.enums import ContentType

from config import TOKEN
from image_processor import ImageProcessor
from utils import clean_file

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ------------------------
# PHOTO HANDLER
# ------------------------
@dp.message(F.content_type == ContentType.PHOTO)
async def handle_photo(message: Message):

    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)

    input_path = "temp/input.jpg"
    output_path = "temp/output.png"

    await bot.download_file(file.file_path, input_path)

    result = ImageProcessor.process(input_path, shape="squircle")

    await message.answer_photo(FSInputFile(result))

    clean_file(input_path)


# ------------------------
# START BOT
# ------------------------
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
