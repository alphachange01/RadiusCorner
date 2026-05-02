import asyncio
import cv2
import numpy as np

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8543852141:AAEfp9wJiLvacB3drRYfiOOTP3zIIe3gTkA"

bot = Bot(TOKEN)
dp = Dispatcher()

user_img = {}


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


# ---------------- PHOTO ----------------
@dp.message(F.photo)
async def photo(message: Message):
    photo = message.photo[-1]

    file = await bot.get_file(photo.file_id)

    path = "input.jpg"
    await bot.download_file(file.file_path, path)

    user_img[message.from_user.id] = path

    await message.answer("Radius tanla:", reply_markup=kb())


# ---------------- PROCESS ----------------
def process(path, r):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)

    h, w = img.shape[:2]

    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

    scale = 0.85
    nw, nh = int(w * scale), int(h * scale)

    resized = cv2.resize(img, (nw, nh))

    canvas = np.zeros((h, w, 4), dtype=np.uint8)

    x, y = (w-nw)//2, (h-nh)//2
    canvas[y:y+nh, x:x+nw] = resized

    # SQUIRCLE MASK (FIXED)
    rect = np.zeros((h, w), dtype=np.uint8)

    cv2.rectangle(rect, (r, r), (w-r, h-r), 255, -1)

    cv2.circle(rect, (r, r), r, 255, -1)
    cv2.circle(rect, (w-r, r), r, 255, -1)
    cv2.circle(rect, (r, h-r), r, 255, -1)
    cv2.circle(rect, (w-r, h-r), r, 255, -1)

    mask = cv2.GaussianBlur(rect, (9, 9), 0)

    canvas[:, :, 3] = mask

    out = "out.png"
    cv2.imwrite(out, canvas)

    return out


# ---------------- CALLBACK ----------------
@dp.callback_query(F.data.startswith("r_"))
async def cb(call: CallbackQuery):

    r = int(call.data.split("_")[1])

    path = user_img.get(call.from_user.id)

    if not path:
        await call.message.answer("Rasm yo‘q")
        return

    out = process(path, r)

    await call.message.answer_photo(FSInputFile(out))

    await call.answer()


# ---------------- START ----------------
async def main():
    print("BOT STARTED")
    await dp.start_polling(bot)


asyncio.run(main())
