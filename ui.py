# packages
import streamlit as st
import utils.get_token as gt # from ..notebooks.src import client_id, client_secret
from utils.playlist_input import *
from utils.get import *
from utils.playlist_output import get_output_playlist
# import spotipy.util as util
# import spotipy

# from utils.get_token import cp_scope, client_id, client_secret, cp_redirect_uri, cp_scope


def build(sp, user):
    col1, col2 = st.columns([.85,.15])

    dfp, dic = get_profile_playlists(sp)

    with st.sidebar:
        try:
            pl = list(playlist_interact(dfp)['0'])  # returns names of selected
        except:
            pl = []

    playlist_links = [x['external_urls']['spotify'] for x in dic['items'] if x['name'] in pl]

    df = get_data(sp, playlist_links)

    df_with_selections = df.copy()
    df_with_selections.insert(0, "Select", False)

    # Get dataframe row-selections from user with st.data_editor
    with col1:
        edited_df = st.data_editor(
            df_with_selections,
            hide_index=True,
            column_config={"Select": st.column_config.CheckboxColumn(required=True),
                           'uri': None},
            disabled=df.columns,
            # column_config=column_config
        )

    selected_rows = edited_df[edited_df.Select]
    out = selected_rows.drop('Select', axis=1)

    # add generate playlist button
    with col2:
        button = st.button('Generate Playlist')
        if button:
            get_output_playlist(sp,
                                user, 
                                tracks=out)

    return out

    # st.dataframe(edited_df)