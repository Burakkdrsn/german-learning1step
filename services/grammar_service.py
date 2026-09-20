"""Gramer konusu işlemleri: ekleme, listeleme, tamamlama, seviye özeti.

Bu dosya sadece veritabanı işini yapar. Kullanıcıdan bilgi alma ve
ekrana yazdırma işi main.py'da kalır.
"""

import sqlite3
from datetime import datetime
from typing import Optional

from database import get_connection
from models import Level


def add_topic(level: Level, title: str) -> Optional[int]:
    """Yeni gramer konusu ekler ve id'sini döndürür.

    Aynı konu aynı seviyede zaten varsa None döner.
    """
    try:
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO grammar_topics (level, title) VALUES (?, ?)",
                (level.value, title),
            )
            return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None


def get_topics(level: Optional[Level] = None) -> list[sqlite3.Row]:
    """Konuları döndürür. level verilirse sadece o seviyenin konuları gelir."""
    with get_connection() as conn:
        if level is None:
            cursor = conn.execute(
                "SELECT * FROM grammar_topics ORDER BY level, id"
            )
        else:
            cursor = conn.execute(
                "SELECT * FROM grammar_topics WHERE level = ? ORDER BY id",
                (level.value,),
            )
        return cursor.fetchall()


def complete_topic(topic_id: int) -> bool:
    """Konuyu tamamlandı olarak işaretler.

    Başarılıysa True döner. Konu yoksa ya da zaten tamamlanmışsa False.
    """
    completed_at = datetime.now().isoformat(timespec="seconds")

    with get_connection() as conn:
        cursor = conn.execute(
            """
            UPDATE grammar_topics
            SET is_completed = 1, completed_at = ?
            WHERE id = ? AND is_completed = 0
            """,
            (completed_at, topic_id),
        )
        return cursor.rowcount > 0


def get_level_summary() -> list[sqlite3.Row]:
    """Her seviye için toplam ve tamamlanan konu sayısını döndürür."""
    with get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT level,
                   COUNT(*) AS total,
                   SUM(is_completed) AS done
            FROM grammar_topics
            GROUP BY level
            ORDER BY level
            """
        )
        return cursor.fetchall()