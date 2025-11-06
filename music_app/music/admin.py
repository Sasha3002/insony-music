from django.contrib import admin
from .models import Artist, Genre, Track, Review, Favorite


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    # які колонки показуємо в списку
    list_display = (
        "title", "artist", "genre",
        "avg_cached", "reviews_cnt",
        "duration_display",  # читається з @property; сортування дамо по duration
        "authored_date", "created_at",
    )
    list_display_links = ("title",)               # клікабельний заголовок
    list_select_related = ("artist", "genre")
    search_fields = ("title", "artist__name")

    # зручні фільтри
    list_filter = (
        "genre", "artist",
        ("authored_date", admin.DateFieldListFilter),
        ("created_at", admin.DateFieldListFilter),
    )

    # ієрархія дат у верхній частині (можна змінити на 'created_at' за потреби)
    date_hierarchy = "authored_date"

    # дефолтне сортування
    ordering = ("-created_at",)

    # системні поля лише для читання у формі
    readonly_fields = ("created_at", "average_rating_cached", "reviews_count_cached")

    # групування полів у формі (необов’язково, але зручніше)
    fieldsets = (
        (None, {
            "fields": ("title", "artist", "genre", "description", "cover_image")
        }),
        ("Daty", {
            "fields": ("authored_date", "created_at")
        }),
        ("Czas", {
            "fields": ("duration",)
        }),
        ("Metryki (tylko do odczytu)", {
            "fields": ("average_rating_cached", "reviews_count_cached")
        }),
    )

    # колонки-метрики з можливістю сортування
    @admin.display(description="Średnia /100", ordering="average_rating_cached")
    def avg_cached(self, obj):
        return None if obj.average_rating_cached is None else round(obj.average_rating_cached, 1)

    @admin.display(description="Recenzje", ordering="reviews_count_cached")
    def reviews_cnt(self, obj):
        return obj.reviews_count_cached

    # дозволимо сортувати по duration для колонки duration_display
    @admin.display(description="Czas", ordering="duration")
    def duration_display(self, obj):
        return obj.duration_display


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "track", "user",
        "rhyme_imagery", "structure_rhythm", "style_execution",
        "individuality", "atmosphere_vibe", "trend_relevance",
        "created_at",
    )
    list_select_related = ("track", "user")
    search_fields = ("track__title", "user__username")
    list_filter = ("created_at", "track__genre")          # <— теж без rating
    ordering = ("-created_at",)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("track", "user", "created_at")
    search_fields = ("track__title", "user__username")
    list_filter = ("created_at",)