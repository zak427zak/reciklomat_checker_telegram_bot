from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.services.get_all_or_my_reciklomats import get_all_or_my_reciklomats_service


async def all_reciklomats(message: Message):
    resp, code = get_all_or_my_reciklomats_service(message.from_user.id, "all")
    if code == 200:
        for item in resp:
            await message.answer(text=item['text'])
    else:
        await message.answer(text=resp)


def register_all_reciklomats(dp: Dispatcher):
    dp.register_message_handler(all_reciklomats, commands=["all"], state="*")
