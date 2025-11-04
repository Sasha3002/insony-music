# music/utils/xp.py
from django.db import transaction
from django.db.models import F

@transaction.atomic
def add_xp(user, delta: int):
    """
    Безпечно додає/знімає XP прямо в User.xp.
    delta може бути від’ємним. XP не опускаємо нижче 0.
    """
    if not user or not delta:
        return

    # 1) інкремент в БД (без читання поточного значення в пам'ять)
    user.__class__.objects.filter(pk=user.pk).update(xp=F("xp") + int(delta))

    # 2) підтягнути оновлене значення в об’єкт
    user.refresh_from_db(fields=["xp"])

    # 3) не даємо піти нижче нуля
    if user.xp < 0:
        user.__class__.objects.filter(pk=user.pk).update(xp=0)
        user.xp = 0

def level_from_xp(xp: int) -> int:
    return max(1, xp // 1000 + 1)

def level_progress(xp: int) -> tuple[int, int, int]:
    """(current_level, current_xp_in_level, xp_to_next_level)"""
    lvl = level_from_xp(xp)
    base = (lvl - 1) * 1000
    cur = xp - base
    to_next = 1000 - cur
    return lvl, cur, to_next

# --- BADGES ---------------------------------------------------------------

# межі включні: min_level..max_level
BADGES = [
    {"slug": "bronze",   "name": "Bronze",   "min": 1,  "max": 4},
    {"slug": "silver",   "name": "Silver",   "min": 5,  "max": 9},
    {"slug": "gold",     "name": "Gold",     "min": 10, "max": 19},
    {"slug": "diamond",  "name": "Diamond",  "min": 20, "max": 9999},
]

def badge_for_level(level: int) -> dict:
    """Повертає словник з даними бейджа для рівня."""
    for b in BADGES:
        if b["min"] <= level <= b["max"]:
            return b
    return BADGES[0]

def badge_progress(level: int, level_xp: int) -> tuple[int, str, str]:
    """
    Прогрес всередині поточного бейджа у %.
    level_xp — XP у поточному рівні (0..1000)
    -> (pct, current_badge_slug, next_badge_slug_or_None)
    """
    b = badge_for_level(level)
    # скільки рівнів у бейджі
    total_levels = b["max"] - b["min"] + 1
    # скільки рівнів уже пройдено в межах бейджа + частка поточного рівня
    passed_levels = (level - b["min"])
    progress_in_levels = passed_levels * 1000 + max(0, min(1000, level_xp))
    pct = int(round(progress_in_levels / (total_levels * 1000) * 100))

    # наступний бейдж
    next_badge = None
    for i, el in enumerate(BADGES):
        if el["slug"] == b["slug"] and i + 1 < len(BADGES):
            next_badge = BADGES[i + 1]["slug"]
            break

    return max(0, min(100, pct)), b["slug"], next_badge

def badge_name(slug: str) -> str:
    for b in BADGES:
        if b["slug"] == slug:
            return b["name"]
    return "Bronze"
