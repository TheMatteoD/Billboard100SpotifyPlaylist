from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Scraping Billboard 100
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
web_page = response.text

soup = BeautifulSoup(web_page, "html.parser")

song_list = soup.find_all(name="h3", id="title-of-a-story")

title_parser = [song.string for song in song_list]
converted_list = []
redundant_items = ["Songwriter(s):", "Producer(s):", "Imprint/Promotion Label:", "Gains in Weekly Performance",
                   "Additional Awards", "Songwriter(s): ", " Imprint/Promotion Label:", " Songwriter(s):"]

for title in title_parser:
    if not title is None:
        parsed_title = title.text.strip('\n')
    if parsed_title not in redundant_items:
        converted_list.append(parsed_title)
    else:
        pass

converted_list = converted_list[0:100]
song_names = converted_list
print(song_names)

#Spotify Authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id="", #INPUT YOUR CLIENT ID HERE
        client_secret="", #INPUT YOUR CLIENT SECRET HERE
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
print(user_id)

#Searching Spotify for songs by title
song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} Couldn't find on Spotify. Skipped.")

#Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

#Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
