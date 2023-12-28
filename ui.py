# packages
import streamlit as st
import numpy as np
# utils
from utils.playlist_input import *
from utils.get import *
from utils.drag_and_drop import *




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
        self.zones = [
                                "📝 Z1",
                                "🔛 Z2",
                                "🔋 Z3",
                                "📒 Z4",
                                "📕 Z5",
                        ]

        self.colors = None

        if 'clicked' not in st.session_state:
            st.session_state.clicked = False

        if 'tracks' not in st.session_state:
            st.session_state['tracks'] = pd.DataFrame()

        if 'final_tracks' not in st.session_state:
            st.session_state['final_tracks'] = pd.DataFrame()


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


                # test drag and drop
                # df_drag_and_drop = build_dad(df_with_selections)
                # st.write(df_drag_and_drop)

        #
        # view 2
        #
        elif st.session_state.clicked:
            self.tracks = st.session_state['tracks']  # selceted tracks
            with self.col2:
                but = st.button('<- Back',
                                on_click=self.click_view_button)
                self.new_pl_name = st.text_input('Playlist Name: ', value=self.new_pl_name)
                button_generate = st.button('Generate New Playlist',
                                            on_click=self.get_output_playlist)
            
            with self.col1:
                #
                # ToDo: implement drag and drop as in https://discuss.streamlit.io/t/drag-and-drop-rows-in-a-dataframe/33077/3
                # 
                df_with_selections = self.tracks.copy()
                df_with_selections.insert(0, "zone", np.repeat(self.zones[0], len(df_with_selections.index)))
                df_with_selections.drop('uri', axis=1, inplace=True)  # dont show uri
                self.edit_tracks = build_dad(df_with_selections, self.zones)

                # self.edit_tracks = st.data_editor(
                #     build_dad(df_with_selections),  # df_with_selections,
                #     hide_index=True,
                #     column_config={
                #         "zone": st.column_config.SelectboxColumn(
                #             "Zone",
                #             help="Zone to ride at",
                #             width="small",
                #             options=self.zones,
                #             required=True,
                #         )
                #     },
                #     disabled=self.tracks.columns
                # )
                if len(self.tracks) > 0:
                    st.session_state['final_tracks'] = self.tracks

            with self.sidebar:
                df = pd.DataFrame()
                df['zone'] = self.zones
                df['total time'] = 0
                df.set_index('zone', inplace=True)
                for z in self.zones:
                    df.loc[z, 'total time'] = self.time_sum(list(self.edit_tracks[self.edit_tracks['zone'] == z]['length']))
                st.dataframe(df)

    def time_sum(self, l):
        """
        sum up time of tracks in list and retunr as str
        """
        seconds = 0
        for i in l:
            seconds += 60 * int(i.split(':')[0])
            seconds += int(i.split(':')[1])
        return convert_seconds(seconds)

    def get_output_playlist(self):
        """
        create output playlist from selected tracks
        """
        print('Creating output playlist...')
        self.playlist = self.sp.user_playlist_create(self.user, self.new_pl_name,
                                           self.pl_public, self.pl_description)

        try:
            self.sp.user_playlist_add_tracks(
                self.user,
                self.playlist['id'],
                list(st.session_state['final_tracks']['uri'])
            )
        except:
            print('Error adding tracks to playlist')