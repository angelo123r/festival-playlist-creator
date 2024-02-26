from django.shortcuts import render, get_object_or_404
from .models import Festival, FestivalArtist, Artist
from .spotify_script import to_spotify

def home(request):
    festivals = Festival.objects.order_by('name').all()
    return render(request, "pages/home.html", {'festivals': festivals})

def festival_artists(request, festival_id):
    festival = get_object_or_404(Festival, pk=festival_id)
    artists = FestivalArtist.objects.filter(festival=festival)
    return render(request, "pages/festival_artists.html", {'festival': festival, 'artists': artists})

def selected_artists(request, festival_id):
    if request.method == 'POST':
        selected_artists_ids = request.POST.getlist('artists')
        selected_artists = Artist.objects.filter(id__in=selected_artists_ids)

        selected_artists_names = [artist.name for artist in selected_artists]

        festival = get_object_or_404(Festival, pk=festival_id)
        festival_name = festival.name
        print(festival_name)
        

        unselected_artists = to_spotify(selected_artists_names, festival_name)
        print(unselected_artists)
        print(len(unselected_artists))

        if len(unselected_artists) > 0 and len(selected_artists) != len(unselected_artists):
            return render(request, "pages/selected_artists.html", {'unselected_artists': unselected_artists})
        if len(unselected_artists) > 0:
            return render(request, "pages/fail.html")


        return render(request, "pages/successful.html")