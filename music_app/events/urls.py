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
]