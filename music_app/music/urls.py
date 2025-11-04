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
]
