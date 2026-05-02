import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8543852141:AAEfp9wJiLvacB3drRYfiOOTP3zIIe3gTkA"

bot = Bot(TOKEN)
dp = Dispatcher()

# user state (oddiy storage)
user_image = {}


# ------------------------
# INLINE BUTTONS
# ------------------------
def radius_kb():
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
    path = "temp.jpg"

    await bot.download_file(file.file_path, path)

    user_image[message.from_user.id] = path

    await message.answer(
        "Radius tanla:",
        reply_markup=radius_kb()
    )


# ------------------------
# CALLBACK HANDLER
# ------------------------
@dp.callback_query(F.data.startswith("r_"))
async def radius(call: CallbackQuery):

    r = int(call.data.split("_")[1])
    uid = call.from_user.id

    path = user_image.get(uid)

    if not path:
        await call.message.answer("Rasm topilmadi")
        return

    # process import (simple inline logic)
    import cv2
    import numpy as np

    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    h, w = img.shape[:2]

    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

    scale = 0.85
    nw, nh = int(w*scale), int(h*scale)

    resized = cv2.resize(img, (nw, nh))

    canvas = np.zeros((h, w, 4), dtype=np.uint8)

    x, y = (w-nw)//2, (h-nh)//2
    canvas[y:y+nh, x:x+nw] = resized

    # squircle mask with radius
    mask = np.zeros((h, w), dtype=np.uint8)

    rect = np.zeros((h, w), dtype=np.uint8)
    cv2.rectangle(rect, (r, r), (w-r, h-r), 255, -1)

    cv2.circle(rect, (r, r), r, 255, -1)
    cv2.circle(rect, (w-r, r), r, 255, -1)
    cv2.circle(rect, (r, h-r), r, 255, -1)
    cv2.circle(rect, (w-r, h-r), r, 255, -1)

    mask = cv2.GaussianBlur(rect, (7, 7), 0)

    canvas[:, :, 3] = mask

    out = "out.png"
    cv2.imwrite(out, canvas)

    await call.message.answer_photo(FSInputFile(out))
    await call.answer()


# ------------------------
# TEXT
# ------------------------
@dp.message()
async def text(message: Message):
    await message.answer("Rasm yubor 🙂")


# ------------------------
# START
# ------------------------
async def main():
    await dp.start_polling(bot)

asyncio.run(main())
