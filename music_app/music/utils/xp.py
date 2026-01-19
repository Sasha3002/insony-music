from django.db import transaction
from django.db.models import F, Case, When, Value, IntegerField

@transaction.atomic
def add_xp(user, delta: int):
    if not user or not delta:
        return

    if delta < 0:
        user.__class__.objects.filter(pk=user.pk).update(
            xp=Case(
                When(xp__gte=abs(delta), then=F('xp') + delta),
                default=Value(0),
                output_field=IntegerField()
            )
        )
    else:
        user.__class__.objects.filter(pk=user.pk).update(xp=F("xp") + int(delta))

    user.refresh_from_db(fields=["xp"])

def level_from_xp(xp: int) -> int:
    return max(1, xp // 1000 + 1)

def level_progress(xp: int) -> tuple[int, int, int]:
    lvl = level_from_xp(xp)
    base = (lvl - 1) * 1000
    cur = xp - base
    to_next = 1000 - cur
    return lvl, cur, to_next

# BADGES 


BADGES = [
    {"slug": "bronze",   "name": "Bronze",   "min": 1,  "max": 4},
    {"slug": "silver",   "name": "Silver",   "min": 5,  "max": 9},
    {"slug": "gold",     "name": "Gold",     "min": 10, "max": 19},
    {"slug": "diamond",  "name": "Diamond",  "min": 20, "max": 9999},
]

def badge_for_level(level: int) -> dict:
    for b in BADGES:
        if b["min"] <= level <= b["max"]:
            return b
    return BADGES[0]

def badge_progress(level: int, level_xp: int) -> tuple[int, str, str]:
    b = badge_for_level(level)
    # how many levels are there in the badge
    total_levels = b["max"] - b["min"] + 1
    # how many levels have already been completed within the badge + the percentage of the current level
    passed_levels = (level - b["min"])
    progress_in_levels = passed_levels * 1000 + max(0, min(1000, level_xp))
    pct = int(round(progress_in_levels / (total_levels * 1000) * 100))

    # next badge
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
