import asyncio
import logging
import io

from aiogram import Bot, Dispatcher, F, types
from aiogram.types import Message, BufferedInputFile
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from PIL import Image, ImageDraw, ImageFilter, ImageOps

TOKEN = "8543852141:AAEfp9wJiLvacB3drRYfiOOTP3zIIe3gTkA"

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

# user memory
user_data = {}  # image
zoom_data = {}  # zoom level per user


# 🔥 IMAGE ENGINE (ZOOM CONTROLLED)
def make_squircle(image: Image.Image, value: int = 150, zoom: float = 1.0):
    image = image.convert("RGBA")

    size = max(image.size)

    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))

    # 🌫 background (light blur)
    bg = ImageOps.fit(image, (size, size))
    bg = bg.filter(ImageFilter.GaussianBlur(12))
    canvas.paste(bg, (0, 0))

    # 🎯 ZOOM CONTROL (THIS IS KEY PART)
    base_scale = min((size * 0.7) / image.width, (size * 0.7) / image.height)

    scale = base_scale * zoom

    new_w = int(image.width * scale)
    new_h = int(image.height * scale)

    fg = image.resize((new_w, new_h), Image.LANCZOS)

    x = (size - new_w) // 2
    y = (size - new_h) // 2

    canvas.paste(fg, (x, y), fg)

    # 🔵 squircle
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


# 🎛 BUTTONS (ZOOM + SHAPE)
def get_keyboard():
    kb = InlineKeyboardBuilder()

    kb.button(text="➖ Zoom -", callback_data="zoom_minus")
    kb.button(text="➕ Zoom +", callback_data="zoom_plus")

    kb.button(text="🔵 100", callback_data="shape_100")
    kb.button(text="🍎 150", callback_data="shape_150")
    kb.button(text="⚪ 200", callback_data="shape_200")

    kb.adjust(2, 3)
    return kb.as_markup()


@dp.message(Command("start"))
async def start(msg: Message):
    await msg.answer("📸 Rasm yubor, keyin zoom + / - va shape tanla")


@dp.message(F.photo)
async def handle_photo(msg: Message):
    file = await bot.get_file(msg.photo[-1].file_id)
    file_data = await bot.download_file(file.file_path)

    image = Image.open(file_data)

    user_data[msg.from_user.id] = image
    zoom_data[msg.from_user.id] = 1.0  # default zoom

    await msg.answer("Control panel 👇", reply_markup=get_keyboard())


# 🎛 ZOOM + SHAPE HANDLER
@dp.callback_query()
async def callback(call: types.CallbackQuery):
    user_id = call.from_user.id

    if user_id not in user_data:
        await call.message.answer("Avval rasm yubor 😅")
        return

    image = user_data[user_id]
    zoom = zoom_data.get(user_id, 1.0)

    # ➖ zoom out
    if call.data == "zoom_minus":
        zoom = max(0.5, zoom - 0.1)
        zoom_data[user_id] = zoom
        await call.answer(f"Zoom: {zoom:.1f}")
        return

    # ➕ zoom in
    if call.data == "zoom_plus":
        zoom = min(2.0, zoom + 0.1)
        zoom_data[user_id] = zoom
        await call.answer(f"Zoom: {zoom:.1f}")
        return

    # 🎨 shape render
    if call.data.startswith("shape_"):
        value = int(call.data.split("_")[1])

        result = make_squircle(image, value, zoom)

        buffer = io.BytesIO()
        result.save(buffer, format="PNG")
        buffer.seek(0)

        await call.message.answer_photo(
            BufferedInputFile(buffer.read(), filename="icon.png"),
            caption=f"✨ shape={value} | zoom={zoom:.1f}"
        )

        await call.answer()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
