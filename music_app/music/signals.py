from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.db.models import Avg, Count, F
from .models import Review, Track, ReviewLike, Favorite, Playlist,  PlaylistTrack
from .utils.xp import add_xp


def _recalc_track_stats(track_id: int):
    # Обчислюємо середнє значення total_points (сума всіх 6 критеріїв)
    agg = Review.objects.filter(track_id=track_id).aggregate(
        avg_total=Avg(
            F('rhyme_imagery') + F('structure_rhythm') + F('style_execution') +
            F('individuality') + F('atmosphere_vibe') + F('trend_relevance')
        ),
        cnt=Count('id')
    )
    
    # Конвертуємо у відсотки (0-100) для збереження в average_rating_cached
    avg_percent = (agg['avg_total'] / 60 * 100) if agg['avg_total'] else None
    
    Track.objects.filter(id=track_id).update(
        average_rating_cached=avg_percent,
        reviews_count_cached=agg['cnt'] or 0
    )

@receiver(post_save, sender=Review)
def review_saved(sender, instance, **kwargs):
    _recalc_track_stats(instance.track_id)

@receiver(post_delete, sender=Review)
def review_deleted(sender, instance, **kwargs):
    _recalc_track_stats(instance.track_id)

# ----------------------------- XP: КОНСТАНТИ -----------------------------
XP_REVIEW_WITH_TEXT = 250
XP_REVIEW_NO_TEXT   = 100
XP_LIKE_GOT         = 10    # лайк під моєю рецензією
XP_LIKE_GIVEN       = 10    # мій лайк чужій рецензії

# --------------- REVIEW: облік різниці між "з текстом"/"без" -------------
@receiver(pre_save, sender=Review)
def review_pre_save_capture_old(sender, instance: Review, **kwargs):
    if instance.pk:
        try:
            old = Review.objects.get(pk=instance.pk)
            instance._old_has_text = bool(old.text and old.text.strip())
        except Review.DoesNotExist:
            instance._old_has_text = False
    else:
        instance._old_has_text = False

@receiver(post_save, sender=Review)
def review_post_save_xp(sender, instance: Review, created: bool, **kwargs):
    new_has_text = bool(instance.text and instance.text.strip())
    user = instance.user

    if created:
        add_xp(user, XP_REVIEW_WITH_TEXT if new_has_text else XP_REVIEW_NO_TEXT)
    else:
        old_has_text = getattr(instance, "_old_has_text", False)
        if old_has_text != new_has_text:
            if new_has_text:
                add_xp(user, XP_REVIEW_WITH_TEXT - XP_REVIEW_NO_TEXT)   # +150
            else:
                add_xp(user, -(XP_REVIEW_WITH_TEXT - XP_REVIEW_NO_TEXT)) # -150

@receiver(post_delete, sender=Review)
def review_post_delete_xp(sender, instance: Review, **kwargs):
    had_text = bool(instance.text and instance.text.strip())
    add_xp(instance.user, -(XP_REVIEW_WITH_TEXT if had_text else XP_REVIEW_NO_TEXT))


# ------------------------------ LIKES: XP ---------------------------------
@receiver(post_save, sender=ReviewLike)
def like_post_save_xp(sender, instance: ReviewLike, created: bool, **kwargs):
    if not created:
        return
    add_xp(instance.review.user, XP_LIKE_GOT)   # автору рецензії
    add_xp(instance.user, XP_LIKE_GIVEN)        # тому, хто лайкнув

@receiver(post_delete, sender=ReviewLike)
def like_post_delete_xp(sender, instance: ReviewLike, **kwargs):
    add_xp(instance.review.user, -XP_LIKE_GOT)
    add_xp(instance.user, -XP_LIKE_GIVEN)

# --------------------------- FAVORITES: playlist ---------------------------

@receiver(post_save, sender=Favorite)
def add_to_favorites_playlist(sender, instance, created, **kwargs):
    """When a track is favorited, add it to user's favorites playlist"""
    if created:
        # Get or create favorites playlist
        favorites_playlist, _ = Playlist.objects.get_or_create(
            user=instance.user,
            is_favorite=True,
            defaults={
                'name': 'Ulubione',
                'description': 'Twoje ulubione utwory'
            }
        )
        
        # Add track to favorites playlist if not already there
        PlaylistTrack.objects.get_or_create(
            playlist=favorites_playlist,
            track=instance.track,
            defaults={'position': favorites_playlist.track_count}
        )


@receiver(post_delete, sender=Favorite)
def remove_from_favorites_playlist(sender, instance, **kwargs):
    """When a track is unfavorited, remove it from favorites playlist"""
    try:
        favorites_playlist = Playlist.objects.get(
            user=instance.user,
            is_favorite=True
        )
        PlaylistTrack.objects.filter(
            playlist=favorites_playlist,
            track=instance.track
        ).delete()
    except Playlist.DoesNotExist:
        pass