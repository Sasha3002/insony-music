"""
URL configuration for music_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static

def placeholder(request, name): return HttpResponse(f"<h2>{name}</h2><p>Wkrótce…</p>")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', include('music.urls')),
    path('chat/', include('chat.urls')),
    path('groups/', include('groups.urls')),
    path('events/', include('events.urls')),
    path('artists/', lambda r: placeholder(r, "Artyści"), name='artist_list'),
    path('genres/',  lambda r: placeholder(r, "Gatunki"), name='genre_list'),
    path('playlists/', lambda r: placeholder(r, "Playlisty"), name='playlist_list'),
    path('reviews/',   lambda r: placeholder(r, "Recenzje"),  name='review_list'),
    path('about/',     lambda r: placeholder(r, "O projekcie"), name='about'),
]
# Serving media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)