from django.urls import path
from .views import (
    login_view, logout_view, profile_view, register_view,
    profile_edit, user_search, user_profile_public, follow_toggle,
    block_toggle, followers_list, following_list, unblock_user, 
    user_playlists_public, user_favorites, user_reviews, user_reviews_public,
    account_delete, account_settings, password_change, blocked_users,
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('register/', register_view, name='register'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('search/', user_search, name='user_search'),
    path('u/<str:username>/', user_profile_public, name='user_profile_public'),
    path('u/<str:username>/follow/', follow_toggle, name='follow_toggle'),
    path('u/<str:username>/block/', block_toggle, name='block_toggle'),
    path('u/<str:username>/followers/', followers_list, name='followers_list'),
    path('u/<str:username>/following/', following_list, name='following_list'),
    path('u/<str:username>/unblock/', unblock_user, name='unblock_user'),
    path('u/<str:username>/playlists/', user_playlists_public, name='user_playlists_public'),
    path('favorites/', user_favorites, name='user_favorites'),
    path('reviews/', user_reviews, name='user_reviews'),
    path('u/<str:username>/reviews/', user_reviews_public, name='user_reviews_public'),
    path('profile/delete/', account_delete, name='account_delete'),
    path('settings/', account_settings, name='account_settings'),  
    path('settings/password/', password_change, name='password_change'),
    path('settings/blocked/', blocked_users, name='blocked_users'),
]
