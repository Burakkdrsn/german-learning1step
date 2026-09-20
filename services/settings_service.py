"""Kalıcı ayarlar: settings tablosundan okur, oraya yazar.

Bir ayar hiç kaydedilmemişse config.py'daki varsayılan değer kullanılır.
"""

from typing import Optional

import config
from database import get_connection

KEY_DAILY_REVIEW_LIMIT: str = "daily_review_limit"
MIN_REVIEW_LIMIT: int = 1
MAX_REVIEW_LIMIT: int = 200


def get_setting(key: str) -> Optional[str]:
    """Bir ayarın değerini döndürür, kayıtlı değilse None."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT value FROM settings WHERE key = ?", (key,)
        ).fetchone()
    return row["value"] if row else None


def set_setting(key: str, value: str) -> None:
    """Bir ayarı kaydeder (varsa üzerine yazar)."""
    with get_connection() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
            (key, value),
        )


def get_daily_review_limit() -> int:
    """Günlük kelime tekrar limitini döndürür."""
    value = get_setting(KEY_DAILY_REVIEW_LIMIT)
    if value is not None and value.isdigit():
        return int(value)
    return config.DAILY_REVIEW_LIMIT


def set_daily_review_limit(limit: int) -> bool:
    """Günlük limiti kaydeder. Değer aralık dışındaysa False döner."""
    if not MIN_REVIEW_LIMIT <= limit <= MAX_REVIEW_LIMIT:
        return False
    set_setting(KEY_DAILY_REVIEW_LIMIT, str(limit))
    return True