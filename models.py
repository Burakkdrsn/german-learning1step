"""Uygulamada ortak kullanılan sabit tanımlar.

Seviyeler, kategoriler ve zorluk dereceleri burada Enum olarak tutulur.
Böylece kodun her yerinde "b1" veya "B1 " gibi yazım hataları yapmayız.

NOT: Her seviyenin grammar konuları, kelime hedefleri gibi ayrıntılar
buraya YAZILMAYACAK. Onları PHASE 2'de veritabanına koyacağız ki
sonradan yönetilebilsin.
"""

from enum import Enum


class Level(Enum):
    """Almanca dil seviyeleri (kolaydan zora doğru sıralı)."""

    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"


class TaskCategory(Enum):
    """Görev kategorileri."""

    HOEREN = "HÖREN"
    LESEN = "LESEN"
    SCHREIBEN = "SCHREIBEN"
    SPRECHEN = "SPRECHEN"
    GRAMMATIK = "GRAMMATIK"
    VOKABELN = "VOKABELN"
    WIEDERHOLUNG = "WIEDERHOLUNG"


class Difficulty(Enum):
    """Görev zorluk dereceleri."""

    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"