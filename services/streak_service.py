"""Streak (üst üste çalışılan gün) hesapları.

Bir gün, o gün en az bir görev tamamlandıysa "çalışılmış" sayılır.
Ayrı bir tablo tutmuyoruz, tarihler tasks.completed_at'ten okunur.
"""

from datetime import date, timedelta

from database import get_connection


def _get_completed_days() -> set[date]:
    """En az bir görevin tamamlandığı günlerin kümesini döndürür."""
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT DISTINCT substr(completed_at, 1, 10) AS day
            FROM tasks
            WHERE is_completed = 1 AND completed_at IS NOT NULL
            """
        ).fetchall()
    return {date.fromisoformat(row["day"]) for row in rows}


def get_current_streak() -> int:
    """Şu anki üst üste çalışılan gün sayısını döndürür.

    Bugün henüz görev tamamlanmadıysa seri bozulmaz, dünden geriye sayılır.
    """
    days = _get_completed_days()
    today = date.today()

    current = today if today in days else today - timedelta(days=1)
    streak = 0
    while current in days:
        streak += 1
        current -= timedelta(days=1)
    return streak


def get_longest_streak() -> int:
    """Şimdiye kadarki en uzun seriyi döndürür."""
    days = sorted(_get_completed_days())

    longest = 0
    run = 0
    previous = None
    for day in days:
        if previous is not None and day - previous == timedelta(days=1):
            run += 1
        else:
            run = 1
        longest = max(longest, run)
        previous = day
    return longest


def get_total_study_days() -> int:
    """Toplam kaç farklı günde görev tamamlandığını döndürür."""
    return len(_get_completed_days())