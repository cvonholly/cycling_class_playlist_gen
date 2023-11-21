# packages
import streamlit as st
import utils.get_token as gt # from ..notebooks.src import client_id, client_secret
from utils.playlist_input import *
from utils.get import *



class UI():
    """
    create UI based on user and view
    """
    def __init__(self, sp, user) -> None:
        self.sp = sp
        self.user = user
        self.tracks = []   # tracks to be selected for new playlist
        self.cols = st.columns([.85,.15])
        self.col1, self.col2 = self.cols[0], self.cols[1]
        self.dfp, self.dic = get_profile_playlists(self.sp)
        self.sidebar = st.sidebar

        self.playlist_links = []  # links of selected playlists

        # for new playlist:
        self.selected_rows = pd.DataFrame()
        self.playlist, self.tracks = None, pd.DataFrame()
        self.new_pl_name = 'New Test Playlist'
        self.pl_public, self.pl_description = True, ''

        if 'clicked' not in st.session_state:
            st.session_state.clicked = False

        if 'tracks' not in st.session_state:
            st.session_state['tracks'] = pd.DataFrame()

    # depreciated
    # def change_view(self):
    #     self.view_1 = not self.view_1

    def click_view_button(self):
        st.session_state.clicked = not st.session_state.clicked

    def build(self):
        #
        # 1st view
        #
        if not st.session_state.clicked:
            with self.col2:
                button_c = st.button('continue ->',
                                on_click=self.click_view_button
                            )
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
                    disabled=df.columns
                )
                

                self.selected_rows = edited_df[edited_df.Select]
                self.tracks = self.selected_rows.drop('Select', axis=1)  # selceted tracks
                if len(self.tracks) > 0:
                    st.session_state['tracks'] = self.tracks

        #
        # view 2
        #
        elif st.session_state.clicked:
            self.tracks = st.session_state['tracks']  # selceted tracks
            with self.col2:
                but = st.button('<- Back',
                                on_click=self.click_view_button)
                button_generate = st.button('Generate New Playlist',
                                            on_click=self.get_output_playlist)
            
            with self.col1:
                df_with_selections = self.tracks.copy()
                df_with_selections.insert(0, "Select", False)
                edited_df = st.data_editor(
                    df_with_selections,
                    hide_index=True,
                    column_config={"Select": st.column_config.CheckboxColumn(required=True),
                                'uri': None},
                    disabled=self.tracks.columns
                )

    def get_output_playlist(self):
        print('Creating output playlist...')
        self.playlist = self.sp.user_playlist_create(self.user, self.new_pl_name,
                                                     self.tracks,
                                           self.pl_public, self.pl_description)

        self.sp.user_playlist_add_tracks(
            self.user,
            self.playlist['id'],
            list(self.tracks['uri'])
        )