from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.services.register_new_user import register_new_user


async def user_start(message: Message):
    register_new_user(message.from_user.id)
    await message.reply(
        "Привет! Это бот для проверки статусов рецикломатов в Белграде (Сербия).\nПока бот работает в тестовом режиме.\n\nБот позволяет проверять заполненность рецикломатов в реальном времени, а так же собрать свой вишлист рецикломатов, которые будет отслеживать. Если один из рецикломатов в вашем вишлисте изменит статус на освободился - вы тут же получите уведомление")


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
