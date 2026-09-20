"""İlerleme özeti: görev ve kelime istatistikleri.

Bu dosya sadece sayıları hesaplar. Ekrana yazdırma main.py'da yapılır.
"""

from datetime import date, timedelta

from database import get_connection

# Bir kelime, art arda bu kadar doğru tekrar edilince "iyi öğrenilmiş" sayılır.
MASTERED_MIN_REVIEWS: int = 3


def get_task_progress() -> dict[str, int]:
    """Görev sayılarını döndürür: toplam, bugün ve son 7 gün."""
    today = date.today().isoformat()
    week_start = (date.today() - timedelta(days=6)).isoformat()

    with get_connection() as conn:
        total = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        completed = conn.execute(
            "SELECT COUNT(*) FROM tasks WHERE is_completed = 1"
        ).fetchone()[0]
        today_total = conn.execute(
            "SELECT COUNT(*) FROM tasks WHERE task_date = ?", (today,)
        ).fetchone()[0]
        today_completed = conn.execute(
            "SELECT COUNT(*) FROM tasks WHERE task_date = ? AND is_completed = 1",
            (today,),
        ).fetchone()[0]
        week_completed = conn.execute(
            """
            SELECT COUNT(*) FROM tasks
            WHERE is_completed = 1 AND substr(completed_at, 1, 10) >= ?
            """,
            (week_start,),
        ).fetchone()[0]

    return {
        "total": total,
        "completed": completed,
        "today_total": today_total,
        "today_completed": today_completed,
        "week_completed": week_completed,
    }


def get_vocabulary_progress() -> dict[str, int]:
    """Kelime sayılarını döndürür: toplam, bugün tekrar edilecek, iyi öğrenilen."""
    today = date.today().isoformat()

    with get_connection() as conn:
        total = conn.execute("SELECT COUNT(*) FROM vocabulary").fetchone()[0]
        due = conn.execute(
            "SELECT COUNT(*) FROM vocabulary WHERE next_review_date <= ?",
            (today,),
        ).fetchone()[0]
        mastered = conn.execute(
            "SELECT COUNT(*) FROM vocabulary WHERE times_reviewed >= ?",
            (MASTERED_MIN_REVIEWS,),
        ).fetchone()[0]

    return {"total": total, "due": due, "mastered": mastered}