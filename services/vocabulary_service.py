"""Kelime (Vocabulary) işlemleri: ekleme, listeleme, aralıklı tekrar.

Bu dosya sadece veritabanı işini yapar. Kullanıcıdan bilgi alma ve
ekrana yazdırma işi main.py'da kalır.
"""

import sqlite3
from datetime import date, timedelta
from typing import Optional

from database import get_connection
from models import Level

# Kelimeyi art arda her hatırlayışta bir sonraki tekrar aralığı (gün).
# 1. doğru: 1 gün sonra, 2. doğru: 3 gün sonra, ... 5. ve sonrası: 30 gün.
REVIEW_INTERVALS_DAYS: list[int] = [1, 3, 7, 14, 30]


def add_word(
    german: str,
    turkish: str,
    level: Level,
    example: Optional[str] = None,
) -> Optional[int]:
    """Yeni kelime ekler ve id'sini döndürür.

    Aynı kelime aynı seviyede zaten varsa None döner.
    Yeni kelimenin ilk tekrar tarihi bugündür.
    """
    today = date.today().isoformat()

    try:
        with get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO vocabulary
                    (german, turkish, level, example, next_review_date)
                VALUES (?, ?, ?, ?, ?)
                """,
                (german, turkish, level.value, example, today),
            )
            return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None


def get_all_words() -> list[sqlite3.Row]:
    """Tüm kelimeleri seviye ve alfabetik sırayla döndürür."""
    with get_connection() as conn:
        cursor = conn.execute(
            "SELECT * FROM vocabulary ORDER BY level, german"
        )
        return cursor.fetchall()


def get_due_words(limit: Optional[int] = None) -> list[sqlite3.Row]:
    """Tekrar tarihi bugün ya da geçmiş olan kelimeleri döndürür.

    limit verilirse en fazla o kadar kelime gelir (en eski tarihliler önce).
    """
    today = date.today().isoformat()

    query = """
        SELECT * FROM vocabulary
        WHERE next_review_date <= ?
        ORDER BY next_review_date, id
    """
    params: tuple = (today,)
    if limit is not None:
        query += " LIMIT ?"
        params = (today, limit)

    with get_connection() as conn:
        return conn.execute(query, params).fetchall()


def count_due_words() -> int:
    """Tekrar tarihi bugün ya da geçmiş olan kelime sayısını döndürür."""
    today = date.today().isoformat()

    with get_connection() as conn:
        return conn.execute(
            "SELECT COUNT(*) FROM vocabulary WHERE next_review_date <= ?",
            (today,),
        ).fetchone()[0]


def review_word(word_id: int, remembered: bool) -> bool:
    """Bir tekrarın sonucunu kaydeder ve sonraki tekrar tarihini hesaplar.

    Hatırlandıysa aralık uzar, hatırlanmadıysa sayaç sıfırlanır ve
    kelime ertesi gün tekrar gelir. Kelime bulunamazsa False döner.
    """
    with get_connection() as conn:
        row = conn.execute(
            "SELECT times_reviewed FROM vocabulary WHERE id = ?",
            (word_id,),
        ).fetchone()

        if row is None:
            return False

        if remembered:
            times_reviewed = row["times_reviewed"] + 1
            index = min(times_reviewed, len(REVIEW_INTERVALS_DAYS)) - 1
            days = REVIEW_INTERVALS_DAYS[index]
        else:
            times_reviewed = 0
            days = 1

        next_date = (date.today() + timedelta(days=days)).isoformat()

        conn.execute(
            """
            UPDATE vocabulary
            SET times_reviewed = ?, next_review_date = ?
            WHERE id = ?
            """,
            (times_reviewed, next_date, word_id),
        )
        return True