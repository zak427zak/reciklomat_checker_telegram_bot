from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.services.check import check


async def get_all_status(message: Message):
    resp = check(message.from_user.id, "all")
    for item in resp:
        await message.answer(text=item['text'])


def register_all_status(dp: Dispatcher):
    dp.register_message_handler(get_all_status, commands=["all"], state="*")
