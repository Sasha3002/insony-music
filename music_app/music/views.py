from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Track, Artist, Genre, Review, ReviewLike, Favorite, Playlist, PlaylistTrack
from django.contrib import messages
from .forms import ReviewForm
from django.db.models import Avg, Count, F, ExpressionWrapper, FloatField, Q, Value, Max
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator
from django.urls import reverse
from urllib.parse import urlencode
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import TrackEditForm
from users.models import User, UserBlock





def track_list(request):
    q = (request.GET.get('q') or '').strip()
    sort = request.GET.get('sort', 'custom')
    page = request.GET.get('page') or 1

    qs = (
        Track.objects
        .select_related('artist', 'genre')
        .annotate(avg=Coalesce(F('average_rating_cached'), Value(0.0)))
    )

    # Search by track name, artist name, and genre
    if q:
        qs = qs.filter(
            Q(title__icontains=q) |
            Q(artist__name__icontains=q) |
            Q(genre__name__icontains=q)
        )

    favorite_ids = set()
    if request.user.is_authenticated:
        favorite_ids = set(
            Favorite.objects.filter(user=request.user)
            .values_list('track_id', flat=True)
        )

    artist_number = Artist.objects.count()
    review_count = Review.objects.count()

    sort_map = {
        'custom':      '-created_at',
        'date':        '-created_at',
        'date_asc':    'created_at',
        'title':       'title',
        'title_desc':  '-title',
        'artist':      'artist__name',
        'artist_desc': '-artist__name',
        'genre':       'genre__name',
        'genre_desc':  '-genre__name',
        'rating_high': '-average_rating_cached',
        'rating_low':  'average_rating_cached',
        'reviews':     '-reviews_count_cached',
    }
    order_by = sort_map.get(sort, '-created_at')
    qs = qs.order_by(order_by, 'id') 
    paginator = Paginator(qs, 12)
    tracks_page = paginator.get_page(page)

    return render(request, 'music/track_list.html', {
        'tracks': tracks_page,   
        'sort': sort,
        'q': q,
        'favorite_ids': favorite_ids,
        'artist_number': artist_number,
        'review_count': review_count,
    })


def is_staff(user):
    return user.is_authenticated and user.is_staff

def track_detail(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    agg = track.reviews.aggregate(
        ri_avg=Avg('rhyme_imagery'),
        sr_avg=Avg('structure_rhythm'),
        se_avg=Avg('style_execution'),
        ind_avg=Avg('individuality'),
        av_avg=Avg('atmosphere_vibe'),
        tr_avg=Avg('trend_relevance'),
        total=Count('id'),
    )

    mode = request.GET.get("mode", "review")
    if mode not in ("review", "no_text"):
        mode = "review"

    if agg['total']:
        criteria = [agg['ri_avg'], agg['sr_avg'], agg['se_avg'], agg['ind_avg'], agg['av_avg'], agg['tr_avg']]
        avg_percent = sum(filter(None, criteria)) / len(criteria) * 10
    else:
        avg_percent = None

    total_reviews = track.reviews_count_cached
    sort = request.GET.get('sort', 'new')
    order_by = {
        'new': '-created_at',
        'old': 'created_at',
        'high': '-rhyme_imagery',  
        'low': 'rhyme_imagery',
    }.get(sort, '-created_at')

    reviews_qs = track.reviews.select_related('user').annotate(likes_count=Count('likes')).order_by(order_by)
    page_number = request.GET.get('page') or 1
    paginator = Paginator(reviews_qs, 5)
    reviews_page = paginator.get_page(page_number)

    liked_ids = set()
    if request.user.is_authenticated:
        liked_ids = set(
            ReviewLike.objects.filter(user=request.user, review__track=track)
            .values_list('review_id', flat=True)
        )


    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(user=request.user, track=track).exists()

    user_review = None
    form = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(track=track, user=request.user).first()
        form = ReviewForm(instance=user_review)
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=user_review)
            if form.is_valid():
                r = form.save(commit=False)
                r.track = track
                r.user = request.user
                if mode == "no_text":
                    r.text = ""
                r.save()
                messages.success(request, 'Twoja recenzja została zapisana.')
                return redirect(f"{reverse('track_detail', args=[track.id])}?sort={sort}&mode={mode}")
            else:
                messages.error(request, 'Popraw błędy w formularzu.')

    def val(field_name):
        return getattr(user_review, field_name, 0) if user_review else 0
    
    def bound(field_name):
        return form[field_name] if form is not None else None
    
    playlists= Playlist.objects.filter(user=request.user, is_favorite = False) if request.user.is_authenticated else []

    criteria_cfg = [
        {"label": "Rymy / Obrazy",            "short": "ri",  "field": "rhyme_imagery",    "color": "crit--blue",   "value": val("rhyme_imagery"),    "bound": bound("rhyme_imagery")},
        {"label": "Struktura / Rytmika",       "short": "sr",  "field": "structure_rhythm", "color": "crit--indigo", "value": val("structure_rhythm"), "bound": bound("structure_rhythm")},
        {"label": "Styl / Realizacja",         "short": "se",  "field": "style_execution",  "color": "crit--violet", "value": val("style_execution"),  "bound": bound("style_execution")},
        {"label": "Indywidualność / Charyzma", "short": "ind", "field": "individuality",    "color": "crit--purple", "value": val("individuality"),    "bound": bound("individuality")},
        {"label": "Atmosfera / Wajb",          "short": "av",  "field": "atmosphere_vibe",  "color": "crit--cyan",   "value": val("atmosphere_vibe"),  "bound": bound("atmosphere_vibe")},
        {"label": "Trend / Aktualność",        "short": "tr",  "field": "trend_relevance",  "color": "crit--pink",   "value": val("trend_relevance"),  "bound": bound("trend_relevance")},
    ]

    return render(request, 'music/track_detail.html', {
        'track': track,
        'avg_percent': avg_percent,         
        'criteria_avg': agg,                
        'total_reviews': total_reviews,
        'reviews_page': reviews_page,
        'liked_ids': liked_ids,
        'sort': sort,
        'is_favorited': is_favorited,
        'form': form,
        'user_review': user_review,
        'playlists': playlists,
        'criteria_cfg': criteria_cfg,   
        'mode': mode,
    })


@require_POST
def review_like_toggle(request, review_id):
    if not request.user.is_authenticated:
        return JsonResponse({"ok": False, "reason": "auth"}, status=401)
    review = get_object_or_404(Review, id=review_id)
    like_qs = ReviewLike.objects.filter(review=review, user=request.user)
    if like_qs.exists():
        like_qs.delete()
        liked = False
    else:
        ReviewLike.objects.create(review=review, user=request.user)
        liked = True
    count = ReviewLike.objects.filter(review=review).count()
    return JsonResponse({'ok': True, 'liked': liked, 'count': count})

@login_required(login_url='/users/login/')
def review_delete(request, track_id):
    sort = request.GET.get('sort', 'new')
    page = request.GET.get('page', '1')

    track = get_object_or_404(Track, id=track_id)
    review = Review.objects.filter(track=track, user=request.user).first()
    if not review:
        messages.error(request, 'Nie masz recenzji do usunięcia.')
        return redirect(f"{reverse('track_detail', args=[track.id])}?{urlencode({'sort': sort, 'page': page})}")

    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Recenzja została usunięta.')
    return redirect(f"{reverse('track_detail', args=[track.id])}?{urlencode({'sort': sort, 'page': page})}")


@login_required(login_url='/users/login/')
def track_add(request):
    if not request.user.is_staff:
        return render(request, "music/403.html", status=403)
    artists = Artist.objects.all()
    genres = Genre.objects.all()
    if request.method == 'POST':
        title = request.POST['title']
        artist = Artist.objects.get(id=request.POST['artist'])
        genre = Genre.objects.get(id=request.POST['genre'])
        Track.objects.create(
            title=title, artist=artist, genre=genre,
            description=request.POST.get('description', ''),
            created_by=request.user
        )
        messages.success(request, 'Utwór został dodany!')
        return redirect('track_list')
    return render(request, 'music/track_add.html', {'artists': artists, 'genres': genres})


@login_required(login_url='/users/login/')
def track_edit(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    if not request.user.is_staff:
        return render(request, "music/403.html", status=403)
    if request.method == 'POST':
        form = TrackEditForm(request.POST, instance=track)
        if form.is_valid():
            form.save()
            messages.success(request, "Utwór został zaktualizowany.")
            return redirect('track_detail', track_id=track.id)
        else:
            messages.error(request, "Popraw błędy w formularzu.")
    else:
        form = TrackEditForm(instance=track)

    return render(request, 'music/track_edit.html', {
        'form': form,
        'track': track,
    })



@login_required(login_url='/users/login/')
def track_delete(request, track_id):
    if not request.user.is_staff:
        return render(request, "music/403.html", status=403)
    track = get_object_or_404(Track, id=track_id)

    if request.method == 'POST':
        title = track.title
        track.delete()
        messages.success(request, f'Utwór "{title}" został usunięty.')
        return redirect('track_list')
    return render(request, 'music/track_delete_confirm.html', {'track': track})


@require_POST
@login_required(login_url="/users/login/")
def favorite_toggle(request, track_id):
    track = get_object_or_404(Track, pk=track_id)

    fav_qs = Favorite.objects.filter(user=request.user, track=track)
    already = fav_qs.exists()

    if already:
        fav_qs.delete()
        is_favorited = False
    else:
        Favorite.objects.create(user=request.user, track=track)
        is_favorited = True
    return JsonResponse({"ok": True, "favorited": is_favorited, "track_id": track_id})


@login_required
def playlist_list(request):
    playlists = Playlist.objects.filter(user=request.user, is_event_playlist=False).order_by('-created_at')
    
    return render(request, 'music/playlist_list.html', {
        'playlists': playlists
    })


@login_required
def playlist_detail(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    is_owner = playlist.user == request.user
    if not is_owner and not playlist.is_public:
        return render(request, 'music/403.html', status=403)
    
    playlist_tracks = PlaylistTrack.objects.filter(
        playlist=playlist
    ).select_related('track', 'track__artist', 'track__genre').order_by('position')
    
    return render(request, 'music/playlist_detail.html', {
        'playlist': playlist,
        'playlist_tracks': playlist_tracks,
        'is_owner': is_owner,  
    })


@login_required
def playlist_create(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        is_public = request.POST.get('is_public') == 'on'
        
        if not name:
            messages.error(request, 'Nazwa playlisty jest wymagana')
            return redirect('playlist_list')
        
        playlist = Playlist.objects.create(
            user=request.user,
            name=name,
            description=description,
            is_public=is_public
        )
        
        if 'cover_image' in request.FILES:
            playlist.cover_image = request.FILES['cover_image']
            playlist.save()
        
        messages.success(request, f'Playlista "{name}" została utworzona!')
        return redirect('playlist_detail', playlist_id=playlist.id)
    
    return render(request, 'music/playlist_create.html')


@login_required
def playlist_edit(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)

    if playlist.is_favorite:
        messages.error(request, 'Nie możesz edytować playlisty ulubionych')
        return redirect('playlist_detail', playlist_id=playlist.id)
    
    if request.method == 'POST':
        playlist.name = request.POST.get('name', playlist.name)
        playlist.description = request.POST.get('description', playlist.description)
        playlist.is_public = request.POST.get('is_public') == 'on'
        
        if 'cover_image' in request.FILES:
            if playlist.cover_image:
                playlist.cover_image.delete()
            playlist.cover_image = request.FILES['cover_image']
        
        if request.POST.get('remove_cover') == 'true':
            if playlist.cover_image:
                playlist.cover_image.delete()
                playlist.cover_image = None
        
        playlist.save()
        messages.success(request, 'Playlista zaktualizowana!')
        return redirect('playlist_detail', playlist_id=playlist.id)
    
    return render(request, 'music/playlist_edit.html', {'playlist': playlist})


@login_required
def playlist_delete(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)

    if playlist.is_favorite:
        messages.error(request, 'Nie możesz usunąć playlisty ulubionych')
        return redirect('playlist_list')
    
    if request.method == 'POST':
        name = playlist.name
        playlist.delete()
        messages.success(request, f'Playlista "{name}" została usunięta')
        return redirect('playlist_list')
    
    return render(request, 'music/playlist_delete_confirm.html', {'playlist': playlist})


@login_required
@require_POST
def playlist_add_track(request, playlist_id, track_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    track = get_object_or_404(Track, id=track_id)
    
    if PlaylistTrack.objects.filter(playlist=playlist, track=track).exists():
        return JsonResponse({'ok': False, 'message': 'Utwór już jest w playliście'})
    
    position = playlist.track_count
    PlaylistTrack.objects.create(
        playlist=playlist,
        track=track,
        position=position
    )
    
    return JsonResponse({'ok': True, 'message': 'Utwór dodany do playlisty'})


@login_required
@require_POST
def playlist_remove_track(request, playlist_id, track_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)
    
    if playlist.is_favorite:
        return JsonResponse({'ok': False, 'message': 'Usuń utwór z ulubionych zamiast tego'})
    
    PlaylistTrack.objects.filter(playlist=playlist, track_id=track_id).delete()
    
    remaining = PlaylistTrack.objects.filter(playlist=playlist).order_by('position')
    for i, pt in enumerate(remaining):
        pt.position = i
        pt.save()
    
    return JsonResponse({'ok': True, 'message': 'Utwór usunięty z playlisty'})
