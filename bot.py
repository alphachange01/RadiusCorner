import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from PIL import Image, ImageDraw, ImageFilter

BOT_TOKEN = ""

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

user_images = {}


# ---------- RADIUS ENGINE ----------
def apply_radius(img_path, value):
    img = Image.open(img_path).convert("RGBA")
    w, h = img.size

    v = max(50, min(int(value), 200))

    # mapping (Canva-style feel)
    if v <= 70:
        radius = int(min(w, h) * 0.15)
    elif v <= 120:
        radius = int(min(w, h) * 0.3)
    elif v <= 170:
        radius = int(min(w, h) * 0.42)
    else:
        radius = int(min(w, h) * 0.5)  # circle mode

    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)

    draw.rounded_rectangle(
        (0, 0, w, h),
        radius=radius,
        fill=255
    )

    # smooth edges (Canva-like feel)
    mask = mask.filter(ImageFilter.GaussianBlur(2))

    img.putalpha(mask)

    out_path = img_path.replace(".png", f"_{value}.png")
    img.save(out_path)

    return out_path


# ---------- SAVE IMAGE ----------
@dp.message()
async def save_photo(message: types.Message):
    if not message.photo:
        return

    file = await bot.get_file(message.photo[-1].file_id)
    data = await bot.download_file(file.file_path)

    path = f"{TEMP_DIR}/{message.from_user.id}.png"

    with open(path, "wb") as f:
        f.write(data.read())

    user_images[message.from_user.id] = path

    await message.answer("✅ Rasm saqlandi. Endi /50 /100 /150 /200 yoz.")


# ---------- APPLY RADIUS ----------
@dp.message(Command("50", "100", "150", "200"))
async def process(message: types.Message):
    user_id = message.from_user.id

    if user_id not in user_images:
        await message.answer("Avval rasm yubor 🙂")
        return

    value = int(message.text.replace("/", ""))

    img_path = user_images[user_id]
    out = apply_radius(img_path, value)

    await message.answer_photo(FSInputFile(out))


# ---------- START ----------
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
