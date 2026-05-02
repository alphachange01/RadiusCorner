import asyncio
import cv2
import numpy as np

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8543852141:AAEfp9wJiLvacB3drRYfiOOTP3zIIe3gTkA"

bot = Bot(TOKEN)
dp = Dispatcher()

user_images = {}

# ---------------- KEYBOARD ----------------
def kb():
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

# ---------------- IMAGE RECEIVER ----------------
@dp.message(F.photo)
async def photo(message: Message):
    photo = message.photo[-1]

    file = await bot.get_file(photo.file_id)

    path = "input.jpg"
    await bot.download_file(file.file_path, path)

    user_images[message.from_user.id] = path

    await message.answer("Radius tanla:", reply_markup=kb())


# ---------------- SQUIRCLE FUNCTION ----------------
def squircle(img, r):

    h, w = img.shape[:2]

    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

    # no distortion resize
    scale = min(w / img.shape[1], h / img.shape[0]) * 0.85

    nw, nh = int(img.shape[1] * scale), int(img.shape[0] * scale)

    resized = cv2.resize(img, (nw, nh), cv2.INTER_AREA)

    canvas = np.zeros((h, w, 4), dtype=np.uint8)

    x = (w - nw) // 2
    y = (h - nh) // 2

    canvas[y:y+nh, x:x+nw] = resized

    # REAL SQUIRCLE MASK
    mask = np.ones((h, w), dtype=np.uint8) * 255

    cv2.circle(mask, (r, r), r, 0, -1)
    cv2.circle(mask, (w-r, r), r, 0, -1)
    cv2.circle(mask, (r, h-r), r, 0, -1)
    cv2.circle(mask, (w-r, h-r), r, 0, -1)

    canvas[:, :, 3] = mask

    return canvas


# ---------------- CALLBACK ----------------
@dp.callback_query(F.data.startswith("r_"))
async def callback(call: CallbackQuery):

    r = int(call.data.split("_")[1])

    path = user_images.get(call.from_user.id)

    if not path:
        await call.message.answer("Rasm yo‘q")
        return

    img = cv2.imread(path)

    result = squircle(img, r)

    out = "output.png"
    cv2.imwrite(out, result)

    await call.message.answer_photo(FSInputFile(out))

    await call.answer()


# ---------------- START ----------------
async def main():
    print("BOT STARTED 🚀")
    await dp.start_polling(bot)

asyncio.run(main())
