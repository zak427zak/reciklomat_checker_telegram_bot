import requests
from aiogram.types import Message

from tgbot.config import load_config


def get_subscription_status(message: Message):
    config = load_config(".env")
    url = f"https://services.llqq.ru/reciklomat/user/status"
    headers = {'Authorization': f'Bearer {config.tg_bot.server_token}' }
    data = {"userId": message.from_user.id}
    r = requests.post(url, headers=headers, data=data)
    if r.status_code == 200:
        return r.json()['result']
    else:
        return r.json()['errorMessage']
