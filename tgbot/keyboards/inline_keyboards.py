from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.callbacks import reciklomat_callback, language_callback
from tgbot.services.get_manage_wishlist import get_manage_wishlist


def create_manage_wishlist_keyboard(user_id):
    manage_wishlist_keyboard = InlineKeyboardMarkup(row_width=2)
    data = get_manage_wishlist(user_id)

    for item in data['items']:
        reciklomat_button = InlineKeyboardButton(text=f"{item['checked_data']} {item['address']}",
                                                 callback_data=reciklomat_callback.new(id=item['id'],
                                                                                       address=item['address'],
                                                                                       is_checked=item['is_checked']))
        manage_wishlist_keyboard.insert(reciklomat_button)

    return manage_wishlist_keyboard, data['text']


def create_languages_keyboard(create_or_update):
    languages_keyboard = InlineKeyboardMarkup()
    langs = {
        "ru": "🇷🇺 Русский",
        "en": "🇬🇧 English",
        "sr": "🇷🇸 Српски"
    }
    for key, value in langs.items():
        language_button = InlineKeyboardButton(text=f"{value}",
                                               callback_data=language_callback.new(id=key, create_or_update=create_or_update))
        languages_keyboard.insert(language_button)

    return languages_keyboard
