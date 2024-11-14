from get_playlists import get_playlists
from api_keys import client_id, client_secret, redirect_uri
from get_artist_genre import extract_artist
from get_access_token import get_access_token
import requests
from loguru import logger
import pandas as pd

headers = {
        "Authorization": f"Bearer {get_access_token(client_id, client_secret, redirect_uri)}"
}
df_two_playlists = get_playlists(headers)

df_rap_playlist = df_two_playlists.loc[1]
df_general_playlist = df_two_playlists.loc[0]


def add_rap_songs_to_playlist(headers, rap_songs, rap_playlist):
    if rap_songs.empty:
        logger.error("No rap songs found!")
        return
    
    rap_playlist_id = rap_playlist["id"]
    rap_playlist_url = f"https://api.spotify.com/v1/playlists/{rap_playlist_id}/tracks"
    rap_uris = rap_songs["uri"].tolist()[::-1]

    data = {
        "uris": rap_uris
    }

    response = requests.post(rap_playlist_url, headers={**headers, "Content-Type": "application/json"}, json=data)
    if response.status_code == 201:
        logger.success("Rap songs added successfully to the end of the playlist!")
    else:
        logger.error(f"Failed to add songs: {response.status_code}")
        logger.error(response.text)


def add_general_songs_to_playlist(headers, general_songs, general_playlist):
    print(general_songs)
    print(general_playlist)
    if general_songs.empty:
        logger.error("No general songs found!")
        return
    
    general_playlist_id = general_playlist["id"]
    general_playlist_url = f"https://api.spotify.com/v1/playlists/{general_playlist_id}/tracks"
    general_uris = general_songs["uri"].tolist()[::-1]

    data = {
        "uris": general_uris
    }

    response = requests.post(general_playlist_url, headers={**headers, "Content-Type": "application/json"}, json=data)
    if response.status_code == 201:
        logger.success("General songs added successfully to the end of the playlist!")
    else:
        logger.error(f"Failed to add songs: {response.status_code}")
        logger.error(response.text)

def delete_tracks_from_saved(headers, rap_songs, general_songs):
    url = "https://api.spotify.com/v1/me/tracks"

    if rap_songs.empty and general_songs.empty:
        logger.error("No songs found to delete!")
        return
    df_rap = pd.DataFrame()
    df_general = pd.DataFrame()

    if not rap_songs.empty:
        df_rap = rap_songs[["id"]] 
    if not general_songs.empty:    
        df_general = general_songs[["id"]]

    if not df_rap.empty or not df_general.empty:
        df = pd.concat([df_rap, df_general])
        track_ids = df["id"].tolist()
    else:
        logger.error("No track IDs found to delete!")
        return
    
    track_ids = df["id"].tolist()

    chunks = [track_ids[i:i + 50] for i in range(0, len(track_ids), 50)]
    
    for chunk in chunks:
        data = {"ids": chunk}
        response = requests.delete(url, headers={**headers, "Content-Type": "application/json"}, json=data)
        
        if response.status_code == 200:
            print("Saved tracks have been removed for this batch")
        else:
            print(f"Failed to remove songs: {response.status_code}")
            print(response.text)

def sort_playlists(headers):
    rap_songs, general_songs = extract_artist(headers)
    logger.info("Adding songs to their playlists!")

    add_rap_songs_to_playlist(headers, rap_songs, rap_playlist=df_rap_playlist)
    add_general_songs_to_playlist(headers, general_songs, general_playlist=df_general_playlist)

    logger.info("All songs have been added to the playlists!")
    
    logger.info("Proceeding to delete the saved tracks...")
    delete_tracks_from_saved(headers, rap_songs, general_songs)

    logger.info("All saved tracks have been removed!")

    exit()

if __name__ == "__main__":
    sort_playlists(headers)