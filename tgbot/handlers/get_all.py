from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.services.check import check


async def get_all_status(message: Message):
    resp, code = check(message.from_user.id, "all")
    await message.answer(resp)


def register_all_status(dp: Dispatcher):
    dp.register_message_handler(get_all_status, commands=["all"], state="*")
