from utils.get_token import scope, client_id, client_secret, redirect_uri
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import ui
import os
import spotipy
import time
from ui import UI


# input
username = 'carlvonholly'

def main():
    try:
        token = util.prompt_for_user_token(username, scope,
                                   client_id=client_id,
                                   client_secret=client_secret,
                                   redirect_uri=redirect_uri,
                                   show_dialog=True
                                   )
        if token:
            sp = spotipy.Spotify(auth=token)
        else:
            print('Authenticaion failed, aborting')
        # sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id, client_secret))
    except:
        print('Authentication failed, aborting!')

    time.sleep(3)

    ui = UI(sp, username)

    ui.build()

    # state_1 = ui.build(sp, user=username)

    # if state_1: # switch screen
    #     print('We are in state_1: ', state_1)
    #     pass


if __name__=='__main__':
    main()