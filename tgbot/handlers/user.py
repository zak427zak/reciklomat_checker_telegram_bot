from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.services.register_new_user import register_new_user


async def user_start(message: Message):
    register_new_user(message.from_user.id)
    await message.reply("Привет! Это бот для проверки статусов рецикломатов в Белграде (Сербия).\nПока бот работает в тестовом режиме.\nСмотри список доступных команд в меню")


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
