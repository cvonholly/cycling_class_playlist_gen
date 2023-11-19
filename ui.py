# packages
import streamlit as st
import utils.get_token as gt # from ..notebooks.src import client_id, client_secret
from utils.playlist_input import *
from utils.get import *


def build(sp):
    dfp, dic = get_profile_playlists(sp)

    with st.sidebar:
        pl = playlist_interact(dfp)  # returns names of selected

    playlist_links = [x['external_urls']['spotify'] for x in dic['items'] if x['name'] in list(pl['0'])]

    df = get_data(sp, playlist_links)

    st.dataframe(df)
