from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.services.get_help import get_user_help


async def help(message: Message):
    get_answer = get_user_help(message)
    await message.answer(get_answer, disable_web_page_preview=True)


def register_help(dp: Dispatcher):
    dp.register_message_handler(help, commands=["help"], state="*")
