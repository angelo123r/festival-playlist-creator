from django.shortcuts import render, get_object_or_404
from .models import Festival, FestivalArtist, Artist

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
        return render(request, "pages/selected_artists.html", {'selected_artists': selected_artists})