# packages
import streamlit as st
import utils.get_token as gt # from ..notebooks.src import client_id, client_secret
from utils.playlist_input import *
from utils.get import *
from utils.playlist_output import get_output_playlist



class UI():
    """
    create UI based on user and view
    """
    def __init__(self, sp, user, view_1) -> None:
        self.sp = sp
        self.user = user
        self.view_1 = view_1
        self.tracks = []   # tracks to be selected for new playlist
        self.cols = st.columns([.85,.15])
        self.col1, self.col2 = self.cols[0], self.cols[1]
        self.dfp, self.dic = get_profile_playlists(self.sp)
        self.sidebar = st.sidebar

        self.playlist_links = []  # links of selected playlists

    def change_view(self):
        self.view_1 = not self.view_1

    def build(self):
        with self.col2:
            button_c = st.button('continue ->', 
                            # on_click=self.change_view()
                            )
        #
        # 1st view
        #
        if not button_c:
        # if self.view_1:
            with self.sidebar:
                try:
                    pl = list(playlist_interact(self.dfp)['0'])  # returns names of selected
                except:
                    pl = []

            self.playlist_links = [x['external_urls']['spotify'] for x in self.dic['items'] if x['name'] in pl]

            df = get_data(self.sp, self.playlist_links)

            df_with_selections = df.copy()
            df_with_selections.insert(0, "Select", False)

            # Get dataframe row-selections from user with st.data_editor
            with self.col1:
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

            # add continue button
            
        #
        # view 2
        #
        else:
            with self.col2:
                but = st.button('<- Back', on_click=self.change_view())
            button_generate = st.button('Generate Playlist')
            if button_generate:
                playlist, tracks = get_output_playlist(sp,
                                self.user,
                                tracks=out)

# def change_view(view_1=True):
#     return view_1

# def build(sp, user):

#     tracks = []
#     view_1 = True
#     playlist = None
#     col1, col2 = st.columns([.85,.15])

#     dfp, dic = get_profile_playlists(sp)

#     with st.sidebar:
#         if view_1:
#             try:
#                 pl = list(playlist_interact(dfp)['0'])  # returns names of selected
#             except:
#                 pl = []

#     playlist_links = [x['external_urls']['spotify'] for x in dic['items'] if x['name'] in pl]

#     df = get_data(sp, playlist_links)

#     df_with_selections = df.copy()
#     df_with_selections.insert(0, "Select", False)

#     # Get dataframe row-selections from user with st.data_editor
#     with col1:
#         if view_1:     # 1st view
#             edited_df = st.data_editor(
#                 df_with_selections,
#                 hide_index=True,
#                 column_config={"Select": st.column_config.CheckboxColumn(required=True),
#                             'uri': None},
#                 disabled=df.columns,
#                 # column_config=column_config
#             )
#         else:  # 2ed view
#             pass

#     selected_rows = edited_df[edited_df.Select]
#     out = selected_rows.drop('Select', axis=1)

#     # add generate playlist button
#     with col2:
#         if view_1:  # 1st view
#             button_c = st.button('continue ->', 
#                                on_click=change_view(False))
#             # if st.button('continue ->'):
#             #     tracks = out
#             #     view_1 = False
#                 # playlist, tracks = get_output_playlist(sp,
#                 #                 user,
#                 #                 tracks=out)
#         else:   # 2ed view
#             if st.button('<- Back'):
#                 view_1 = True
#             button_generate = st.button('Generate Playlist')
#             if button_generate:
#                 playlist, tracks = get_output_playlist(sp,
#                                 user,
#                                 tracks=out)
    
#     return view_1