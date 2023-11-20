# python workflow on requesting token and api data
# author: Carl von Holly
from __future__ import print_function
import sys
import spotipy
import spotipy.util as util
import os

# url = "https://accounts.spotify.com/api/token"
redirect_uri = 'http://localhost:8888/callback'
client_id = '54cfccda4e9943e5a50fcbe7fe29b695'
file_path = os.getcwd() + os.sep + 'client_secret.txt'
with open(file_path, 'r') as file:
    line = file.readline().rstrip("\n")
    client_secret = line

scope = 'user-library-read playlist-modify-public playlist-modify-private'
# cp_scope = 'playlist-modify-public playlist-modify-private'
# cp_redirect_uri = 'http://localhost:8888/'


# def get_sp(username):
#     token = util.prompt_for_user_token(username, scope,
#                                     client_id=client_id,
#                                     client_secret=client_secret,
#                                     redirect_uri='http://localhost:3000')

#     if token:
#         sp = spotipy.Spotify(auth=token)
#     else:
#         print('Authenticaion failed, aborting')
#         return

#     return sp