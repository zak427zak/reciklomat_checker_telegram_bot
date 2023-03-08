import requests

from tgbot.config import load_config


def set_language_service(message, language):
    config = load_config(".env")
    url = f"https://services.llqq.ru/reciklomat/user/language"
    headers = {'Authorization': f'Bearer {config.tg_bot.server_token}', 'Accept-Language': language}
    data = {"userId": message.from_user.id, "language": language}
    r = requests.post(url, headers=headers, data=data)
    print(r.text)
    if r.status_code == 200:
        return r.json()['result']
    else:
        return r.json()['errorMessage']
