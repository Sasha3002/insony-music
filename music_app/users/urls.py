from django.urls import path
from .views import login_view, logout_view, profile_view, register_view, profile_edit

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('register/', register_view, name='register'),
    path('profile/edit/', profile_edit, name='profile_edit'),
]
