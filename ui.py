import streamlit as st
import pandas as pd
import numpy as np
from utils.get import get_data

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import utils.get_token as gt # from ..notebooks.src import client_id, client_secret


# st.set_title('Cycling Class Playlist Generator')

birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(gt.client_id, gt.client_secret))

df = get_data(sp,
              'https://open.spotify.com/playlist/37i9dQZF1DX6J5NfMJS675?si=aca32942f2b44c15')

st.dataframe(df)