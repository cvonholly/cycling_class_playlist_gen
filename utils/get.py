import pandas as pd
import spotipy as sp


def convert_seconds(seconds):
    """
    converts seconds to str(minutes:seconds)
    """
    try:
        seconds = int(seconds)
    except:
        return 'invalid conversion'
    minutes = seconds // 60  # Get the whole number of minutes
    remaining_seconds = seconds % 60  # Get the remaining seconds
    return f"{minutes:02d}:{remaining_seconds:02d}"

def convert_to_seconds(time):
    """
    converts str(minutes:seconds) to seconds
    """
    minutes, seconds = time.split(':')
    return int(minutes)*60 + int(seconds)



def get_profile_playlists(sp) -> (pd.DataFrame(), dict):
    """
    returns current user playlists
    """
    dic = sp.current_user_playlists(limit=20)
    playlist_names = [x['name'] for x in dic['items']]
    return (pd.DataFrame(playlist_names), dic)

def get_data(sp,
             pl_url: [],   # list of urls
             headers=['tempo', 'duration_ms'],   # headers to get
             headers_af=['name', 'uri'],
             header_names={'tempo': 'BPM', 'duration_ms': 'length'},
             headers_af_names={'name': 'Name', 'uri': 'uri'},
             dtypes={'BPM': int, 'Name': str},
             multiplies={'duration_ms': 1e-3},
             get_artist=True
             ):
    """
    gets playlist data
    docu on tracks audio features: https://developer.spotify.com/documentation/web-api/reference/get-several-audio-features
    """
    df_tot = pd.DataFrame()
    for p in pl_url:
        df = pd.DataFrame()
        playlist_tracks = sp.playlist_tracks(p)

        if len(playlist_tracks['items'])==0:  # if playlist empty
            continue

        for h in headers_af:
            x = [track['track'][h] for track in playlist_tracks['items']]
            df[headers_af_names[h]] = x  # [song['track'][h] for song in playlist_tracks]
        
        if get_artist:
            df['Artist'] = [', '.join(i['name'] for i in track['track']['artists']) for track in playlist_tracks['items']]
        
        song_ids = [track['track']['id'] for track in playlist_tracks['items']]

        audio_features = sp.audio_features(song_ids)
        
        for h in headers:
            df[header_names[h]] = [song[h] for song in audio_features]  # get header info of songs
            if h in multiplies:
                df[header_names[h]] = df[header_names[h]] * multiplies[h]
            if h=='duration_ms':  # exception format for datetime
                df[header_names[h]] = [convert_seconds(x) for x in df[header_names[h]]]

        if dtypes is not None:
            df = df.astype(dtypes)
        df_tot = pd.concat([df_tot, df])
    return df_tot