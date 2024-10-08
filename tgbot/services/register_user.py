import requests


def register_user_service(message, language):
    url = f"http://reciklomat_api:8000/user/register"
    headers = {'Accept-Language': language}
    data = {"userId": message.from_user.id, "firstName": str(message.from_user.first_name),
            "lastName": str(message.from_user.last_name), "username": str(message.from_user.username),
            "language": language}
    r = requests.post(url, headers=headers, data=data)
    if r.status_code == 200:
        return r.json()['result']
    else:
        return r.json()['errorMessage']
