"""İstatistik hesapları: görev dağılımı, kelime tekrar başarısı, en aktif gün.

Bu dosya sadece sayıları hesaplar. Ekrana yazdırma main.py'da yapılır.
"""

import sqlite3
from typing import Optional

from database import get_connection


def get_task_stats_by_category() -> list[sqlite3.Row]:
    """Her kategori için toplam ve tamamlanan görev sayısını döndürür."""
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT category,
                   COUNT(*) AS total,
                   SUM(is_completed) AS done
            FROM tasks
            GROUP BY category
            ORDER BY category
            """
        ).fetchall()


def get_task_stats_by_level() -> list[sqlite3.Row]:
    """Her seviye için toplam ve tamamlanan görev sayısını döndürür."""
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT level,
                   COUNT(*) AS total,
                   SUM(is_completed) AS done
            FROM tasks
            GROUP BY level
            ORDER BY level
            """
        ).fetchall()


def get_review_stats() -> dict[str, int]:
    """Kelime tekrarlarının toplamını, doğru sayısını ve yüzdesini döndürür."""
    with get_connection() as conn:
        total = conn.execute("SELECT COUNT(*) FROM review_log").fetchone()[0]
        remembered = conn.execute(
            "SELECT COUNT(*) FROM review_log WHERE remembered = 1"
        ).fetchone()[0]

    percent = round(remembered * 100 / total) if total else 0
    return {"total": total, "remembered": remembered, "percent": percent}


def get_most_active_day() -> Optional[tuple[str, int]]:
    """En çok çalışma yapılan günü ve çalışma sayısını döndürür.

    Çalışma sayısı = o gün tamamlanan görevler + yapılan kelime tekrarları.
    Hiç kayıt yoksa None döner.
    """
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT day, SUM(n) AS total
            FROM (
                SELECT substr(completed_at, 1, 10) AS day, COUNT(*) AS n
                FROM tasks
                WHERE is_completed = 1 AND completed_at IS NOT NULL
                GROUP BY day
                UNION ALL
                SELECT review_date AS day, COUNT(*) AS n
                FROM review_log
                GROUP BY review_date
            )
            GROUP BY day
            ORDER BY total DESC, day DESC
            LIMIT 1
            """
        ).fetchone()

    if row is None:
        return None
    return row["day"], row["total"]