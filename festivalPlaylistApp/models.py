from django.db import models

class Festival(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

class Artist(models.Model):
    name = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    festivals = models.ManyToManyField(Festival, through='FestivalArtist')

class FestivalArtist(models.Model):
    festival = models.ForeignKey(Festival, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
