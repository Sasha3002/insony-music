from django.conf import settings
from django.db import models
from django.db.models import CheckConstraint, Q, UniqueConstraint


class Artist(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)

    def __str__(self):
        return self.name


class Track(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name="tracks"
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL, null=True, blank=True, related_name="tracks"
    )
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="added_tracks",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    average_rating_cached = models.FloatField(null=True, blank=True, default=None)
    reviews_count_cached = models.PositiveIntegerField(default=0)
    authored_date = models.DateField(
        "Data utworu (autora)", null=True, blank=True, db_index=True,
        help_text="Data stworzenia / wydania utworu przez autora."
    )

    duration = models.DurationField(
        "Czas trwania", null=True, blank=True,
        help_text="Format: hh:mm:ss lub mm:ss"
    )
    
    cover_image = models.URLField(
        "Track cover", max_length=500, null=True, blank=True,
        help_text="URL of the cover image from Cover Art Archive"
    )


    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["artist", "title"]),
            models.Index(fields=["genre"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.artist.name}"

    @property
    def average_rating(self):
        return self.average_rating_cached
    
    @property
    def duration_display(self) -> str:
        if not self.duration:
            return "—"
        total = int(self.duration.total_seconds())
        h, rem = divmod(total, 3600)
        m, s = divmod(rem, 60)
        return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


class Review(models.Model):
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews"
    )
    title = models.CharField(max_length=120, blank=True)


    # 6 критеріїв по 0–10
    rhyme_imagery = models.PositiveSmallIntegerField(default=0)       # Рими / Образи
    structure_rhythm = models.PositiveSmallIntegerField(default=0)    # Структура / Ритміка
    style_execution = models.PositiveSmallIntegerField(default=0)     # Реалізація стилю
    individuality = models.PositiveSmallIntegerField(default=0)       # Індивідуальність / Харизма
    atmosphere_vibe = models.PositiveSmallIntegerField(default=0)     # Атмосфера / Вайб
    trend_relevance = models.PositiveSmallIntegerField(default=0)     # Трендовість / Актуальність жанру

    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        constraints = [
            UniqueConstraint(fields=["track", "user"], name="uniq_review_per_user_track"),
            CheckConstraint(check=Q(rhyme_imagery__gte=0) & Q(rhyme_imagery__lte=10), name="ri_0_10"),
            CheckConstraint(check=Q(structure_rhythm__gte=0) & Q(structure_rhythm__lte=10), name="sr_0_10"),
            CheckConstraint(check=Q(style_execution__gte=0) & Q(style_execution__lte=10), name="se_0_10"),
            CheckConstraint(check=Q(individuality__gte=0) & Q(individuality__lte=10), name="ind_0_10"),
            CheckConstraint(check=Q(atmosphere_vibe__gte=0) & Q(atmosphere_vibe__lte=10), name="av_0_10"),
            CheckConstraint(check=Q(trend_relevance__gte=0) & Q(trend_relevance__lte=10), name="tr_0_10"),
        ]
        indexes = [models.Index(fields=["track", "user"])]

    # сума всіх критеріїв (0..60)
    @property
    def total_points(self):
        return (
            self.rhyme_imagery
            + self.structure_rhythm
            + self.style_execution
            + self.individuality
            + self.atmosphere_vibe
            + self.trend_relevance
        )

    # у відсотках (0..100)
    @property
    def total_percent(self):
        return (self.total_points / 60) * 100 if self.total_points else 0

    def __str__(self):
        return f"{self.track} · {self.user} · {self.total_points}/60 ({self.total_percent:.1f}%)"

class ReviewLike(models.Model):
    review = models.ForeignKey('Review', on_delete=models.CASCADE, related_name='likes')
    user   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='review_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('review', 'user')

    def __str__(self):
        return f"{self.user_id} ♥ {self.review_id}"

class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorite_tracks"
    )
    track = models.ForeignKey(
        "Track",
        on_delete=models.CASCADE,
        related_name="favorites"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("user", "track"),)
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["user", "track"]),
            models.Index(fields=["track", "created_at"]),
        ]

    def __str__(self):
        return f"{self.user} → {self.track} (★ {self.created_at:%Y-%m-%d})"
    

class Playlist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="playlists"
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='playlist_covers/', blank=True, null=True)
    is_favorite = models.BooleanField(default=False)  # Special flag for favorites playlist
    is_public = models.BooleanField(default=False)
    is_event_playlist = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    
    # Many-to-many relationship with Track through PlaylistTrack
    tracks = models.ManyToManyField(
        'Track',
        through='PlaylistTrack',
        related_name='playlists',
        blank=True
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_favorite']),
        ]
        constraints = [
            # Each user can have only one favorites playlist
            models.UniqueConstraint(
                fields=['user'],
                condition=models.Q(is_favorite=True),
                name='unique_favorite_playlist_per_user'
            )
        ]

    def __str__(self):
        return f"{self.name} - {self.user.username}"

    @property
    def track_count(self):
        return self.tracks.count()

    @property
    def total_duration(self):
        from datetime import timedelta
        total = timedelta()
        for track in self.tracks.all():
            if track.duration:
                total += track.duration
        return total


class PlaylistTrack(models.Model):
    """Through model for many-to-many relationship with ordering"""
    playlist = models.ForeignKey(
        Playlist,
        on_delete=models.CASCADE,
        related_name='playlist_tracks'
    )
    track = models.ForeignKey(
        'Track',
        on_delete=models.CASCADE,
        related_name='in_playlists'
    )
    position = models.PositiveIntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['position', 'added_at']
        unique_together = [['playlist', 'track']]
        indexes = [
            models.Index(fields=['playlist', 'position']),
        ]

    def __str__(self):
        return f"{self.track.title} in {self.playlist.name}"


