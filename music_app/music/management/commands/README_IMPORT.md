# Імпорт треків з MusicBrainz

Цей документ описує, як використовувати команду `import_musicbrainz` для імпорту треків з бази даних MusicBrainz у вашу базу даних.

## Встановлення

Пакет `musicbrainzngs` вже встановлено. Якщо потрібно встановити його знову:

```bash
pip install musicbrainzngs
```

## Використання

### Базова команда

```bash
python manage.py import_musicbrainz --artist "Назва виконавця" --limit 10
```

### Параметри команди

- `--artist` - Пошук треків за ім'ям виконавця
- `--title` - Пошук треків за назвою треку
- `--limit` - Максимальна кількість треків для імпорту (за замовчуванням: 10)
- `--skip-duplicates` - Пропускати треки, які вже існують в базі даних
- `--default-genre` - Встановити жанр за замовчуванням для всіх імпортованих треків

## Приклади використання

### 1. Імпорт треків конкретного виконавця

```bash
python manage.py import_musicbrainz --artist "The Beatles" --limit 20
```

### 2. Пошук конкретного треку

```bash
python manage.py import_musicbrainz --title "Imagine" --artist "John Lennon"
```

### 3. Імпорт з пропуском дублікатів

```bash
python manage.py import_musicbrainz --artist "Pink Floyd" --limit 15 --skip-duplicates
```

### 4. Встановлення жанру за замовчуванням

```bash
python manage.py import_musicbrainz --artist "AC/DC" --limit 10 --default-genre "Rock"
```

### 5. Пошук тільки за назвою треку (усі виконавці)

```bash
python manage.py import_musicbrainz --title "Yesterday" --limit 5
```

### 6. Комбінований пошук

```bash
python manage.py import_musicbrainz --artist "Nirvana" --title "Smells Like Teen Spirit" --skip-duplicates
```

## Що імпортується?

Для кожного знайденого треку імпортуються наступні дані:

- **Назва треку** (title)
- **Виконавець** (artist) - автоматично створюється, якщо не існує
- **Тривалість** (duration) - якщо доступно в MusicBrainz
- **Жанр** (genre) - **ЗАВЖДИ є жанр**:
  1. Якщо вказано `--default-genre`, використовується він
  2. Якщо є теги в MusicBrainz, використовується перший тег
  3. Якщо немає жанру, автоматично встановлюється "Unknown"
- **Обкладинка** (cover_image) - URL зображення з Cover Art Archive (якщо доступно)
- **Дата випуску** (authored_date) - дата створення/випуску треку (якщо доступно)
- **Автор додавання** (created_by) - **всі треки додаються від імені адміністратора (ID=3)**
- **Опис** (description) - містить інформацію про джерело імпорту та MusicBrainz ID

## Робота з дублікатами

За замовчуванням команда імпортує всі знайдені треки, навіть якщо вони вже існують у базі даних.

Щоб уникнути дублікатів, використовуйте параметр `--skip-duplicates`:

```bash
python manage.py import_musicbrainz --artist "Queen" --skip-duplicates
```

Перевірка на дублікати відбувається за комбінацією **назва треку + виконавець**.

## Обмеження та рекомендації

1. **Rate Limiting**: MusicBrainz API має обмеження на кількість запитів. Рекомендується не робити занадто багато запитів підряд.

2. **Точність пошуку**: Результати залежать від якості даних у MusicBrainz. Можливі неточності в назвах виконавців або треків.

3. **Жанри**: Не всі треки в MusicBrainz мають теги жанрів. Рекомендується використовувати `--default-genre` для встановлення жанру за замовчуванням.

4. **Тривалість**: Тривалість треку може бути відсутня для деяких записів.

## Приклад повного робочого процесу

```bash
# 1. Імпорт треків The Beatles з жанром "Rock"
python manage.py import_musicbrainz --artist "The Beatles" --limit 20 --default-genre "Rock" --skip-duplicates

# 2. Імпорт класичного року
python manage.py import_musicbrainz --artist "Led Zeppelin" --limit 15 --default-genre "Classic Rock" --skip-duplicates

# 3. Імпорт українських виконавців
python manage.py import_musicbrainz --artist "Океан Эльзи" --limit 10 --default-genre "Rock" --skip-duplicates

# 4. Пошук популярних треків
python manage.py import_musicbrainz --title "Bohemian Rhapsody" --skip-duplicates
```

## Важливо: Вимоги до адміністратора

**Команда вимагає наявності користувача-адміністратора з ID=3 у базі даних.**

Перед використанням команди переконайтесь, що у вас є користувач з ID=3:

```bash
# Перевірка наявності адміністратора
python manage.py shell
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> User.objects.get(id=3)
```

Якщо користувач не існує, створіть його або використайте існуючого адміністратора, змінивши ID в коді команди.

## Усунення проблем

### Помилка: "Користувач admin (ID=3) не знайдено"

Створіть користувача-адміністратора або переконайтесь, що користувач з ID=3 існує у вашій базі даних.

```bash
python manage.py createsuperuser
```

### Помилка: "Пакет musicbrainzngs не встановлено"

```bash
pip install musicbrainzngs
```

### Помилка: "Потрібно вказати хоча б один параметр"

Обов'язково вкажіть хоча б один з параметрів: `--artist` або `--title`

### Помилка з'єднання з API

Перевірте інтернет-з'єднання. MusicBrainz API може бути тимчасово недоступним.

## Додаткова інформація

- [MusicBrainz](https://musicbrainz.org/) - офіційний сайт
- [MusicBrainz API документація](https://musicbrainz.org/doc/Development/XML_Web_Service/Version_2)
- [musicbrainzngs на PyPI](https://pypi.org/project/musicbrainzngs/)
