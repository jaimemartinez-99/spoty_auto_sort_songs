from get_access_token import get_access_token
from api_keys import client_id, client_secret, redirect_uri
from get_users_saved_tracks import process_tracks
import requests
from loguru import logger
import pandas as pd

rap_array = ['hip hop','chicago rap', 'rap', 'philly rap', 'slap house', 'pop rap', 'conscious hip hop', 'east coast hip hop', 'west coast hip hop',
             'boom bap espanol', 'rap underground espanol', 'spanish hip hop', 'gangster rap', 'canadian hip hop','urbano espanol', 'colombian hip hop', 
             'hardcore hip hop', 'queens hip hop']

def extract_artist(headers):
    df = process_tracks(headers)


    df_rap_songs = pd.DataFrame()
    df_general_songs = pd.DataFrame()

    for _, row in df.iterrows():  
        artist_id = row["artist_id"]  
        genres = get_artist_genre(artist_id, headers)
        if any(genre in rap_array for genre in genres):
            logger.success(f"Artist {row["artist_name"]} belongs to the rap playlist")
            df_rap_songs = pd.concat([df_rap_songs, row.to_frame().T], ignore_index=True)
        else:
            logger.error(f"Artist {row["artist_name"]} does NOT belong to the rap playlist")
            df_general_songs = pd.concat([df_general_songs, row.to_frame().T], ignore_index=True)

    logger.info("Rap Playlist:")
    print(df_rap_songs.head(10))

    logger.info("General Playlist:")
    print(df_general_songs.head(10))

    logger.info(f"Total rap songs: {df_rap_songs.shape[0]}")

    return df_rap_songs, df_general_songs


def get_artist_genre(artist_id,  headers):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    response = requests.get(url, headers=headers)
    # Handle the response
    if response.status_code == 200:
        artist = response.json()
        genres = artist["genres"]
        print(genres)
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        print(response.text)
    return genres