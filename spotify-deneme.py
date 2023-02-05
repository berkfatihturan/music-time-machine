
from spotipy.oauth2 import SpotifyClientCredentials


def spotify_dev():
    # Authentication - without user
    client_credentials_manager = SpotifyClientCredentials(client_id="e065370182224cabb8dbcd6fda7f0abf", client_secret="4f03df70a91844e58881552b4bdeceb3")
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    playlist_link = "https://open.spotify.com/playlist/0G8wM0EfPNbFYl1Y4hur7y"
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]
    print(playlist_URI)
    track_uris = [x["track"]["uri"] for x in sp.playlist_items(playlist_URI)["items"]]
    print(track_uris)
