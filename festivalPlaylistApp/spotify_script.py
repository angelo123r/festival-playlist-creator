import spotipy
from dotenv import load_dotenv
import os
import webbrowser
import sys
import json
from datetime import datetime, timedelta
from spotipy.oauth2 import SpotifyOAuth
from unidecode import unidecode
import re
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse



def get_user_info(user_token):
    user = user_token.current_user()

    user_id = user['id']
    print(user_id)

    return user_id


def get_artist_id(user_token, artist, unselected_artists):
    try:
        query = artist.lower()
        results = user_token.search(q=query, type="artist")    

        if results['artists']['items'] == []:
            unselected_artists.append(artist)
            return None, unselected_artists
        
        artist_id = results['artists']['items'][0]['id']
        artist_name = results['artists']['items'][0]['name']
        print(f"Artist Name: {artist_name}")
        
        artist_name = artist_name.replace("’", "'").replace('&','and')
        query = query.replace("’", "'").replace('&','and')

        if (re.sub(r'\W+', '', unidecode(artist_name.lower().replace(" ", ""))) != re.sub(r'\W+', '', unidecode(query.lower().strip().replace(" ", "")))):
            print(f"Artist Name: {artist_name} does not match query: {query}")
            unselected_artists.append(artist)
            artist_id = None

        return artist_id, unselected_artists
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, unselected_artists
    

def get_artist_top_songs(user_token, artist_id):
    try:
        results = user_token.artist_top_tracks(artist_id, country='US')

        url_list = []

        for track in results['tracks'][:10]:
            print('track    : ' + track['name'])
            url_list.append(track['uri'])
    
        return url_list
    
    except Exception as e:
        print(f"An error occured: {e}")
        return []

def create_playlist(user_token, playlist_name, user_id):

    results = user_token.user_playlist_create(user_id, playlist_name, public=True, collaborative=False, description="")
    print(json.dumps(results, sort_keys=True, indent=4))

    return results['id']


def add_songs_to_playlist(user_token, user_id, playlist_id, tracks):
    try:
        user_token.user_playlist_add_tracks(user_id, playlist_id, tracks)
    except Exception as e:
        print(f"An error occurred while adding tracks to the playlist: {e}")


def to_spotify(selected_artists, festival_name, sp):
    user_token = sp

    user_id = get_user_info(user_token)
    
    full_url_list = []
    unselected_artists = []
    print("SELECTED")
    print(selected_artists)
    
    for artist in selected_artists:
        artist_id, unselected_artists = get_artist_id(user_token, artist, unselected_artists)
        if (artist_id == None):
            continue
        url_list = get_artist_top_songs(user_token, artist_id)
        full_url_list.append(url_list)
    if all(not sublist for sublist in full_url_list):
        # full_url_list contains only empty sublists
        if len(selected_artists) == 0:
            unselected_artists.extend(selected_artists)
        print("INSIDE SUBLIST")
        print(unselected_artists)
        return unselected_artists

    if not (full_url_list):
        return unselected_artists
    
    playlist_id = create_playlist(user_token, festival_name, user_id)

    for track_url in full_url_list:
        add_songs_to_playlist(user_token, user_id, playlist_id, track_url)   
        
    return unselected_artists
