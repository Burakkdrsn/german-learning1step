"""German Learning Tracker - programın giriş noktası.

Bu dosya sadece terminal menüsünü yönetir. Asıl işleri
services/ klasöründeki dosyalar yapacak.
"""

from typing import Callable

import config

# Bir menü seçeneği seçilince çalışacak fonksiyonun türü:
# argüman almayan ve hiçbir şey döndürmeyen fonksiyon
MenuAction = Callable[[], None]

EXIT_CHOICE: str = "10"


def show_coming_soon(feature_name: str, phase_number: int) -> None:
    """Henüz yazılmamış bir özellik için bilgi mesajı gösterir."""
    print(f"\n'{feature_name}' henüz hazır değil (PHASE {phase_number}'te eklenecek).")


# --- Menü seçeneklerinin fonksiyonları ---
# Şimdilik hepsi yer tutucu. İlerleyen aşamalarda gerçek işleri yapacaklar.

def show_todays_tasks() -> None:
    show_coming_soon("Today's Tasks", 4)


def add_task() -> None:
    show_coming_soon("Add Task", 3)


def complete_task() -> None:
    show_coming_soon("Complete Task", 3)


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
    main()