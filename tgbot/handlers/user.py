from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.services.register_new_user import register_new_user


async def user_intro(message: Message):
    register_new_user(message, message.from_user.locale.language)
    await message.answer(
        f"Привет! Это бот для проверки статусов рецикломатов в Белграде (Сербия).\n\nБот позволяет проверять заполненность всех рецикломатов в реальном времени - команда /all\n\nА ещё можно собрать свой вишлист рецикломатов, которые бот будет отслеживать. Если один из рецикломатов в вашем вишлисте изменит статус на освободился - вы тут же получите уведомление.\n\nДля работы с вишлистом используйте /wishlist\nПроверить статус рецикломатов в вишлисте можно командой /check\n\nВсе доступные команды вы найдете в меню")


def register_intro(dp: Dispatcher):
    dp.register_message_handler(user_intro, commands=["intro"], state="*")
