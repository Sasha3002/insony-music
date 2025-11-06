from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from .models import User
from .forms import RegisterForm
#from music.models import Review
from music.utils.xp import level_from_xp, level_progress, badge_for_level, badge_progress, badge_name
from music.models import Review, Favorite
from django.db.models import Avg, F, FloatField


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

    recent_reviews = Review.objects.filter(user=user).select_related('track', 'track__artist').order_by('-created_at')[:10]
    
    # Calculate average rating from user's reviews
   
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
        "average_rating": average_rating,
        "favorite_genres_list": favorite_genres_list,
        "favorites_count": favorites_count,
        "favorite_artists_list": favorite_artists_list,
        "badge": b,                               # dict: slug/name/min/max
        "badge_slug": badge_slug,                 # 'bronze' / 'silver' / 'gold' / 'diamond'
        "badge_name": badge_name(badge_slug),     # 'Bronze' / 'Silver' ...
        "badge_pct": badge_pct,                   # % прогресу всередині бейджа
        "next_badge_slug": next_badge_slug,       # або None
        "next_badge_name": badge_name(next_badge_slug) if next_badge_slug else None,
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
        # просте оновлення базових полів
        user.email = request.POST.get("email", user.email)
        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name  = request.POST.get("last_name", user.last_name)
        user.favorite_genres  = request.POST.get("favorite_genres", user.favorite_genres)
        user.favorite_artists = request.POST.get("favorite_artists", user.favorite_artists)
        user.bio = request.POST.get("bio", user.bio)
        user.save()
        messages.success(request, "Profil zaktualizowano.")
        return redirect("profile")

    # GET – показуємо форму з поточними значеннями
    context = {
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "favorite_genres": user.favorite_genres,
        "favorite_artists": user.favorite_artists,
        "bio": user.bio,
    }
    return render(request, "users/profile_edit.html", context)
