from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.services.get_answer_service import get_user_help


async def user_help(message: Message):
    get_answer = get_user_help(message)
    await message.answer(get_answer, disable_web_page_preview=True)


def register_help(dp: Dispatcher):
    dp.register_message_handler(user_help, commands=["help"], state="*")
