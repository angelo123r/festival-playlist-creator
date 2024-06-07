from django.urls import path
from festivalPlaylistApp import views

urlpatterns = [
    path("", views.home, name="home"),
    path("festival/<int:festival_id>/",
         views.festival_artists, name="festival_artists"),
    path("selected_artists/<int:festival_id>/",
         views.selected_artists, name="selected_artists"),
    path("success/<int:festival_id>/", views.selected_artists, name="success"),
    path("fail/<int:festival_id>/", views.selected_artists, name="fail"),
    path("callback/", views.callback, name="callback"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact")
]
