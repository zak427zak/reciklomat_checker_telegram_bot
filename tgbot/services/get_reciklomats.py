import requests

from tgbot.config import load_config


def get_reciklomats(user_id):
    config = load_config(".env")
    url = f"https://services.llqq.ru/reciklomat/user/wishlist"
    headers = {'Authorization': f'Bearer {config.tg_bot.server_token}'}
    data = {"userId": user_id}
    r = requests.post(url, headers=headers, data=data)
    return r.json()['items'], r.json()['text']

