from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.callback_datas import reciklomat_callback, languages_callback
from tgbot.services.get_reciklomats import get_reciklomats


def create_new_keyboard(user_id):
    all_reciklomats_keyboard = InlineKeyboardMarkup(row_width=2)
    data, text = get_reciklomats(user_id)
    for item in data:
        reciklomat_button = InlineKeyboardButton(text=f"{item['checked_data']} {item['address']}",
                                                 callback_data=reciklomat_callback.new(id=item['id'],
                                                                                       address=item['address'],
                                                                                       is_checked=item['is_checked']))
        all_reciklomats_keyboard.insert(reciklomat_button)

    return all_reciklomats_keyboard, text


def create_languages_keyboard():
    languages_keyboard = InlineKeyboardMarkup()
    langs = {
        "ru": "🇷🇺 Русский",
        "en": "🇬🇧 English",
        "sr": "🇷🇸 Српски"
    }
    for key, value in langs.items():
        language_button = InlineKeyboardButton(text=f"{value}",
                                               callback_data=languages_callback.new(id=key))
        languages_keyboard.insert(language_button)

    return languages_keyboard
