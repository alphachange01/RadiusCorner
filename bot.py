import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, BufferedInputFile
from aiogram.filters import Command
from PIL import Image, ImageDraw
import io

TOKEN = "8543852141:AAEfp9wJiLvacB3drRYfiOOTP3zIIe3gTkA"

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)


def make_squircle(image: Image.Image, value: int = 150):
    image = image.convert("RGBA")
    w, h = image.size

    # normalize value (0-200)
    value = max(0, min(200, value))

    # radius calculation:
    # 200 -> full circle
    # 150 -> iPhone style squircle
    radius = int((value / 200) * (min(w, h) // 2))

    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)

    draw.rounded_rectangle(
        (0, 0, w, h),
        radius=radius,
        fill=255
    )

    result = Image.new("RGBA", (w, h))
    result.paste(image, (0, 0), mask)

    return result


@dp.message(Command("start"))
async def start(msg: Message):
    await msg.answer(
        "Rasm yubor va men uni squircle qilaman 😎\n"
        "Yoki /shape 150 yoki 200 yoz"
    )


@dp.message(Command("shape"))
async def shape_cmd(msg: Message):
    try:
        value = int(msg.text.split()[1])
    except:
        value = 150

    await msg.answer(f"OK, shape value: {value}")


@dp.message(F.photo)
async def handle_photo(msg: Message):
    # default shape
    value = 150

    if msg.caption:
        try:
            if "200" in msg.caption:
                value = 200
            elif "150" in msg.caption:
                value = 150
        except:
            pass

    file = await bot.get_file(msg.photo[-1].file_id)
    file_data = await bot.download_file(file.file_path)

    image = Image.open(file_data)

    result = make_squircle(image, value)

    buffer = io.BytesIO()
    result.save(buffer, format="PNG")
    buffer.seek(0)

    await msg.answer_photo(
        BufferedInputFile(buffer.read(), filename="squircle.png"),
        caption=f"Done ✨ shape={value}"
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
