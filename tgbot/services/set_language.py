import logging

import requests


def set_language_service(message, language):
    url = f"http://reciklomat_api:8000/user/language"
    headers = {'Content-Type': 'application/json', 'Accept-Language': language}
    data = {"telegram_id": message.from_user.id, "language": language}

    try:
        r = requests.post(url, headers=headers, json=data)
        # logging.info(f"Response from registration API: {r.status_code} - {r.text}")
        return r.json()['result']
    except Exception as e:
        logging.error(f"Failed to register user: {e}")
        return r.json()['errorMessage']
