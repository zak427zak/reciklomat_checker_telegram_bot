import requests

from tgbot.config import load_config


def switch_subscription_service(user_id, switch_type):
    config = load_config(".env")
    url = f"https://services.llqq.ru/reciklomat/user/switch/{switch_type}"
    headers = {
        'Authorization': f'Bearer {config.tg_bot.server_token}'
    }
    data = {"userId": user_id}
    r = requests.post(url, headers=headers, data=data)
    if r.status_code == 200:
        return r.json()['result']
    else:
        return r.json()['errorMessage']
