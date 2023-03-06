from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.services.check import check


async def get_current_status(message: Message):
    resp = check(message.from_user.id, "some")
    for item in resp:
        await message.answer(text=item['text'])


def register_check_status(dp: Dispatcher):
    dp.register_message_handler(get_current_status, commands=["check"], state="*")
