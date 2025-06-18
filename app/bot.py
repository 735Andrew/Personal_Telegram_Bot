import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Salute! Let`s calculate the length of your messages.")


@dp.message()
async def calculating_message_length(message: Message):
    await message.answer(f"You sent a message of {len(message.text)} characters")


async def main(token: str):
    bot = Bot(token=token)
    await dp.start_polling(bot)


def telegram_bot_creation(token: str):
    try:
        asyncio.run(main(token))
    except KeyboardInterrupt:
        print("Exit")
