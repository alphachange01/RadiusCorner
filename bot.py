import asyncio
import os
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile

from shape_engine import apply_radius

# ---------------- LOGGING ----------------
logging.basicConfig(level=logging.INFO)

print("BOT STARTED 🚀")

# ---------------- TOKEN ----------------
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise Exception("BOT_TOKEN topilmadi!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

user_images = {}


# ---------------- START COMMAND ----------------
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 Bot ishlayapti!\n\n"
        "📸 Rasm yubor\n"
        "🔘 Keyin /50 /100 /150 /200 yoz"
    )


# ---------------- SAVE IMAGE ----------------
@dp.message(lambda m: m.photo)
async def handle_photo(message: types.Message):
    file = await bot.get_file(message.photo[-1].file_id)
    data = await bot.download_file(file.file_path)

    path = f"{TEMP_DIR}/{message.from_user.id}.png"

    with open(path, "wb") as f:
        f.write(data.read())

    user_images[message.from_user.id] = path

    await message.answer("✅ Rasm saqlandi. Endi /50 /100 /150 /200 yoz")


# ---------------- APPLY RADIUS ----------------
@dp.message(Command("50", "100", "150", "200"))
async def apply(message: types.Message):
    uid = message.from_user.id

    if uid not in user_images:
        await message.answer("❌ Avval rasm yubor")
        return

    value = int(message.text.replace("/", ""))

    out = apply_radius(user_images[uid], value)

    await message.answer_photo(FSInputFile(out))


# ---------------- DEBUG MESSAGE ----------------
@dp.message()
async def fallback(message: types.Message):
    logging.info(f"Unknown message: {message.text}")


# ---------------- MAIN ----------------
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
