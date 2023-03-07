from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.callback_datas import languages_callback
from tgbot.keyboards.inline import create_languages_keyboard
from tgbot.services.register_new_user import register_new_user


async def user_start(message: Message):
    new_keyboard = create_languages_keyboard()
    await message.answer(
        "Hello! Choose your language:",
        reply_markup=new_keyboard)


async def choose_reciklomat(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    await call.message.answer(register_new_user(call, callback_data.get("id")))


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_callback_query_handler(choose_reciklomat, languages_callback.filter(), state="*")
