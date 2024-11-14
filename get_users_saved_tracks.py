import requests
import json
import webbrowser
from api_keys import client_id, client_secret, redirect_uri
from urllib.parse import urlencode, urlparse, parse_qs
from get_access_token import get_access_token
import pandas as pd

def get_users_saved_tracks(headers):
    url = "https://api.spotify.com/v1/me/tracks"
    limit = 20
    offset = 0
    all_tracks = []

    while True:
        # Update the URL with limit and offset for pagination
        params = {
            "limit": limit,
            "offset": offset
        }
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            user_data = response.json()
            all_tracks.extend(user_data["items"])  

            if len(user_data["items"]) < limit:
                break
        else:
            print(f"Failed to retrieve data: {response.status_code}")
            print(response.text)
            break
        
        offset += limit

    print(f"Total tracks retrieved: {len(all_tracks)}")
    return all_tracks

def process_tracks(headers):
    response = get_users_saved_tracks(headers)
    tracks_data = []
    for item in response:
        track = item["track"]
        track_info = {
            "name": track["name"],
            "uri": track["uri"],
            "id": track["id"],
            "external_url": track["external_urls"]["spotify"],
            "artist_id": track["artists"][0]["id"],  
            "artist_name": track["artists"][0]["name"],
        }
        tracks_data.append(track_info)
    # Create a DataFrame
    df = pd.DataFrame(tracks_data)
    return df