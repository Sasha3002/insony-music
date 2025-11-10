from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from .models import User, UserFollow, UserBlock
from .forms import RegisterForm
#from music.models import Review
from music.utils.xp import level_from_xp, level_progress, badge_for_level, badge_progress, badge_name
from music.models import Review, Favorite, Genre, Artist, Playlist
from django.db.models import Avg, F, FloatField, Q, Count
from django.views.decorators.http import require_POST
from django.http import JsonResponse


def login_view(request):
    next_url = request.GET.get('next') or request.POST.get('next')
    # якщо вже залогінений — перенаправляємо туди, куди просив, або в профіль
    if request.user.is_authenticated:
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
            return redirect(next_url)
        return redirect('profile')

    ctx = {"next_url": next_url, "username": ""}

    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        password = request.POST.get("password") or ""
        ctx["username"] = username  # щоб не вводити логін повторно

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # "Запам’ятай мене": якщо чекбокс не поставлено — сесія до закриття браузера
            if not request.POST.get("remember_me"):
                request.session.set_expiry(0)
            messages.success(request, f"Witaj, {user.username}!")
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect("profile")

        messages.error(request, "Nieprawidłowy login lub hasło")

    return render(request, "users/login.html", ctx)


def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def profile_view(request):
    user = request.user
    xp = getattr(user, "xp", 0)

    level = level_from_xp(xp)
    level_cur, xp_in_level, to_next = level_progress(xp)
    level_progress_pct = round((xp_in_level / 1000) * 100, 1)

    b = badge_for_level(level)
    badge_pct, badge_slug, next_badge_slug = badge_progress(level, xp_in_level)

    recent_reviews = Review.objects.filter(user=user).select_related('track', 'track__artist').order_by('-created_at')[:5]
    reviews_count = Review.objects.filter(user=user).count()
    
    playlists_number = Playlist.objects.filter(user=user, is_favorite = False).count()

    # Calculate average rating from user's reviews

    followers_count = UserFollow.objects.filter(following=user).count()
    following_count = UserFollow.objects.filter(follower=user).count()
   
    avg_data = Review.objects.filter(user=user).aggregate(
        avg_total=Avg(
            F('rhyme_imagery') + F('structure_rhythm') + F('style_execution') + 
            F('individuality') + F('atmosphere_vibe') + F('trend_relevance'),
            output_field=FloatField()
        )
    )
    # avg_total is the average sum of all 6 criteria (0-60), convert to 0-10 scale
    average_rating = round(avg_data['avg_total'] / 6, 1) if avg_data['avg_total'] else 0
    
    # Parse favorite genres (comma-separated)
    favorite_genres_list = [g.strip() for g in user.favorite_genres.split(',') if g.strip()] if user.favorite_genres else []
    
    # Parse favorite artists (comma-separated) 
    favorite_artists_list = [a.strip() for a in user.favorite_artists.split(',') if a.strip()] if user.favorite_artists else []

    favorites_count = Favorite.objects.filter(user=user).count()

    ctx = {
        "user": user,
        "xp": xp,
        "level": level,
        "level_in_xp": xp_in_level,
        "level_need_xp": 1000,
        "to_next": to_next,
        "level_progress_pct": level_progress_pct,
        "recent_reviews": recent_reviews,
        "reviews_count": reviews_count,
        "average_rating": average_rating,
        "favorite_genres_list": favorite_genres_list,
        "favorites_count": favorites_count,
        "favorite_artists_list": favorite_artists_list,
        "followers_count": followers_count,
        "following_count": following_count,
        "badge": b,                               # dict: slug/name/min/max
        "badge_slug": badge_slug,                 # 'bronze' / 'silver' / 'gold' / 'diamond'
        "badge_name": badge_name(badge_slug),     # 'Bronze' / 'Silver' ...
        "badge_pct": badge_pct,                   # % прогресу всередині бейджа
        "next_badge_slug": next_badge_slug,       # або None
        "next_badge_name": badge_name(next_badge_slug) if next_badge_slug else None,
        "playlists_number": playlists_number,
    }
    return render(request, "users/profile.html", ctx)



def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Konto utworzono. Witaj w Insony!")
            return redirect("profile")
        # якщо не валідно – упадемо до render із помилками
    else:
        form = RegisterForm()

    return render(request, "users/register.html", {"form": form})

@login_required
def profile_edit(request):
    user = request.user
    if request.method == "POST":
        if request.method == "POST":
            # Handle picture removal
            if request.POST.get('remove_picture') == 'true':
                if user.profile_picture:
                    user.profile_picture.delete()
                    user.profile_picture = None
            # Handle new picture upload
            elif 'profile_picture' in request.FILES:
                # Delete old picture if exists
                if user.profile_picture:
                    user.profile_picture.delete()
                user.profile_picture = request.FILES['profile_picture']
        user.email = request.POST.get("email", user.email)
        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name  = request.POST.get("last_name", user.last_name)
        user.favorite_genres = request.POST.get("favorite_genres", user.favorite_genres)
        user.favorite_artists = request.POST.get("favorite_artists", user.favorite_artists)
        user.bio = request.POST.get("bio", user.bio)
        user.save()
        messages.success(request, "Profil zaktualizowano.")
        return redirect("profile")
    
    all_genres = Genre.objects.all().order_by('name')
    all_artists = Artist.objects.all().order_by('name')

    # GET – показуємо форму з поточними значеннями
    context = {
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "favorite_genres": user.favorite_genres,
        "favorite_artists": user.favorite_artists,
        "bio": user.bio,
        "all_genres": all_genres,
        "all_artists": all_artists,
    }
    return render(request, "users/profile_edit.html", context)


def user_search(request):
    """Search for users"""
    q = request.GET.get('q', '').strip()
    
    users = []
    if q:
        excluded_ids = set()
        if request.user.is_authenticated:
            # Users I blocked
            excluded_ids.update(
                UserBlock.objects.filter(blocker=request.user).values_list('blocked_id', flat=True)
            )
            # Users who blocked me
            excluded_ids.update(
                UserBlock.objects.filter(blocked=request.user).values_list('blocker_id', flat=True)
            )
            # Exclude myself
            excluded_ids.add(request.user.id)
        
        users = User.objects.filter(
            Q(username__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q)
        ).exclude(id__in=excluded_ids).annotate(
            followers_count=Count('followers'),
            following_count=Count('following')
        )[:20]
        
        # Check if current user follows each user
        if request.user.is_authenticated:
            following_ids = set(
                UserFollow.objects.filter(follower=request.user).values_list('following_id', flat=True)
            )
            for user in users:
                user.is_followed = user.id in following_ids
        else:
            for user in users:
                user.is_followed = False
    
    return render(request, 'users/user_search.html', {
        'users': users,
        'q': q
    })


def user_profile_public(request, username):
    """View public user profile"""
    profile_user = User.objects.filter(username=username).first()
    
    if not profile_user:
        return render(request, 'users/404.html', status=404)
    
    # Check if blocked
    if request.user.is_authenticated:
        is_blocked = UserBlock.objects.filter(
            Q(blocker=request.user, blocked=profile_user) |
            Q(blocker=profile_user, blocked=request.user)
        ).exists()
        
        if is_blocked and request.user != profile_user:
            return render(request, 'users/user_blocked.html', status=403)
        
        is_following = UserFollow.objects.filter(
            follower=request.user,
            following=profile_user
        ).exists()
    else:
        is_following = False
    
    # Get stats
    followers_count = UserFollow.objects.filter(following=profile_user).count()
    following_count = UserFollow.objects.filter(follower=profile_user).count()
    
    # Get reviews
    recent_reviews = Review.objects.filter(user=profile_user).select_related('track', 'track__artist').order_by('-created_at')[:5]
    recent_reviews_count = Review.objects.filter(user=profile_user).count()
    
    # Get XP and level info
    xp = getattr(profile_user, "xp", 0)
    from music.utils.xp import level_from_xp, level_progress, badge_for_level, badge_progress, badge_name
    
    level = level_from_xp(xp)
    level_cur, xp_in_level, to_next = level_progress(xp)
    level_progress_pct = round((xp_in_level / 1000) * 100, 1)
    
    # Parse favorites
    favorite_genres_list = [g.strip() for g in profile_user.favorite_genres.split(',') if g.strip()] if profile_user.favorite_genres else []
    favorite_artists_list = [a.strip() for a in profile_user.favorite_artists.split(',') if a.strip()] if profile_user.favorite_artists else []
    
    favorites_count = Favorite.objects.filter(user=profile_user).count()
    playlists_number = Playlist.objects.filter(user=profile_user, is_favorite=False).count()
    
    # Average rating
    avg_data = Review.objects.filter(user=profile_user).aggregate(
        avg_total=Avg(
            F('rhyme_imagery') + F('structure_rhythm') + F('style_execution') + 
            F('individuality') + F('atmosphere_vibe') + F('trend_relevance'),
            output_field=FloatField()
        )
    )
    average_rating = round(avg_data['avg_total'] / 6, 1) if avg_data['avg_total'] else 0
    
    return render(request, 'users/user_profile_public.html', {
        'profile_user': profile_user,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count,
        'recent_reviews': recent_reviews,
        'recent_reviews_count': recent_reviews_count,
        'xp': xp,
        'level': level,
        'level_in_xp': xp_in_level,
        'level_progress_pct': level_progress_pct,
        'favorite_genres_list': favorite_genres_list,
        'favorite_artists_list': favorite_artists_list,
        'favorites_count': favorites_count,
        'playlists_number': playlists_number,
        'average_rating': average_rating,
    })


@login_required
@require_POST
def follow_toggle(request, username):
    """Toggle follow/unfollow user"""
    target_user = User.objects.filter(username=username).first()
    
    if not target_user:
        return JsonResponse({'ok': False, 'message': 'Użytkownik nie istnieje'})
    
    if target_user == request.user:
        return JsonResponse({'ok': False, 'message': 'Nie możesz obserwować siebie'})
    
    # Check if blocked
    is_blocked = UserBlock.objects.filter(
        Q(blocker=request.user, blocked=target_user) |
        Q(blocker=target_user, blocked=request.user)
    ).exists()
    
    if is_blocked:
        return JsonResponse({'ok': False, 'message': 'Nie możesz obserwować tego użytkownika'})
    
    follow = UserFollow.objects.filter(follower=request.user, following=target_user)
    
    if follow.exists():
        follow.delete()
        is_following = False
        message = 'Przestałeś obserwować'
    else:
        UserFollow.objects.create(follower=request.user, following=target_user)
        is_following = True
        message = 'Teraz obserwujesz'
    
    followers_count = UserFollow.objects.filter(following=target_user).count()
    
    return JsonResponse({
        'ok': True,
        'is_following': is_following,
        'followers_count': followers_count,
        'message': message
    })


@login_required
@require_POST
def block_toggle(request, username):
    """Toggle block/unblock user"""
    target_user = User.objects.filter(username=username).first()
    
    if not target_user:
        return JsonResponse({'ok': False, 'message': 'Użytkownik nie istnieje'})
    
    if target_user == request.user:
        return JsonResponse({'ok': False, 'message': 'Nie możesz zablokować siebie'})
    
    block = UserBlock.objects.filter(blocker=request.user, blocked=target_user)
    
    if block.exists():
        block.delete()
        is_blocked = False
        message = 'Użytkownik odblokowany'
    else:
        # Remove follow relationships
        UserFollow.objects.filter(
            Q(follower=request.user, following=target_user) |
            Q(follower=target_user, following=request.user)
        ).delete()
        
        UserBlock.objects.create(blocker=request.user, blocked=target_user)
        is_blocked = True
        message = 'Użytkownik zablokowany'
    
    return JsonResponse({
        'ok': True,
        'is_blocked': is_blocked,
        'message': message
    })


@login_required
def followers_list(request, username):
    """List user's followers"""
    profile_user = User.objects.filter(username=username).first()
    
    if not profile_user:
        return render(request, 'users/404.html', status=404)
    
    followers = UserFollow.objects.filter(following=profile_user).select_related('follower')
    
    return render(request, 'users/followers_list.html', {
        'profile_user': profile_user,
        'followers': followers
    })


@login_required
def following_list(request, username):
    """List users that user is following"""
    profile_user = User.objects.filter(username=username).first()
    
    if not profile_user:
        return render(request, 'users/404.html', status=404)
    
    following = UserFollow.objects.filter(follower=profile_user).select_related('following')
    
    return render(request, 'users/following_list.html', {
        'profile_user': profile_user,
        'following': following
    })

@login_required
@require_POST
def unblock_user(request, username):
    """Unblock a user"""
    target_user = User.objects.filter(username=username).first()
    
    if not target_user:
        return JsonResponse({'ok': False, 'message': 'Użytkownik nie istnieje'})
    
    block = UserBlock.objects.filter(blocker=request.user, blocked=target_user)
    
    if block.exists():
        block.delete()
        return JsonResponse({
            'ok': True,
            'message': f'Użytkownik {username} został odblokowany'
        })
    else:
        return JsonResponse({
            'ok': False,
            'message': 'Ten użytkownik nie jest zablokowany'
        })
    
def user_playlists_public(request, username):
    """View user's public playlists"""
    profile_user = User.objects.filter(username=username).first()
    
    if not profile_user:
        return render(request, 'users/404.html', status=404)
    
    # Check if blocked
    if request.user.is_authenticated:
        is_blocked = UserBlock.objects.filter(
            Q(blocker=request.user, blocked=profile_user) |
            Q(blocker=profile_user, blocked=request.user)
        ).exists()
        
        if is_blocked:
            return render(request, 'users/user_blocked.html', status=403)
    
    # Show only public playlists for other users, all playlists for own profile
    if request.user == profile_user:
        # Redirect to their own playlist page
        return redirect('playlist_list')
    else:
        playlists = Playlist.objects.filter(user=profile_user, is_favorite=False, is_public=True).order_by('-created_at')
    
    return render(request, 'music/playlist_list.html', {  
        'playlists': playlists,
        'profile_user': profile_user, 
        'viewing_other_user': True,  
    })

@login_required
def user_favorites(request):
    """Redirect to user's favorites playlist"""
    # Get or create favorites playlist
    favorites_playlist, created = Playlist.objects.get_or_create(
        user=request.user,
        is_favorite=True,
        defaults={'name': 'Ulubione'}
    )
    
    # Redirect to playlist detail
    return redirect('playlist_detail', playlist_id=favorites_playlist.id)

@login_required
def user_reviews(request):
    """View all user's reviews"""
    user = request.user
    
    # Get all reviews
    reviews = Review.objects.filter(user=user).select_related('track', 'track__artist').order_by('-created_at')
    
    return render(request, 'users/user_reviews.html', {
        'reviews': reviews,
    })

def user_reviews_public(request, username):
    """View all user's reviews (public)"""
    profile_user = User.objects.filter(username=username).first()
    
    if not profile_user:
        return render(request, 'users/404.html', status=404)
    
    # Check if blocked
    if request.user.is_authenticated:
        is_blocked = UserBlock.objects.filter(
            Q(blocker=request.user, blocked=profile_user) |
            Q(blocker=profile_user, blocked=request.user)
        ).exists()
        
        if is_blocked:
            return render(request, 'users/user_blocked.html', status=403)
    
    # Get all reviews
    reviews = Review.objects.filter(user=profile_user).select_related('track', 'track__artist').order_by('-created_at')
    
    return render(request, 'users/user_reviews.html', {
        'reviews': reviews,
        'profile_user': profile_user,  
        'viewing_other_user': request.user != profile_user, 
    })


@login_required
def account_delete(request):
    """Delete user account with password confirmation"""
    user = request.user
    
    if request.method == 'POST':
        password = request.POST.get('password', '')
        confirm_text = request.POST.get('confirm_text', '').strip()
        
        # Check if password is correct
        if not user.check_password(password):
            messages.error(request, 'Nieprawidłowe hasło')
            return render(request, 'users/account_delete.html')
        
        # Check if confirmation text matches
        if confirm_text != 'USUŃ KONTO':
            messages.error(request, 'Nieprawidłowy tekst potwierdzenia')
            return render(request, 'users/account_delete.html')
        
        # Delete the account
        username = user.username
        logout(request)
        user.delete()
        
        messages.success(request, f'Konto {username} zostało usunięte')
        return redirect('login')
    
    return render(request, 'users/account_delete.html')


@login_required
def account_settings(request):
    """Account settings page"""
    user = request.user
    
    # Get blocked users count
    blocked_count = UserBlock.objects.filter(blocker=user).count()
    
    return render(request, 'users/account_settings.html', {
        'blocked_count': blocked_count,
    })


@login_required
def password_change(request):
    """Change password"""
    if request.method == 'POST':
        current_password = request.POST.get('current_password', '')
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')
        
        # Check current password
        if not request.user.check_password(current_password):
            messages.error(request, 'Nieprawidłowe obecne hasło')
            return render(request, 'users/password_change.html')
        
        # Check new passwords match
        if new_password != confirm_password:
            messages.error(request, 'Nowe hasła nie są zgodne')
            return render(request, 'users/password_change.html')
        
        # Check password length
        if len(new_password) < 8:
            messages.error(request, 'Hasło musi mieć co najmniej 8 znaków')
            return render(request, 'users/password_change.html')
        
        # Change password
        request.user.set_password(new_password)
        request.user.save()
        
        # Re-login user
        from django.contrib.auth import update_session_auth_hash
        update_session_auth_hash(request, request.user)
        
        messages.success(request, 'Hasło zostało zmienione')
        return redirect('account_settings')
    
    return render(request, 'users/password_change.html')

@login_required
def blocked_users(request):
    """Manage blocked users"""
    user = request.user
    
    # Get blocked users
    blocked_users = UserBlock.objects.filter(blocker=user).select_related('blocked')
    
    return render(request, 'users/blocked_users.html', {
        'blocked_users': blocked_users,
    })