from django.urls import path
from . import views

urlpatterns = [
    path('', views.track_list, name='track_list'),
    path('add/', views.track_add, name='track_add'),
    path('<int:track_id>/', views.track_detail, name='track_detail'),
    path('<int:track_id>/edit/', views.track_edit, name='track_edit'),
    path('<int:track_id>/delete/', views.track_delete, name='track_delete'),
    path('<int:track_id>/review/delete/', views.review_delete, name='review_delete'),
    path('reviews/<int:review_id>/like/', views.review_like_toggle, name='review_like_toggle'),
    path("<int:track_id>/favorite/", views.favorite_toggle, name="favorite_toggle"),
    path('favorite/<int:track_id>/toggle/', views.favorite_toggle, name='favorite_toggle'),
    path('playlists/', views.playlist_list, name='playlist_list'),
    path('playlists/create/', views.playlist_create, name='playlist_create'),
    path('playlists/<int:playlist_id>/', views.playlist_detail, name='playlist_detail'),
    path('playlists/<int:playlist_id>/edit/', views.playlist_edit, name='playlist_edit'),
    path('playlists/<int:playlist_id>/delete/', views.playlist_delete, name='playlist_delete'),
    path('playlists/<int:playlist_id>/add/<int:track_id>/', views.playlist_add_track, name='playlist_add_track'),
    path('playlists/<int:playlist_id>/remove/<int:track_id>/', views.playlist_remove_track, name='playlist_remove_track'),

]
