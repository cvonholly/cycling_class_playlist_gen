import spotipy as sp
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials


def get_data(sp,
             pl_url: str,
             headers=['tempo', 'duration_ms'],
            #  headers_af=['duration_ms'],
             header_names={'tempo': 'BPM', 'duration_ms': 'length'},
            #  headers_af_names={'duration_ms': 'length'}
             ):
    """
    returns dataframe with headers
    docu on tracks audio features: https://developer.spotify.com/documentation/web-api/reference/get-several-audio-features
    """
    df = pd.DataFrame()
    playlist_tracks = sp.playlist_tracks(pl_url)

    song_ids = [track['track']['id'] for track in playlist_tracks['items']]

    audio_features = sp.audio_features(song_ids)

    for h in headers:
        df[header_names[h]] = [song[h] for song in audio_features]  # get header info of songs

    return df