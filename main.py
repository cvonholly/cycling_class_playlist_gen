from utils.get_token import scope, client_id, client_secret, redirect_uri
import spotipy.util as util
import ui
import os
import spotipy


# scope = 'user-library-read'
# url = "https://accounts.spotify.com/api/token"
# client_id = '54cfccda4e9943e5a50fcbe7fe29b695'
# file_path = os.getcwd() + os.sep + 'client_secret.txt'
# with open(file_path, 'r') as file:
#     line = file.readline().rstrip("\n")
#     client_secret = line

# input
username = 'carlvonholly'

def main():
    try:
        token = util.prompt_for_user_token(username, scope,
                                   client_id=client_id,
                                   client_secret=client_secret,
                                   redirect_uri=redirect_uri)
        if token:
            sp = spotipy.Spotify(auth=token)
        else:
            print('Authenticaion failed, aborting')
    except:
        print('Authentication failed, aborting!')

    ui.build(sp)


if __name__=='__main__':
    main()