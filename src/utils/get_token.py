# python workflow on requesting token and api data
# author: Carl von Holly
from __future__ import print_function
import sys
import spotipy
import spotipy.util as util
import os

# url = "https://accounts.spotify.com/api/token"
redirect_uri = 'http://localhost:8888/callback'

if "SPOTIPY_CLIENT_ID" in os.environ and "SPOTIPY_CLIENT_SECRET" in os.environ:
    client_id = os.environ["SPOTIPY_CLIENT_ID"]
    client_secret = os.environ["SPOTIPY_CLIENT_SECRET"]
else:
    raise Exception("Supply your credentials as environment variables!")

scope = 'user-library-read playlist-modify-public playlist-modify-private'