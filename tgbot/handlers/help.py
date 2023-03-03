from aiogram import Dispatcher
from aiogram.types import Message


async def user_help(message: Message):
    await message.answer(
        f"Пожелания, предложения и иная обратная связь - @German_goncharov")


def register_help(dp: Dispatcher):
    dp.register_message_handler(user_help, commands=["help"], state="*")
