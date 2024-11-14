from get_access_token import get_access_token
from api_keys import client_id, client_secret, redirect_uri
import requests 
import pandas as pd

def get_playlists(headers):

    url = f"https://api.spotify.com/v1/me/playlists"
    params = {
        "limit": 10,
    }
    all_playlists = []

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        user_data = response.json()
        all_playlists.extend(user_data['items'])
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        print(response.text)

    # Create a DataFrame with the two playlists
    df_two_playlists = pd.DataFrame(all_playlists[0:2])
    print(df_two_playlists["name"])
    return df_two_playlists