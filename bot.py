from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

from config import TOKEN
from image_processor import ImageProcessor

bot = Bot(token=TOKEN)
dp = Dispatcher()

# TEMP storage (simple)
user_data = {}

# ------------------------
# INLINE BUTTONS
# ------------------------
def radius_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="50", callback_data="r_50"),
            InlineKeyboardButton(text="100", callback_data="r_100"),
        ],
        [
            InlineKeyboardButton(text="150", callback_data="r_150"),
            InlineKeyboardButton(text="200", callback_data="r_200"),
        ]
    ])

# ------------------------
# PHOTO HANDLER
# ------------------------
@dp.message(F.photo)
async def photo(message: Message):
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)

    path = "temp/input.jpg"
    await bot.download_file(file.file_path, path)

    user_data[message.from_user.id] = path

    await message.answer(
        "Radius tanla:",
        reply_markup=radius_keyboard()
    )

# ------------------------
# CALLBACK
# ------------------------
@dp.callback_query(F.data.startswith("r_"))
async def set_radius(call: CallbackQuery):

    radius = int(call.data.split("_")[1])
    user_id = call.from_user.id

    image_path = user_data.get(user_id)

    if not image_path:
        await call.message.answer("Rasm topilmadi")
        return

    result = ImageProcessor.process(image_path, radius)

    await call.message.answer_photo(FSInputFile(result))

    await call.answer()

# ------------------------
# START
# ------------------------
async def main():
    print("BOT STARTED")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
