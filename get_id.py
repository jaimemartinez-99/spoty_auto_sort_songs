import requests
import json
import webbrowser
from api_keys import client_id, client_secret, redirect_uri
from urllib.parse import urlencode, urlparse, parse_qs
from get_access_token import get_access_token

def get_id():
    url = "https://api.spotify.com/v1/me"
    headers = {
        "Authorization": f"Bearer {get_access_token(client_id, client_secret)}"
    }
    response = requests.get(url, headers=headers)

    # Handle the response
    if response.status_code == 200:
        user_data = response.json()
        print(json.dumps(user_data, indent=4))
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        print(response.text)

    print(response.text)
    return response