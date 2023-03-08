from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.services.get_subscription_status import get_subscription_status
from tgbot.services.switch_subscription import switch_subscription_service


async def turn_on_notifications(message: Message):
    resp = switch_subscription_service(message.from_user.id, "on")
    await message.answer(resp)


async def turn_off_notifications(message: Message):
    resp = switch_subscription_service(message.from_user.id, "off")
    await message.answer(resp)


async def get_notifications_status(message: Message):
    resp = get_subscription_status(message)
    await message.answer(resp)


def register_manage_subscription(dp: Dispatcher):
    dp.register_message_handler(turn_on_notifications, commands=["on"], state="*")
    dp.register_message_handler(turn_off_notifications, commands=["off"], state="*")
    dp.register_message_handler(get_notifications_status, commands=["status"], state="*")
