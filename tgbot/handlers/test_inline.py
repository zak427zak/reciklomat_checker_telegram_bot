from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.callback_datas import reciklomat_callback
from tgbot.keyboards.inline import create_new_keyboard
from tgbot.services.manage_wishlist import add_or_remove_from_wishlist


async def show_wishlist(message: Message):
    new_keyboard, text = create_new_keyboard(message.from_user.id)
    await message.answer(
        text,
        reply_markup=new_keyboard)


async def choose_reciklomat(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    address = callback_data.get("address")
    add_or_remove_from_wishlist(call.from_user.id, address)
    new_keyboard, text = create_new_keyboard(call.from_user.id)
    await call.message.edit_reply_markup(new_keyboard)


def register_show_items(dp: Dispatcher):
    dp.register_message_handler(show_wishlist, commands=["wishlist"], state="*")
    dp.register_callback_query_handler(choose_reciklomat, reciklomat_callback.filter(), state="*")
