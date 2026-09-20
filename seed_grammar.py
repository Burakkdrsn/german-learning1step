"""A1, A2 ve B1 seviyeleri için gramer konularını toplu ekler.

Kullanım (proje ana klasöründe):
    python3 seed_grammar.py

Birden fazla kez çalıştırmak güvenlidir: zaten kayıtlı konular atlanır.
"""

from database import init_db
from models import Level
from services import grammar_service

TOPICS: dict[Level, list[str]] = {
    Level.A1: [
        "Personalpronomen (kişi zamirleri)",
        "Verb sein und haben (olmak ve sahip olmak)",
        "Regelmäßige Verben im Präsens (düzenli fiil çekimi)",
        "Artikel: der, die, das (tanımlıklar)",
        "Negation: nicht und kein (olumsuzluk)",
        "W-Fragen (soru kelimeleri)",
        "Satzstellung: Verb an Position 2 (cümle sırası)",
        "Ja/Nein-Fragen (evet/hayır soruları)",
        "Nominativ und Akkusativ (yalın ve -i hali)",
        "Plural der Nomen (çoğul)",
        "Possessivartikel (iyelik sıfatları)",
        "Modalverben: können, müssen, wollen (kip fiilleri)",
        "Trennbare Verben (ayrılabilen fiiller)",
        "Imperativ (emir kipi)",
        "Zahlen und Uhrzeit (sayılar ve saat)",
    ],
    Level.A2: [
        "Perfekt (bitmiş geçmiş zaman)",
        "Präteritum von sein und haben",
        "Dativ (-e hali)",
        "Wechselpräpositionen (yer ve yön edatları)",
        "Reflexive Verben (dönüşlü fiiller)",
        "Nebensätze mit weil (çünkü)",
        "Nebensätze mit dass",
        "Nebensätze mit wenn (eğer, -diğinde)",
        "Komparativ und Superlativ (karşılaştırma)",
        "Adjektivdeklination Grundlagen (sıfat çekimi)",
        "Modalverben im Präteritum",
        "Konjunktiv II: höfliche Bitten (nazik rica)",
        "Futur I (gelecek zaman)",
        "Konnektoren: und, aber, oder, denn",
    ],
    Level.B1: [
        "Passiv Präsens (edilgen çatı)",
        "Passiv Perfekt und Präteritum",
        "Relativsätze (ilgi cümleleri)",
        "Konjunktiv II: irreale Wünsche und Bedingungen",
        "Präteritum regelmäßiger und unregelmäßiger Verben",
        "Plusquamperfekt (-miş idi)",
        "Nebensätze mit obwohl (-e rağmen)",
        "Nebensätze mit damit und um ... zu (amaç)",
        "Infinitiv mit zu",
        "Genitiv (-in hali)",
        "Verben mit Präpositionen (edatlı fiiller)",
        "Indirekte Fragen (dolaylı sorular)",
        "Konnektoren: deshalb, trotzdem, außerdem",
        "Adjektivdeklination vollständig",
        "je ... desto (ne kadar ... o kadar)",
    ],
}


def main() -> None:
    init_db()

    added = 0
    skipped = 0
    for level, titles in TOPICS.items():
        level_added = 0
        for title in titles:
            result = grammar_service.add_topic(level, title)
            if result is None:
                skipped += 1
            else:
                added += 1
                level_added += 1
        print(f"{level.value}: {level_added} yeni konu eklendi")

    print(f"\nToplam eklenen: {added}, zaten kayıtlı olduğu için atlanan: {skipped}")


if __name__ == "__main__":
    main()