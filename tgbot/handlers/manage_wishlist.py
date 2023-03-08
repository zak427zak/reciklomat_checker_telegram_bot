from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.callbacks import reciklomat_callback
from tgbot.keyboards.inline_keyboards import create_manage_wishlist_keyboard
from tgbot.services.add_or_remove_item import add_or_remove_item_service


async def show_wishlist(message: Message):
    new_keyboard, text = create_manage_wishlist_keyboard(message.from_user.id)
    await message.answer(
        text,
        reply_markup=new_keyboard)


async def add_or_remove_item(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    address = callback_data.get("address")
    add_or_remove_item_service(call.from_user.id, address)
    new_keyboard, text = create_manage_wishlist_keyboard(call.from_user.id)
    await call.message.edit_reply_markup(new_keyboard)


def register_manage_wishlist(dp: Dispatcher):
    dp.register_message_handler(show_wishlist, commands=["wishlist"], state="*")
    dp.register_callback_query_handler(add_or_remove_item, reciklomat_callback.filter(), state="*")
