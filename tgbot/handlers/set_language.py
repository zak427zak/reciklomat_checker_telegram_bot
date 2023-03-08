from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.callbacks import language_callback
from tgbot.keyboards.inline_keyboards import create_languages_keyboard
from tgbot.services.set_language import set_language_service


async def set_language(message: Message):
    languages_keyboard = create_languages_keyboard("update")
    await message.answer(
        "Choose your language:",
        reply_markup=languages_keyboard)


async def updated_language(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    await call.message.answer(set_language_service(call, callback_data.get("id")))


def register_set_language(dp: Dispatcher):
    dp.register_message_handler(set_language, commands=["language"], state="*")
    dp.register_callback_query_handler(updated_language, language_callback.filter(create_or_update="update"), state="*")
