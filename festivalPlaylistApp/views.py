from django.shortcuts import render, get_object_or_404
from .models import Festival, FestivalArtist, Artist
from .spotify_script import to_spotify
from django.shortcuts import render, get_object_or_404, redirect
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException
from django.http import HttpResponse



SPOTIPY_CLIENT_ID = "ed5e6b6708294ee9b26e614b5cbfdac2"
SPOTIPY_CLIENT_SECRET = "dc7f1d3271c842f9b58941db51918c01"
SPOTIPY_REDIRECT_URI = "https://festijam.com/callback"



sp_oauth = SpotifyOAuth(SPOTIPY_CLIENT_ID,SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope="playlist-modify-public", cache_path=None)


def home(request):
    festivals = Festival.objects.order_by('name').all()
    return render(request, "pages/home.html", {'festivals': festivals})

def festival_artists(request, festival_id):
    festival = get_object_or_404(Festival, pk=festival_id)
    artists = FestivalArtist.objects.filter(festival=festival)
    return render(request, "pages/festival_artists.html", {'festival': festival, 'artists': artists})

def selected_artists(request, festival_id):
    #clear tokens


    selected_artists_ids = request.POST.getlist('artists')
    selected_artists = Artist.objects.filter(id__in=selected_artists_ids)

    selected_artists_length = (len(selected_artists))

    selected_artists_names = [artist.name for artist in selected_artists]
    print (selected_artists_names)
    
    festival = get_object_or_404(Festival, pk=festival_id)
    festival_name = festival.name

    if request.method == 'POST':

        if not request.session.get('access_token') and not request.session.get('refresh_token'):
            request.session['festival_name'] = festival_name
            request.session['selected_artists_length'] = selected_artists_length
            request.session['selected_artists_names'] = selected_artists_names
            auth_url = sp_oauth.get_authorize_url()
            return redirect(auth_url)
        
        access_token = request.session.get('access_token')
        sp = Spotify(auth=access_token)

        try:
            unselected_artists = to_spotify(selected_artists_names, festival_name, sp)
            print(unselected_artists)
            print(len(unselected_artists))

            if len(unselected_artists) > 0 and len(selected_artists) != len(unselected_artists):
                return render(request, "pages/selected_artists.html", {'unselected_artists': unselected_artists})
            if len(unselected_artists) > 0:
                return render(request, "pages/fail.html")
            return render(request, "pages/successful.html")
        except SpotifyException as e:
                if e.http_status == 401 and "The access token expired" in str(e):
                    print("Refreshing token..")
                    refreshed_token_info = sp_oauth.refresh_access_token(request.session['refresh_token'])
                    access_token = refreshed_token_info['access_token']
                    request.session['access_token'] = access_token
                    print(f"Refreshed!")
                return redirect("https://festijam.com/")


def callback(request):
    
    print("Callback route reached")
    
    festival_name = request.session.get('festival_name', '')
    selected_artists_length = request.session.get('selected_artists_length', '')
    selected_artists_names = request.session.get('selected_artists_names', [])

    print(festival_name)
    print(selected_artists_length)
    print (selected_artists_names)

    token_info = sp_oauth.get_access_token(request.GET.get('code'))
    print("Token info received")

    access_token = token_info['access_token']
    expires_at = token_info['expires_at']
    refresh_token = token_info.get('refresh_token', None)

    request.session['access_token'] = access_token
    request.session['refresh_token'] = refresh_token

    sp = Spotify(auth=access_token)

    try:
        unselected_artists = to_spotify(selected_artists_names, festival_name, sp)
        print(unselected_artists)
        print(len(unselected_artists))

        request.session.pop('festival_name', None)
        request.session.pop('selected_artists_length', None)
        request.session.pop('selected_artists_names', None)

        if len(unselected_artists) > 0 and selected_artists_length != len(unselected_artists):
            return render(request, "pages/selected_artists.html", {'unselected_artists': unselected_artists})
        if len(unselected_artists) > 0:
            return render(request, "pages/fail.html")
        return render(request, "pages/successful.html")
    except SpotifyException as e:
            if e.http_status == 401 and "The access token expired" in str(e):
                print("Refreshing token..")
                refreshed_token_info = sp_oauth.refresh_access_token(request.session['refresh_token'])
                access_token = refreshed_token_info['access_token']
                request.session['access_token'] = access_token
                print(f"Refreshed!")
            return redirect("https://festijam.com/")
