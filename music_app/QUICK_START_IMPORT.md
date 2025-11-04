# Швидкий старт: Імпорт треків з MusicBrainz

## Основні команди

### 1. Імпорт треків виконавця
```bash
python music_app\manage.py import_musicbrainz --artist "Назва виконавця" --limit 10
```

### 2. Імпорт з жанром за замовчуванням
```bash
python music_app\manage.py import_musicbrainz --artist "Queen" --default-genre "Rock" --limit 15 --skip-duplicates
```

### 3. Пошук конкретного треку
```bash
python music_app\manage.py import_musicbrainz --title "Yesterday" --artist "The Beatles" --skip-duplicates
```

## Параметри

- `--artist` - ім'я виконавця
- `--title` - назва треку
- `--limit` - кількість треків (default: 10)
- `--skip-duplicates` - не імпортувати дублікати
- `--default-genre` - встановити жанр для всіх треків

## Приклади для популярних виконавців

```bash
# Українські виконавці
python music_app\manage.py import_musicbrainz --artist "Океан Ельзи" --limit 20 --default-genre "Rock" --skip-duplicates
python music_app\manage.py import_musicbrainz --artist "ТНМК" --limit 15 --default-genre "Hip-Hop" --skip-duplicates

# Світові виконавці
python music_app\manage.py import_musicbrainz --artist "The Beatles" --limit 20 --default-genre "Rock" --skip-duplicates
python music_app\manage.py import_musicbrainz --artist "Pink Floyd" --limit 15 --default-genre "Progressive Rock" --skip-duplicates
python music_app\manage.py import_musicbrainz --artist "Eminem" --limit 20 --default-genre "Hip-Hop" --skip-duplicates
python music_app\manage.py import_musicbrainz --artist "Metallica" --limit 20 --default-genre "Metal" --skip-duplicates
```

## Що було створено

✅ **Management команда**: `music_app/music/management/commands/import_musicbrainz.py`
✅ **Пакет встановлено**: `musicbrainzngs`
✅ **Документація**: `music_app/music/management/commands/README_IMPORT.md`
✅ **Тестування**: Успішно імпортовано 5 треків The Beatles

## Перевірка імпортованих треків

```bash
# Через Django shell
python music_app\manage.py shell -c "from music.models import Track; print(f'Total tracks: {Track.objects.count()}')"
```

## Додаткова інформація

Детальну документацію дивіться у файлі:
`music_app/music/management/commands/README_IMPORT.md`
