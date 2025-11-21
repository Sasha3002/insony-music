from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('group/<slug:group_slug>/create/', views.event_create, name='event_create'),
    path('<slug:slug>/', views.event_detail, name='event_detail'),
    path('<slug:slug>/edit/', views.event_edit, name='event_edit'),
    path('<slug:slug>/delete/', views.event_delete, name='event_delete'),
    path('<slug:slug>/attend/', views.event_attend, name='event_attend'),
    path('<slug:slug>/rate/', views.rate_event, name='rate_event'),  
    path('<slug:slug>/delete-rating/', views.delete_rating, name='delete_rating'),
    path('<slug:slug>/create-poll/', views.create_poll, name='create_poll'), 
    path('poll/<int:poll_id>/vote/', views.vote_on_poll, name='vote_on_poll'),  
    path('poll/<int:poll_id>/close/', views.close_poll, name='close_poll'),  
    path('poll/<int:poll_id>/apply/', views.apply_poll_changes, name='apply_poll_changes'),  
    path('<slug:slug>/playlist/add/', views.event_playlist_add_track, name='event_playlist_add_track'), 
    path('<slug:slug>/playlist/remove/<int:track_id>/', views.event_playlist_remove_track, name='event_playlist_remove_track'),  
]