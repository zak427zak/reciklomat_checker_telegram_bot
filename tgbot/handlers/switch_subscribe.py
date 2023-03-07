from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.services.status import status_notifications
from tgbot.services.switch import switch_notifications


async def turn_on(message: Message):
    resp = switch_notifications(message.from_user.id, "on")
    await message.answer(resp)


async def turn_off(message: Message):
    resp = switch_notifications(message.from_user.id, "off")
    await message.answer(resp)


async def turn_status(message: Message):
    resp = status_notifications(message)
    await message.answer(resp)


def register_switch(dp: Dispatcher):
    dp.register_message_handler(turn_on, commands=["on"], state="*")
    dp.register_message_handler(turn_off, commands=["off"], state="*")
    dp.register_message_handler(turn_status, commands=["status"], state="*")