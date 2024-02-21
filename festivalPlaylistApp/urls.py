from django.urls import path
from festivalPlaylistApp import views

urlpatterns = [
    path("", views.home, name="home"),
    path("festival/<int:festival_id>/", views.festival_artists, name="festival_artists"),
    path("selected_artists/", views.selected_artists, name="selected_artists"),
]