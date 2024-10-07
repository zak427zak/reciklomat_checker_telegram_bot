import requests


def set_language_service(message, language):
    url = f"http://reciklomat_api:8000/user/language"
    headers = {'Content-Type': 'application/json', 'Accept-Language': language}
    data = {"userId": message.from_user.id, "language": language}
    r = requests.post(url, headers=headers, data=data)
    print(r.text)
    if r.status_code == 200:
        return r.json()['result']
    else:
        return r.json()['errorMessage']
