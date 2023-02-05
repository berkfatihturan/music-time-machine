from bs4 import BeautifulSoup
import requests
import re

import spotipy
from spotipy.oauth2 import SpotifyOAuth

URL = "https://www.billboard.com/charts/hot-100"
date = "2012-07-22"


def scraping_data():
    response = requests.get(f"{URL}/{date}/")
    soup = BeautifulSoup(response.text, 'html.parser')

    # find the music name in website
    sours_list = soup.find_all(class_="o-chart-results-list__item")
    music_data = [music_location.find("h3").text for music_location in sours_list if
                  music_location.find("h3") is not None]

    # remove space and tab
    music_data = [re.sub(r"[\n\t]*", "", m) for m in music_data]

    return music_data


def spotify_api():
    global date
    date = input("Date: ")
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope="playlist-modify-private",
            redirect_uri="http://example.com",
            client_id="YOUR CLİENT ID",
            client_secret="YOUR CLİENT SECRET",
            show_dialog=True,
            cache_path="token.txt"
        )
    )
    user_id = sp.current_user()["id"]

    # getting music name
    song_names = scraping_data()

    # find music in spotify and add song_uris
    song_uris = []
    year = date.split("-")[0]
    for song in song_names:
        result = sp.search(q=f"track:{song} year:{year}", type="track")  # search music
        print(result)
        try:
            uri = result["tracks"]["items"][0]["uri"]  # get music uri
            song_uris.append(uri)
        except IndexError:
            print(f"{song} doesn't exist in Spotify. Skipped.")

    playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)  # create playlist
    sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)  # add all song in song_uris from created playlist

    print("Playlist CREATED")


spotify_api()
