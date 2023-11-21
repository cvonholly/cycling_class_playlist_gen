def get_output_playlist(sp,
                        user,
                        tracks,
                        name='New Playlist',
                        public=True,
                        description=None):
    

    print('Creating output playlist...')
    playlist = sp.user_playlist_create(user,
                                            name, public, description)
    
    sp.user_playlist_add_tracks(
        user,
        playlist['id'],
        list(tracks['uri'])
    )
    
    return playlist, tracks