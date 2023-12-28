# Ultimate AI Cycling Class Playlist Generator
A helpful tool to automatically create playlist's with the tracks fulfilling a number of characteristics such as BPM, length, energy and more.

Manual [BPM Tap Tool](https://www.all8.com/tools/bpm.htm)

## Installation
### Pre:
- Python 3.x
- .venv (for setup)
  - [streamlit](https://docs.streamlit.io/library/get-started/installation)
  - [spotipy](https://spotipy.readthedocs.io/en/2.22.1/)

## Setup

1. Install the required packages in a virtual environment
2. Add your client secret in `client_secret.txt` to be able to connect to the service
3. Set your SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET environment variables to the specific values to use the [Spotipy library](https://spotipy.readthedocs.io/en/2.22.1/).
4. execute `streamlit run main.py`
5. In the web browser pop-up, allow the application access to your spotify account
6. Enjoy! Select your favourite playlists, sort for the reuired songs and create a new workout with these.


## To Dev
- ~~Drag and drop functionality in table~~ --done
    - adapt total time table headers/integration
- save selected playlists and songs (e.g. via `st.session_state`)
    - issues: certain objects are not saved while others are
- ~~add Text input for new playlist name~~  --done
- export to google sheets or excel (should be easy with dataframe)
