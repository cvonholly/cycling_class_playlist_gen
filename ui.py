# packages
import streamlit as st
import utils.get_token as gt # from ..notebooks.src import client_id, client_secret
from utils.playlist_input import *
from utils.get import *


def build(sp):
    col1, col2 = st.columns([.85,.15])

    dfp, dic = get_profile_playlists(sp)

    with st.sidebar:
        pl = playlist_interact(dfp)  # returns names of selected

    playlist_links = [x['external_urls']['spotify'] for x in dic['items'] if x['name'] in list(pl['0'])]

    df = get_data(sp, playlist_links)

    df_with_selections = df.copy()
    df_with_selections.insert(0, "Select", False)

    # Get dataframe row-selections from user with st.data_editor
    with col1:
        edited_df = st.data_editor(
            df_with_selections,
            hide_index=True,
            column_config={"Select": st.column_config.CheckboxColumn(required=True)},
            disabled=df.columns,
            # column_config=column_config
        )

    # add generate playlist button
    with col2:
        st.button('Generate Playlist', )

    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = edited_df[edited_df.Select]
    return selected_rows.drop('Select', axis=1)

    # st.dataframe(edited_df)