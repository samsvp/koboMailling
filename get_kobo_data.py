import requests
import json

def get_kobo_data():
    with open('tokens.json') as f:
        data = json.load(f)

    auth_token = data["auth_token"]
    form_uid = data["form_uid"]

    headers = {'Authorization': f'Token {auth_token}', 'Content-Type': 'application/json'}

    r = requests.get(f'https://kf.kobotoolbox.org/api/v2/assets/{form_uid}/data/?format=json', headers=headers, timeout=10)
    registries = r.json()

    return registries["results"]