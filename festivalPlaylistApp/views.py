from django.shortcuts import render, get_object_or_404
from .models import Festival, FestivalArtist, Artist
from .spotify_script import get_user_token, get_user_info, get_artist_id, get_artist_top_songs

def home(request):
    festivals = Festival.objects.order_by('name').all()
    return render(request, "pages/home.html", {'festivals': festivals})

def festival_artists(request, festival_id):
    festival = get_object_or_404(Festival, pk=festival_id)
    artists = FestivalArtist.objects.filter(festival=festival)
    return render(request, "pages/festival_artists.html", {'festival': festival, 'artists': artists})

def selected_artists(request):
    if request.method == 'POST':
        selected_artists_ids = request.POST.getlist('artists')
        selected_artists = Artist.objects.filter(id__in=selected_artists_ids)

        selected_artists_names = [artist.name for artist in selected_artists]

        user_token = get_user_token()
        user_id = get_user_info(user_token)

        full_url_list = []
        for artist in selected_artists_names:
            artist_id = get_artist_id(user_token, artist)
            url_list = get_artist_top_songs(user_token, artist_id)
            full_url_list.append(url_list)
        
        

        return render(request, "pages/selected_artists.html", {'selected_artists': selected_artists})