import os
import uuid
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import asyncio

from shape_engine import apply_radius

BOT_TOKEN = "YOUR_BOT_TOKEN"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

user_files = {}

@dp.message(Command("start"))
async def start(msg: Message):
    await msg.answer("Rasm yubor. Keyin /50 /100 /150 /200 yozasan.")

@dp.message(lambda m: m.photo)
async def get_photo(msg: Message):
    file_id = msg.photo[-1].file_id
    file = await bot.get_file(file_id)

    path = f"tmp/{uuid.uuid4()}.png"
    os.makedirs("tmp", exist_ok=True)

    await bot.download_file(file.file_path, path)

    user_files[msg.from_user.id] = path

    await msg.answer("Qabul qilindi. Endi /50 /100 /150 /200 yubor.")

@dp.message(lambda m: m.text and m.text.startswith("/"))
async def process(msg: Message):
    if msg.from_user.id not in user_files:
        return await msg.answer("Avval rasm yubor.")

    value = msg.text.replace("/", "")

    try:
        out = apply_radius(user_files[msg.from_user.id], value)
    except Exception as e:
        return await msg.answer(f"Xato: {e}")

    await msg.answer_photo(types.FSInputFile(out))

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
