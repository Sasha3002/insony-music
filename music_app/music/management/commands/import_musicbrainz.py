"""
Django management command для імпорту треків з MusicBrainz API
"""
import datetime
import requests
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.contrib.auth import get_user_model
from music.models import Track, Artist, Genre

User = get_user_model()


class Command(BaseCommand):
    help = 'Importuje utwory z MusicBrainz API do bazy danych'

    def add_arguments(self, parser):
        parser.add_argument(
            '--artist',
            type=str,
            help='Wyszukiwanie utworów według nazwy wykonawcy',
        )
        parser.add_argument(
            '--title',
            type=str,
            help='Wyszukiwanie utworów według tytułu utworu',
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=10,
            help='Maksymalna liczba utworów do importu (domyślnie: 10)',
        )
        parser.add_argument(
            '--skip-duplicates',
            action='store_true',
            help='Pomijaj utwory, które już istnieją w bazie danych',
        )
        parser.add_argument(
            '--default-genre',
            type=str,
            help='Domyślny gatunek dla importowanych utworów',
        )

    def handle(self, *args, **options):
        try:
            import musicbrainzngs
        except ImportError:
            raise CommandError(
                'Pakiet musicbrainzngs nie został zainstalowany. '
                'Zainstaluj go: pip install musicbrainzngs'
            )

        # Налаштування MusicBrainz API
        musicbrainzngs.set_useragent(
            "MusicApp",
            "1.0",
            "https://example.com"
        )

        artist_query = options.get('artist')
        title_query = options.get('title')
        limit = options.get('limit')
        skip_duplicates = options.get('skip_duplicates')
        default_genre_name = options.get('default_genre')

        if not artist_query and not title_query:
            raise CommandError(
                'Należy podać co najmniej jeden parametr: --artist lub --title'
            )

        # Отримання адміністратора (ID = 3)
        try:
            admin_user = User.objects.get(id=3)
            self.stdout.write(
                self.style.SUCCESS(f'Użytkownik admin znaleziony: {admin_user.username}')
            )
        except User.DoesNotExist:
            raise CommandError(
                'Użytkownik admin (ID=3) nie został znaleziony w bazie danych. '
                'Utwórz użytkownika admin lub zmień ID w kodzie.'
            )

        # Отримання або створення жанру за замовчуванням
        default_genre = None
        if default_genre_name:
            default_genre, _ = Genre.objects.get_or_create(name=default_genre_name)
            self.stdout.write(
                self.style.SUCCESS(f'Domyślny gatunek: {default_genre.name}')
            )

        self.stdout.write(self.style.SUCCESS('Wyszukiwanie utworów na MusicBrainz...'))

        try:
            # Пошук записів (recordings) на MusicBrainz
            search_query = []
            if artist_query:
                search_query.append(f'artist:"{artist_query}"')
            if title_query:
                search_query.append(f'recording:"{title_query}"')
            
            query = ' AND '.join(search_query)
            
            result = musicbrainzngs.search_recordings(
                query=query,
                limit=limit
            )

            recordings = result.get('recording-list', [])
            
            if not recordings:
                self.stdout.write(
                    self.style.WARNING('Nie znaleziono utworów')
                )
                return

            self.stdout.write(
                self.style.SUCCESS(
                    f'Znaleziono {len(recordings)} utworów'
                )
            )

            imported_count = 0
            skipped_count = 0

            for recording in recordings:
                track_title = recording.get('title', 'Unknown Title')
                
                # Отримання інформації про виконавця
                artist_credit = recording.get('artist-credit', [])
                if artist_credit:
                    artist_name = artist_credit[0].get('artist', {}).get('name', 'Unknown Artist')
                else:
                    artist_name = 'Unknown Artist'

                # Отримання тривалості
                duration_ms = recording.get('length')
                duration = None
                if duration_ms:
                    try:
                        duration = datetime.timedelta(milliseconds=int(duration_ms))
                    except (ValueError, TypeError):
                        pass

                # Отримання обкладинки та дати випуску з Cover Art Archive
                cover_url = None
                authored_date = None
                release_list = recording.get('release-list', [])
                if release_list:
                    # Беремо перший реліз для пошуку обкладинки та дати
                    first_release = release_list[0]
                    release_id = first_release.get('id')
                    
                    # Отримання дати випуску
                    release_date_str = first_release.get('date')
                    if release_date_str:
                        try:
                            # MusicBrainz повертає дати у форматі YYYY, YYYY-MM або YYYY-MM-DD
                            date_parts = release_date_str.split('-')
                            if len(date_parts) == 3:
                                authored_date = datetime.date(
                                    int(date_parts[0]),
                                    int(date_parts[1]),
                                    int(date_parts[2])
                                )
                            elif len(date_parts) == 2:
                                # Якщо лише рік та місяць, використовуємо перший день місяця
                                authored_date = datetime.date(
                                    int(date_parts[0]),
                                    int(date_parts[1]),
                                    1
                                )
                            elif len(date_parts) == 1:
                                # Якщо лише рік, використовуємо 1 січня
                                authored_date = datetime.date(int(date_parts[0]), 1, 1)
                        except (ValueError, TypeError) as e:
                            self.stdout.write(
                                self.style.WARNING(
                                    f'Nie udało się przetworzyć daty "{release_date_str}": {str(e)}'
                                )
                            )
                    
                    if release_id:
                        try:
                            cover_response = requests.get(
                                f'https://coverartarchive.org/release/{release_id}',
                                timeout=5
                            )
                            if cover_response.status_code == 200:
                                cover_data = cover_response.json()
                                images = cover_data.get('images', [])
                                if images:
                                    # Беремо перше зображення (зазвичай фронт обкладинки)
                                    for img in images:
                                        if img.get('front', False):
                                            cover_url = img.get('thumbnails', {}).get('small') or img.get('image')
                                            break
                                    if not cover_url and images:
                                        cover_url = images[0].get('thumbnails', {}).get('small') or images[0].get('image')
                        except Exception as e:
                            self.stdout.write(
                                self.style.WARNING(
                                    f'Nie udało się pobrać okładki: {str(e)}'
                                )
                            )

                # Перевірка на дублікати
                artist_obj, _ = Artist.objects.get_or_create(name=artist_name)
                
                if skip_duplicates:
                    if Track.objects.filter(title=track_title, artist=artist_obj).exists():
                        self.stdout.write(
                            self.style.WARNING(
                                f'Pominięto (duplikat): {track_title} - {artist_name}'
                            )
                        )
                        skipped_count += 1
                        continue

                # Отримання жанру з пріоритетом:
                # 1. Теги з MusicBrainz (якщо немає default_genre)
                # 2. Параметр --default-genre
                # 3. Жанр "Unknown" як fallback
                genre = None
                tags = recording.get('tag-list', [])
                
                if default_genre:
                    # Якщо вказано --default-genre, використовуємо його
                    genre = default_genre
                elif tags:
                    # Використовуємо перший тег з MusicBrainz як жанр
                    genre_name = tags[0].get('name', '').capitalize()
                    if genre_name:
                        genre, _ = Genre.objects.get_or_create(name=genre_name)
                
                # Якщо жанр все ще не визначено, створюємо "Unknown"
                if not genre:
                    genre, _ = Genre.objects.get_or_create(name='Unknown')

                # Створення треку з адміністратором
                with transaction.atomic():
                    track = Track.objects.create(
                        title=track_title,
                        artist=artist_obj,
                        genre=genre,
                        created_by=admin_user,
                        duration=duration,
                        cover_image=cover_url,
                        authored_date=authored_date,
                        description=f'Zaimportowano z MusicBrainz (ID: {recording.get("id", "N/A")})'
                    )

                imported_count += 1
                cover_status = '🖼️' if cover_url else '📝'
                date_status = f'📅 {authored_date}' if authored_date else ''
                genre_status = f'🎵 {genre.name}'
                self.stdout.write(
                    self.style.SUCCESS(
                        f'{cover_status} Zaimportowano: {track_title} - {artist_name} | '
                        f'{genre_status} {f"| {duration}" if duration else ""} {date_status}'
                    )
                )

            # Підсумок
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n Podsumowanie: zaimportowano {imported_count} utworów, '
                    f'pominięto {skipped_count} duplikatów'
                )
            )

        except Exception as e:
            raise CommandError(f'Błąd podczas pracy z MusicBrainz API: {str(e)}')
