# packages
import streamlit as st
import utils.get_token as gt # from ..notebooks.src import client_id, client_secret
from utils.playlist_input import *
from utils.get import *


def build(sp):
    df = get_data(sp,
                'https://open.spotify.com/playlist/37i9dQZF1DX6J5NfMJS675?si=aca32942f2b44c15')

    st.dataframe(df)

    dfp = get_profile_playlists(sp)

    with st.sidebar:
        playlist_interact(dfp)
