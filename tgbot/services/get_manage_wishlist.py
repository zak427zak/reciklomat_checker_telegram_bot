import requests


def get_manage_wishlist(user_id):
    url = f"http://reciklomat_api:8000/user/wishlist"
    headers = {'Content-Type': 'application/json'}
    data = {"userId": user_id}
    r = requests.post(url, headers=headers, data=data)
    if r.status_code == 200:
        return r.json()['result']
    else:
        return r.json()['errorMessage']
