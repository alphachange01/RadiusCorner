import asyncio
import logging
import io

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, BufferedInputFile
from aiogram.filters import Command
from PIL import Image, ImageDraw

TOKEN = "T"

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)


def make_squircle(image: Image.Image, value: int = 150):
    image = image.convert("RGBA")

    w, h = image.size
    size = max(w, h)

    # 🔥 FIX 1: kichik logolarni yo‘qotmaslik uchun upscale
    min_target = int(size * 0.80)

    if image.width < min_target or image.height < min_target:
        scale = min_target / max(image.width, image.height)
        image = image.resize(
            (int(image.width * scale), int(image.height * scale)),
            Image.LANCZOS
        )

    # 📦 square canvas
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))

    # 🎯 center placement
    x = (size - image.width) // 2
    y = (size - image.height) // 2
    canvas.paste(image, (x, y), image)

    # 🔵 squircle / circle control
    value = max(0, min(200, value))
    radius = int((value / 200) * (size // 2))

    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)

    draw.rounded_rectangle(
        (0, 0, size, size),
        radius=radius,
        fill=255
    )

    result = Image.new("RGBA", (size, size))
    result.paste(canvas, (0, 0), mask)

    return result


@dp.message(Command("start"))
async def start(msg: Message):
    await msg.answer(
        "Rasm yubor 📸\n"
        "150 → iPhone squircle 🍎\n"
        "200 → full circle ⚪"
    )


@dp.message(F.photo)
async def handle_photo(msg: Message):
    value = 150

    if msg.caption:
        if "200" in msg.caption:
            value = 200
        elif "150" in msg.caption:
            value = 150

    file = await bot.get_file(msg.photo[-1].file_id)
    file_data = await bot.download_file(file.file_path)

    image = Image.open(file_data)

    result = make_squircle(image, value)

    buffer = io.BytesIO()
    result.save(buffer, format="PNG")
    buffer.seek(0)

    await msg.answer_photo(
        BufferedInputFile(buffer.read(), filename="result.png"),
        caption=f"Done ✨ shape={value}"
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
