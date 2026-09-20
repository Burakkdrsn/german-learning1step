"""Kelime tekrar geçmişi: her tekrar review_log tablosuna kaydedilir.

Bu kayıtlar iki iş için kullanılır:
- Günlük tekrar limitini gerçekten günlük yapmak
- Kelime çalışılan günleri streak'e (seriye) saymak
"""

from datetime import date, datetime

from database import get_connection


def log_review(word_id: int, remembered: bool) -> None:
    """Yapılan bir kelime tekrarını kaydeder."""
    now = datetime.now()

    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO review_log (word_id, review_date, reviewed_at, remembered)
            VALUES (?, ?, ?, ?)
            """,
            (
                word_id,
                now.date().isoformat(),
                now.isoformat(timespec="seconds"),
                int(remembered),
            ),
        )


def count_reviews_today() -> int:
    """Bugün yapılan toplam kelime tekrarı sayısını döndürür."""
    today = date.today().isoformat()

    with get_connection() as conn:
        return conn.execute(
            "SELECT COUNT(*) FROM review_log WHERE review_date = ?",
            (today,),
        ).fetchone()[0]


def get_review_days() -> set[date]:
    """En az bir kelime tekrarı yapılan günlerin kümesini döndürür."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT DISTINCT review_date FROM review_log"
        ).fetchall()
    return {date.fromisoformat(row["review_date"]) for row in rows}