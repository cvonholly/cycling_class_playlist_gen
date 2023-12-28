import streamlit as st
import pandas as pd


def playlist_interact(df_with_selections, df):
    """
    returns selected playlists, edited df
    """
    # Get dataframe row-selections from user with st.data_editor
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={"Select": st.column_config.CheckboxColumn(required=True),
                       '0': 'Playlist'
                       },
        disabled=df.columns
    )

    # Filter the dataframe using the temporary column, then drop the column
    # selected_rows = edited_df[edited_df.Select].drop('Select', axis=1)
    return edited_df


def tracks_input(df_with_selections):
    edited_df = st.data_editor(
                    df_with_selections,
                    hide_index=True,
                    column_config={"Select": st.column_config.CheckboxColumn(required=True),
                                'uri': None},
                    disabled=df_with_selections.columns[1:]
                )

    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = edited_df[edited_df.Select]
    return selected_rows.drop('Select', axis=1), edited_df