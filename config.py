"""Uygulamanın sabit ayarları.

Değişmeyen değerleri (dosya yolları, başlıklar vb.) tek bir yerde
topluyoruz. Böylece kodun içinde "sihirli sayılar" dolaşmaz.
"""

from pathlib import Path

# Bu dosyanın bulunduğu klasör = projenin ana klasörü
BASE_DIR: Path = Path(__file__).resolve().parent

# Veritabanı dosyasının konumu (PHASE 2'de kullanacağız)
DATA_DIR: Path = BASE_DIR / "data"
DATABASE_PATH: Path = DATA_DIR / "german_learning.db"

# Terminal görünümü
APP_TITLE: str = "GERMAN LEARNING TRACKER"
MENU_WIDTH: int = 36