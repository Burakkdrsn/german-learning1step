"""German Learning Tracker - programın giriş noktası.

Bu dosya sadece terminal menüsünü yönetir. Asıl işleri
services/ klasöründeki dosyalar yapacak.
"""

from typing import Callable

import config
import database
from models import Difficulty, Level, TaskCategory
from services import (
    grammar_service,
    progress_service,
    streak_service,
    task_service,
    vocabulary_service,
)



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


def _add_word() -> None:
    german = input("\nAlmanca kelime: ").strip()
    turkish = input("Türkçe anlamı: ").strip()
    if not german or not turkish:
        print("Kelime ve anlamı boş olamaz.")
        return

    level = _choose(Level, "Seviye")
    if level is None:
        print("Geçersiz seçim, kelime eklenmedi.")
        return

    example = input("Örnek cümle (boş bırakabilirsin): ").strip() or None

    word_id = vocabulary_service.add_word(german, turkish, level, example)
    if word_id is None:
        print("\nBu kelime bu seviyede zaten kayıtlı.")
    else:
        print(f"\nKelime eklendi (id: {word_id}).")


def _list_words() -> None:
    words = vocabulary_service.get_all_words()
    if not words:
        print("\nHenüz kelime yok.")
        return

    print(f"\n--- Kelimeler ({len(words)}) ---")
    for word in words:
        print(f"[{word['level']}] {word['german']} = {word['turkish']}")


def _review_words() -> None:
    words = vocabulary_service.get_due_words()
    if not words:
        print("\nBugün tekrar edilecek kelime yok.")
        return

    print(f"\nBugün tekrar edilecek {len(words)} kelime var.")
    for word in words:
        print(f"\nAlmanca: {word['german']}")
        input("Anlamını düşün, göstermek için Enter'a bas...")
        print(f"Türkçe: {word['turkish']}")
        if word["example"]:
            print(f"Örnek: {word['example']}")

        answer = input("Hatırladın mı? (e/h, çıkmak için q): ").strip().lower()
        if answer == "q":
            break
        vocabulary_service.review_word(word["id"], answer == "e")

    print("\nTekrar bitti.")


def show_vocabulary() -> None:
    print("\n--- Kelimeler ---")
    print("1. Kelime ekle")
    print("2. Tüm kelimeleri listele")
    print("3. Bugünün tekrarı")
    print("0. Geri")

    choice = input("Seçim: ").strip()
    if choice == "1":
        _add_word()
    elif choice == "2":
        _list_words()
    elif choice == "3":
        _review_words()
    elif choice != "0":
        print("Geçersiz seçim.")

def _print_grammar_topics(level=None) -> None:
    topics = grammar_service.get_topics(level)
    if not topics:
        print("\nKonu bulunamadı.")
        return

    print("\n--- Gramer Konuları ---")
    current_level = None
    for topic in topics:
        if topic["level"] != current_level:
            current_level = topic["level"]
            print(f"\n[{current_level}]")
        mark = "x" if topic["is_completed"] else " "
        print(f"  [{mark}] {topic['id']}. {topic['title']}")

        
def _complete_grammar_topic() -> None:
    raw = input("\nTamamlanan konunun numarası: ").strip()
    if not raw.isdigit():
        print("Geçerli bir numara gir.")
        return

    if grammar_service.complete_topic(int(raw)):
        print("Konu tamamlandı.")
    else:
        print("Konu bulunamadı ya da zaten tamamlanmış.")


def _show_grammar_summary() -> None:
    rows = grammar_service.get_level_summary()
    if not rows:
        print("\nHenüz gramer konusu yok.")
        return

    print("\n--- Gramer Özeti ---")
    for row in rows:
        print(f"{row['level']}: {row['done']}/{row['total']} konu tamamlandı")


def show_grammar() -> None:

    print("\n--- Gramer ---")
    print("1. Tüm konuları listele")
    print("2. Bir seviyenin konularını listele")
    print("3. Konuyu tamamla")
    print("4. Seviye özeti")
    print("0. Geri")

    choice = input("Seçim: ").strip()
    if choice == "1":
        _print_grammar_topics()
    elif choice == "2":
        level = _choose(Level, "Seviye")
        if level is None:
            print("Geçersiz seçim.")
        else:
            _print_grammar_topics(level)
    elif choice == "3":
        _print_grammar_topics()
        _complete_grammar_topic()
    elif choice == "4":
        _show_grammar_summary()
    elif choice != "0":
        print("Geçersiz seçim.")


def show_progress() -> None:
    tasks = progress_service.get_task_progress()
    vocab = progress_service.get_vocabulary_progress()

    print("\n--- İlerleme ---")
    print(f"Bugün: {tasks['today_completed']}/{tasks['today_total']} görev tamamlandı")
    print(f"Son 7 gün: {tasks['week_completed']} görev tamamlandı")
    print(f"Toplam: {tasks['completed']}/{tasks['total']} görev")

    print(f"\nKelimeler: {vocab['total']} kayıtlı")
    print(f"Bugün tekrar edilecek: {vocab['due']}")
    print(f"İyi öğrenilmiş (3+ doğru tekrar): {vocab['mastered']}")



def show_statistics() -> None:
    show_coming_soon("Statistics", 8)


def show_streak() -> None:

    current = streak_service.get_current_streak()
    longest = streak_service.get_longest_streak()
    total_days = streak_service.get_total_study_days()

    print("\n--- Streak ---")
    print(f"Şu anki seri: {current} gün")
    print(f"En uzun seri: {longest} gün")
    print(f"Toplam çalışılan gün: {total_days}")


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