"""SQLite veritabanı bağlantısı ve tablo oluşturma.

Bu dosya sadece bağlantıyı ve tabloları yönetir. Asıl işler
(görev ekleme, kelime listeleme vb.) services/ klasöründe yapılır.
"""

import sqlite3
from contextlib import contextmanager
from enum import Enum
from typing import Iterator

import config
from models import Difficulty, Level, TaskCategory


def _sql_list(enum_class: type[Enum]) -> str:
    """Enum değerlerini SQL CHECK için "'A1', 'A2', ..." metnine çevirir."""
    return ", ".join(f"'{item.value}'" for item in enum_class)


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    """Veritabanı bağlantısı açar; hata yoksa kaydeder, varsa geri alır.

    Kullanım:
        with get_connection() as conn:
            conn.execute("SELECT ...")
    """
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # sütunlara isimle erişebilmek için
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    """Tablolar yoksa oluşturur. Her açılışta çağrılabilir, veri silmez."""
    levels = _sql_list(Level)
    categories = _sql_list(TaskCategory)
    difficulties = _sql_list(Difficulty)

    with get_connection() as conn:
        conn.execute(
            f"""
            CREATE TABLE IF NOT EXISTS tasks (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                title        TEXT NOT NULL,
                category     TEXT NOT NULL CHECK (category IN ({categories})),
                level        TEXT NOT NULL CHECK (level IN ({levels})),
                difficulty   TEXT NOT NULL CHECK (difficulty IN ({difficulties})),
                task_date    TEXT NOT NULL,            -- YYYY-MM-DD
                is_completed INTEGER NOT NULL DEFAULT 0,
                created_at   TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                completed_at TEXT
            )
            """
        )

        conn.execute(
            f"""
            CREATE TABLE IF NOT EXISTS vocabulary (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                german           TEXT NOT NULL,
                turkish          TEXT NOT NULL,
                level            TEXT NOT NULL CHECK (level IN ({levels})),
                example          TEXT,
                times_reviewed   INTEGER NOT NULL DEFAULT 0,
                next_review_date TEXT,                 -- YYYY-MM-DD
                created_at       TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (german, level)
            )
            """
        )



        

        conn.execute(
            f"""
            CREATE TABLE IF NOT EXISTS grammar_topics (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                level        TEXT NOT NULL CHECK (level IN ({levels})),
                title        TEXT NOT NULL,
                is_completed INTEGER NOT NULL DEFAULT 0,
                completed_at TEXT,
                UNIQUE (level, title)
            )
            """
        )




        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS review_log (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                word_id     INTEGER NOT NULL REFERENCES vocabulary (id),
                review_date TEXT NOT NULL,
                reviewed_at TEXT NOT NULL,
                remembered  INTEGER NOT NULL
            )
            """
        )



        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS settings (
                key   TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
            """
        )