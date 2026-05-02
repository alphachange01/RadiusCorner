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

# memory (last image per user)
user_data = {}


# 🔥 PRO IMAGE ENGINE (APPLE STYLE + BLUR BACKGROUND)
def make_squircle(image: Image.Image, value: int = 150):
    image = image.convert("RGBA")

    size = max(image.size)

    # 📦 canvas
    canvas = Image.new("RGBA", (size, size))

    # 🌫 BACKGROUND (blur fill)
    bg = ImageOps.fit(image, (size, size))
    bg = bg.filter(ImageFilter.GaussianBlur(30))
    canvas.paste(bg, (0, 0))

    # 🎯 FOREGROUND (safe scale, no stretch)
    scale = min((size * 0.75) / image.width, (size * 0.75) / image.height)

    new_w = int(image.width * scale)
    new_h = int(image.height * scale)

    fg = image.resize((new_w, new_h), Image.LANCZOS)

    x = (size - new_w) // 2
    y = (size - new_h) // 2

    canvas.paste(fg, (x, y), fg)

    # 🔵 squircle radius control
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


# 🎛 INLINE BUTTONS
def get_keyboard():
    kb = InlineKeyboardBuilder()

    kb.button(text="🔵 100", callback_data="shape_100")
    kb.button(text="🍎 150", callback_data="shape_150")
    kb.button(text="⚪ 200", callback_data="shape_200")

    kb.adjust(3)
    return kb.as_markup()


# /start
@dp.message(Command("start"))
async def start(msg: Message):
    await msg.answer(
        "📸 Rasm yubor\n"
        "Shape tanla:\n"
        "🔵 100 | 🍎 150 | ⚪ 200"
    )


# photo handler
@dp.message(F.photo)
async def handle_photo(msg: Message):
    file = await bot.get_file(msg.photo[-1].file_id)
    file_data = await bot.download_file(file.file_path)

    image = Image.open(file_data)

    user_data[msg.from_user.id] = image

    await msg.answer(
        "Shape tanla 👇",
        reply_markup=get_keyboard()
    )


# callback handler
@dp.callback_query(F.data.startswith("shape_"))
async def process_shape(call: types.CallbackQuery):
    value = int(call.data.split("_")[1])

    image = user_data.get(call.from_user.id)

    if not image:
        await call.message.answer("Avval rasm yubor 😅")
        return

    result = make_squircle(image, value)

    buffer = io.BytesIO()
    result.save(buffer, format="PNG")
    buffer.seek(0)

    await call.message.answer_photo(
        BufferedInputFile(buffer.read(), filename="icon.png"),
        caption=f"✨ Done | shape={value}"
    )

    await call.answer()


# run bot
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
