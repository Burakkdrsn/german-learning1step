"""German Learning Tracker - programın giriş noktası.

Bu dosya sadece terminal menüsünü yönetir. Asıl işleri
services/ klasöründeki dosyalar yapacak.
"""

from typing import Callable

import config
import database
from models import Difficulty, Level, TaskCategory
from services import task_service


# Bir menü seçeneği seçilince çalışacak fonksiyonun türü:
# argüman almayan ve hiçbir şey döndürmeyen fonksiyon
MenuAction = Callable[[], None]

EXIT_CHOICE: str = "10"


def show_coming_soon(feature_name: str, phase_number: int) -> None:
    """Henüz yazılmamış bir özellik için bilgi mesajı gösterir."""
    print(f"\n'{feature_name}' henüz hazır değil (PHASE {phase_number}'te eklenecek).")


# --- Menü seçeneklerinin fonksiyonları ---
# Şimdilik hepsi yer tutucu. İlerleyen aşamalarda gerçek işleri yapacaklar.

def _choose(enum_class, label: str):
    """Kullanıcıya numaralı liste gösterir, seçilen enum değerini döndürür."""
    items = list(enum_class)
    print(f"\n{label}:")
    for number, item in enumerate(items, start=1):
        print(f"  {number}. {item.value}")

    raw = input("Seçim (numara): ").strip()
    if raw.isdigit() and 1 <= int(raw) <= len(items):
        return items[int(raw) - 1]
    return None


def show_todays_tasks() -> None:
    tasks = task_service.get_tasks_by_date()
    if not tasks:
        print("\nBugün için görev yok.")
        return

    print("\n--- Bugünün Görevleri ---")
    for task in tasks:
        mark = "x" if task["is_completed"] else " "
        print(
            f"[{mark}] {task['id']}. {task['title']} "
            f"({task['category']}, {task['level']}, {task['difficulty']})"
        )


def add_task() -> None:
    title = input("\nGörev başlığı: ").strip()
    if not title:
        print("Başlık boş olamaz.")
        return

    category = _choose(TaskCategory, "Kategori")
    level = _choose(Level, "Seviye")
    difficulty = _choose(Difficulty, "Zorluk")

    if category is None or level is None or difficulty is None:
        print("Geçersiz seçim, görev eklenmedi.")
        return

    task_id = task_service.add_task(title, category, level, difficulty)
    print(f"\nGörev eklendi (id: {task_id}).")


def complete_task() -> None:
    show_todays_tasks()

    raw = input("\nTamamlanan görevin numarası: ").strip()
    if not raw.isdigit():
        print("Geçerli bir numara gir.")
        return

    if task_service.complete_task(int(raw)):
        print("Görev tamamlandı.")
    else:
        print("Görev bulunamadı ya da zaten tamamlanmış.")

        
def show_vocabulary() -> None:
    show_coming_soon("Vocabulary", 5)


def show_grammar() -> None:
    show_coming_soon("Grammar", 6)


def show_progress() -> None:
    show_coming_soon("Progress", 7)


def show_statistics() -> None:
    show_coming_soon("Statistics", 8)


def show_streak() -> None:
    show_coming_soon("Streak", 9)


def show_settings() -> None:
    show_coming_soon("Settings", 2)


# Menü tablosu: seçim numarası -> (görünen isim, çalışacak fonksiyon)
MENU_ITEMS: dict[str, tuple[str, MenuAction]] = {
    "1": ("Today's Tasks", show_todays_tasks),
    "2": ("Add Task", add_task),
    "3": ("Complete Task", complete_task),
    "4": ("Vocabulary", show_vocabulary),
    "5": ("Grammar", show_grammar),
    "6": ("Progress", show_progress),
    "7": ("Statistics", show_statistics),
    "8": ("Streak", show_streak),
    "9": ("Settings", show_settings),
}


def print_menu() -> None:
    """Ana menüyü ekrana yazdırır."""
    line = "=" * config.MENU_WIDTH
    print()
    print(line)
    print(config.APP_TITLE)
    print(line)
    print()
    for choice, (label, _action) in MENU_ITEMS.items():
        print(f"{choice}. {label}")
    print(f"{EXIT_CHOICE}. Exit")
    print()


def run_menu() -> None:
    """Menü döngüsü: kullanıcı çıkana kadar seçim ister."""
    while True:
        print_menu()
        choice = input("Seçiminiz: ").strip()

        if choice == EXIT_CHOICE:
            print("\nAuf Wiedersehen! Bis morgen! 👋")
            break

        menu_item = MENU_ITEMS.get(choice)
        if menu_item is None:
            print("\nGeçersiz seçim. Lütfen 1-10 arasında bir sayı girin.")
            continue

        _label, action = menu_item
        action()


def main() -> None:
    """Programı başlatır ve beklenmeyen çıkışları düzgün karşılar."""
    try:
        run_menu()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C veya Ctrl+D ile çıkılırsa hata yığını yerine nazik mesaj
        print("\n\nProgram kapatıldı. Tschüss!")


if __name__ == "__main__":
    database.init_db()
    main()