# German Learning Tracker

Almanca öğrenme sürecini takip etmek için yazılmış terminal tabanlı bir uygulama.
Günlük görevler, kelime tekrarı, gramer konuları, ilerleme ve seri (streak) takibi
tek bir menüden yönetilir. Tüm veriler yerel bir SQLite dosyasında saklanır.

## Özellikler

| Menü             | Özellik                                                     |
| ---------------- | ----------------------------------------------------------- |
| 1. Today's Tasks | Bugünün görevlerini listeler                                |
| 2. Add Task      | Kategori, seviye ve zorluk seçerek görev ekler              |
| 3. Complete Task | Görevi tamamlandı olarak işaretler                          |
| 4. Vocabulary    | Kelime ekleme, listeleme ve aralıklı tekrar                 |
| 5. Grammar       | Seviyeye göre gramer konuları, tamamlama ve seviye özeti    |
| 6. Progress      | Günlük/haftalık görev sayısı ve kelime ilerlemesi           |
| 7. Statistics    | Kategori/seviye dağılımı, tekrar başarı oranı, en aktif gün |
| 8. Streak        | Şu anki ve en uzun üst üste çalışılan gün sayısı            |
| 9. Settings      | Günlük kelime tekrar limitini değiştirme                    |
| 10. Exit         | Çıkış                                                       |

### Kelime tekrarı (aralıklı tekrar)

Bir kelimeyi hatırladıkça bir sonraki tekrar aralığı uzar: 1, 3, 7, 14 ve 30 gün.
Hatırlanmayan kelime ertesi gün tekrar gelir. Günlük tekrar sayısı bir limitle
sınırlanır (varsayılan 20, Settings menüsünden değiştirilebilir). Yapılan her
tekrar `review_log` tablosuna kaydedilir.

### Streak

Bir gün, o gün en az bir görev tamamlandıysa **ya da** en az bir kelime tekrarı
yapıldıysa çalışılmış sayılır. Bugün henüz çalışmadıysan seri bozulmaz, dünden
geriye doğru sayılır.

## Kurulum ve çalıştırma

Gereksinimler: **Python 3.9 veya üstü**. Harici paket gerekmez, sadece Python'un
kendi kütüphaneleri kullanılır.

```bash
python3 main.py
```

İlk açılışta `data/german_learning.db` veritabanı ve tablolar kendiliğinden oluşur.

### Başlangıç verilerini yükleme (isteğe bağlı)

A1, A2 ve B1 seviyeleri için hazır kelime ve gramer listelerini yüklemek için:

```bash
python3 seed_vocabulary.py   # yaklaşık 190 kelime
python3 seed_grammar.py      # 44 gramer konusu
```

İki betik de birden fazla kez çalıştırılabilir, zaten kayıtlı olanlar atlanır.

## Proje yapısı

```
.
├── main.py                  # Terminal menüsü ve kullanıcı etkileşimi
├── config.py                # Sabit ayarlar (yollar, başlık, varsayılan limit)
├── database.py              # SQLite bağlantısı ve tablo oluşturma
├── models.py                # Ortak Enum'lar: Level, TaskCategory, Difficulty
├── seed_vocabulary.py       # Başlangıç kelimelerini yükler
├── seed_grammar.py          # Başlangıç gramer konularını yükler
├── data/                    # SQLite veritabanı dosyası burada oluşur
└── services/
    ├── task_service.py          # Görev ekleme, listeleme, tamamlama
    ├── vocabulary_service.py    # Kelime ekleme, listeleme, aralıklı tekrar
    ├── grammar_service.py       # Gramer konuları ve seviye özeti
    ├── review_service.py        # Kelime tekrar geçmişi (review_log)
    ├── progress_service.py      # Görev ve kelime ilerleme özeti
    ├── statistics_service.py    # İstatistik hesapları
    ├── streak_service.py        # Seri hesapları
    └── settings_service.py      # Kalıcı ayarlar
```

Tasarım kuralı: `main.py` sadece menüyü yönetir ve kullanıcıdan girdi alıp ekrana
yazdırır. Veritabanı işlerinin hepsi `services/` klasöründeki dosyalarda yapılır.

## Veritabanı tabloları

| Tablo            | Amaç                                                          |
| ---------------- | ------------------------------------------------------------- |
| `tasks`          | Günlük görevler (kategori, seviye, zorluk, tarih, tamamlanma) |
| `vocabulary`     | Kelimeler, tekrar sayısı ve bir sonraki tekrar tarihi         |
| `grammar_topics` | Seviyeye göre gramer konuları ve tamamlanma durumu            |
| `review_log`     | Yapılan her kelime tekrarının kaydı                           |
| `settings`       | Kalıcı ayarlar (ör. günlük tekrar limiti)                     |

Seviyeler (A1-C1), görev kategorileri ve zorluk dereceleri `models.py` içindeki
Enum'lardan gelir ve veritabanında CHECK kısıtı olarak da uygulanır.

## Geliştirme aşamaları

- **PHASE 1:** Menü iskeleti
- **PHASE 2:** SQLite veritabanı
- **PHASE 3:** Görev sistemi
- **PHASE 4-5:** Kelime sistemi, progress ve streak
- **PHASE 6:** Gramer sistemi
- **PHASE 7:** Tekrar geçmişi ve istatistikler
- **PHASE 8:** Ayarlar

## Fikirler ve eksikler

- Görev ve kelime silme/düzenleme
- Kelime arama
- Veritabanı yedekleme
- B2 ve C1 için kelime ve gramer listeleri
