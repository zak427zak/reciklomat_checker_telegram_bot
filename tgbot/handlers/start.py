from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.callbacks import language_callback
from tgbot.keyboards.inline_keyboards import create_languages_keyboard
from tgbot.services.register_user import register_user_service


async def start(message: Message):
    languages_keyboard = create_languages_keyboard("create")
    await message.answer(
        "Hello! Choose your language:",
        reply_markup=languages_keyboard)


async def choose_language(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    await call.message.answer(register_user_service(call, callback_data.get("id")))


def register_start(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"], state="*")
    dp.register_callback_query_handler(choose_language, language_callback.filter(create_or_update="create"), state="*")
