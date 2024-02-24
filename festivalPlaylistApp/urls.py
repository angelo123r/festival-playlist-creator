from django.urls import path
from festivalPlaylistApp import views

urlpatterns = [
    path("", views.home, name="home"),
    path("festival/<int:festival_id>/", views.festival_artists, name="festival_artists"),
    path("selected_artists/<int:festival_id>/", views.selected_artists, name="selected_artists"),
    path("success/<int:festival_id>/", views.selected_artists, name="success"),
]