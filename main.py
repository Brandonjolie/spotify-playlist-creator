import requests
from bs4 import BeautifulSoup
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

spotify_key = os.environ.get("spotify_key")
spotify_id = os.environ.get("spotify_id")
spotify_user = os.environ.get("spotify_user")
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=spotify_id,
        client_secret=spotify_key,
        show_dialog=True,
        cache_path="token.txt",
    )
)
input_date = input(
    "Which year do you want to travel to? Type the date in this format YYYY-MM-DD: "
)
# input_date = "2000-08-12" testing date
year = input_date.split("-")[0]
billboard_link = f"https://www.billboard.com/charts/hot-100/{input_date}/"
data = requests.get(billboard_link).text
soup = BeautifulSoup(data, "html.parser")
results = soup.find_all(name="li", class_="lrv-u-width-100p")
song_names = []
for i in range(0, len(results), 2):
    song_names.append(results[i].h3.text.strip())
songs_to_add = []
id = sp.current_user()["id"]
for song in song_names:
    data = sp.search(song)["tracks"]["items"][0]
    if song == data["name"]:
        songs_to_add.append(data["id"])

outp = sp.user_playlist_create(
    id,
    name=f"{input_date} Billboard 100",
    public=False,
    description="Automated",
)
sp.user_playlist_add_tracks(id, outp["id"], songs_to_add)
