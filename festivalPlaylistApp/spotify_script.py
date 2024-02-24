import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import spotipy.util as util
import webbrowser
import sys
import json
from datetime import datetime, timedelta

unselected_artists = []

def get_user_token():
    scope = "playlist-modify-public"
    cache_filename = f".cache-{username}"

    try:
        token = util.prompt_for_user_token(username, scope)
        user_token = spotipy.Spotify(auth=token)
        return user_token
    except FileNotFoundError:
        print(f"Cache file not found: {cache_filename}")
    except Exception as e:
        print(f"Error obtaining user token: {e}")
    
    try:
        os.remove(cache_filename)
        print(f"Cache file removed: {cache_filename}")
    except FileNotFoundError:
        print(f"Cache file not found: {cache_filename}")
    except Exception as e:
        print(f"Error removing cache file: {e}")
        
    return None


def get_user_info(user_token):
    user = user_token.current_user()

    user_id = user['id']

    return user_id


def get_artist_id(user_token, artist, unselected_artists):
    query = artist.lower()
    results = user_token.search(query, 1, 0, "artist")

    artist_id = results['artists']['items'][0]['id']
    artist_name = results['artists']['items'][0]['name']
    print(f"Artist Name: {artist_name}")
    
    artist_name = artist_name.replace("’", "'")
    query = query.replace("’", "'")

    if (artist_name.lower() != query.lower()):
        print(f"Artist Name: {artist_name} does not match query: {query}")
        unselected_artists.append(artist)
        return None

    return artist_id
    

def get_artist_top_songs(user_token, artist_id):
    results = user_token.artist_top_tracks(artist_id, country='US')

    url_list = []

    for track in results['tracks'][:10]:
        print('track    : ' + track['name'])
        url_list.append(track['uri'])
    
    return url_list


def create_playlist(user_token, playlist_name, user_id):

    results = user_token.user_playlist_create(user_id, playlist_name, public=True, collaborative=False, description="")
    print(json.dumps(results, sort_keys=True, indent=4))

    return results['id']


def add_songs_to_playlist(user_token, user_id, playlist_id, tracks):
    user_token.user_playlist_add_tracks(user_id, playlist_id, tracks, position=None)


load_dotenv("festivalPlaylistApp\\.env.spotipy")

client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")
formatted_datetime = datetime.now().strftime("%Y%m%d%H%M%S%f")
username = "user-" + formatted_datetime
print(username)

def to_spotify(selected_artists, festival_name):
    user_token = get_user_token()
    user_id = get_user_info(user_token)
    
    full_url_list = []
    for artist in selected_artists:
        artist_id = get_artist_id(user_token, artist, unselected_artists)
        if (artist_id == None):
            continue
        url_list = get_artist_top_songs(user_token, artist_id)
        full_url_list.append(url_list)

    playlist_id = create_playlist(user_token, festival_name, user_id)

    for track_url in full_url_list:
        add_songs_to_playlist(user_token, user_id, playlist_id, track_url)   
    print(unselected_artists)
