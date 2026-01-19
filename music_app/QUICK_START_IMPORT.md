### 1. Import utworów wykonawcy
```bash
python music_app\manage.py import_musicbrainz --artist "Nazwa wykonawcy" --limit 10
```

### 2. Importuj z domyślnym gatunkiem
```bash
python music_app\manage.py import_musicbrainz --artist "Queen" --default-genre "Rock" --limit 15 --skip-duplicates
```

### 3. Wyszukiwanie konkretnego utworu
```bash
python music_app\manage.py import_musicbrainz --title "Yesterday" --artist "The Beatles" --skip-duplicates
```

## Parametry

- `--artist` - nazwa wykonawcy
- `--title` - nazwa utworu
- `--limit` - liczba utworów (default: 10)
- `--skip-duplicates` - nie importować duplikatów
- `--default-genre` - ustawić gatunek dla wszystkich utworów

## Przykłady dla popularnych wykonawców

```bash

python music_app\manage.py import_musicbrainz --artist "The Beatles" --limit 20 --default-genre "Rock" --skip-duplicates
python music_app\manage.py import_musicbrainz --artist "Pink Floyd" --limit 15 --default-genre "Progressive Rock" --skip-duplicates
python music_app\manage.py import_musicbrainz --artist "Eminem" --limit 20 --default-genre "Hip-Hop" --skip-duplicates
python music_app\manage.py import_musicbrainz --artist "Metallica" --limit 20 --default-genre "Metal" --skip-duplicates
```
