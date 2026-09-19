"""Görev (Todo) işlemleri: ekleme, listeleme, tamamlama.

Bu dosya sadece veritabanı işini yapar. Kullanıcıdan bilgi alma ve
ekrana yazdırma işi main.py'da kalır.
"""

import sqlite3
from datetime import date, datetime
from typing import Optional

from database import get_connection
from models import Difficulty, Level, TaskCategory


def add_task(
    title: str,
    category: TaskCategory,
    level: Level,
    difficulty: Difficulty,
    task_date: Optional[str] = None,
) -> int:
    """Yeni görev ekler ve görevin id'sini döndürür.

    task_date verilmezse bugünün tarihi (YYYY-MM-DD) kullanılır.
    """
    if task_date is None:
        task_date = date.today().isoformat()

    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO tasks (title, category, level, difficulty, task_date)
            VALUES (?, ?, ?, ?, ?)
            """,
            (title, category.value, level.value, difficulty.value, task_date),
        )
        return cursor.lastrowid


def get_tasks_by_date(task_date: Optional[str] = None) -> list[sqlite3.Row]:
    """Verilen günün görevlerini döndürür (varsayılan: bugün)."""
    if task_date is None:
        task_date = date.today().isoformat()

    with get_connection() as conn:
        cursor = conn.execute(
            "SELECT * FROM tasks WHERE task_date = ? ORDER BY id",
            (task_date,),
        )
        return cursor.fetchall()


def complete_task(task_id: int) -> bool:
    """Görevi tamamlandı olarak işaretler.

    Başarılıysa True döner. Görev yoksa ya da zaten tamamlanmışsa False.
    """
    completed_at = datetime.now().isoformat(timespec="seconds")

    with get_connection() as conn:
        cursor = conn.execute(
            """
            UPDATE tasks
            SET is_completed = 1, completed_at = ?
            WHERE id = ? AND is_completed = 0
            """,
            (completed_at, task_id),
        )
        return cursor.rowcount > 0