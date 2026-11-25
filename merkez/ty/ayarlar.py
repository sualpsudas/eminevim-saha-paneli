"""Merkezin bütün ayarları tek yerde: dosya yolları, port, atama kuralları, hesap güvenliği sabitleri.

Ortam değişkenleri (deneme kopyası için): TY_PORT (8794), TY_YOL (gizli yol yerine), TY_VERI (veri dosyası).
H/G ve randevu hedefi gibi iş kuralları veri/ayarlar.json'dadır (SPY listesi üretilirken kullanılır).
"""
import os
from pathlib import Path

KLASOR = Path(__file__).resolve().parent.parent          # merkez/
KOK = KLASOR.parent                                       # depo kökü
PORT = int(os.environ.get("TY_PORT", "8794"))
VERI = Path(os.environ.get("TY_VERI") or KLASOR / "veri.json")  # deneme kopyası ayrı dosya kullanır
PID = KLASOR / ("sunucu.pid" if PORT == 8794 else f"sunucu_{PORT}.pid")
ANAHTAR = KLASOR / "gizli_yol.txt"
YEDEK = KLASOR / "yedek"
AKTARIM = Path(os.environ.get("TY_AKTARIM") or KLASOR / "aktarim")  # şirket sistemine gidecek kayıtlar (aktarim.py)
UYGULAMA = "Eminevim Saha Paneli.dc.html"
SPY_DOSYASI = KOK / "veri" / "spyler.js"

# Bildirim (Web Push): telefon başına abonelik. Anahtar yalnız sunucuda (depoda yok).
ABONELIK = VERI.with_name(VERI.stem + "_abonelik.json")
VAPID = KLASOR / "vapid.pem"
APNS_P8 = KLASOR / "apns.p8"     # iPhone uygulaması bildirimi (apns.py); yalnız sunucuda
APNS_AYAR = KLASOR / "apns.json"  # {"key_id", "team_id", "topic"}
VAPID_SUB = "mailto:sualpsudas@users.noreply.github.com"  # bildirim servislerine iletişim (depodaki açık git kimliği)
BILDIRIM_TTL = 120      # telefon kapalı/çevrimdışıysa bildirim bu süre bekler (teklif süresi kadar)

# Atama kuralları (rapor/tasarruf-yanimda-proje-calismasi/10-atama-ve-rota.md)
KABUL_SN = 120          # SPY bu sürede kabul etmezse çağrı sıradakine geçer (sınır yok; herkes reddederse "kimse almadı")
HEMEN_DK = 120          # bugün ve saati en geç 2 saat sonra olan çağrı "hemen" sayılır (en erken seçilebilen saatler)
# Atama seçenekleri: varsayılanlar burada; takip sayfasındaki "Atama seçenekleri" bölümü değiştirir (veri["atamaAyar"], test sıfırlanınca korunur)
ATAMA_VARSAYILAN = {
    "agirlik": {"yakinlik": 40, "yuk": 30, "ciro": 20, "randevu": 10},  # öncelik: yakınlık, çağrı sayısı, ciro H/G, randevu H/G (2026-11-25)
    "uzaklik": "trafikli",  # trafikli: yol süresi × İBB tipik trafik çarpanı (dk) · yol: trafiksiz yol süresi (dk) · yolkm: yol km · kus: kuş uçuşu km
    "sifirDk": 30,          # süreyle ölçülürken bu varış süresinde yakınlık puanı sıfır
    "sifirKm": 10,          # km ile ölçülürken bu uzaklıkta yakınlık puanı sıfır
    "gunlukSinir": 4,       # bir SPY'ye bir günde en fazla çağrı
    "aralikDk": 60,         # aynı gün iki randevu arası en az (hemen ve ileri çağrıda)
    "ilceSarti": True,      # yalnız müşterinin ilçesindeki SPY aday olur
}
UZAKLIK_TURLERI = {"trafikli": "Trafikli varış süresi", "yol": "Yol süresi (trafiksiz)", "yolkm": "Yol mesafesi (km)", "kus": "Kuş uçuşu (km)"}
HG_TAVAN = 30           # H/G puanı %100'ün üstündeki ilk 30 puanda artar (%130 ve üstü tam puan)

# Canlı konum (konum.py): SPY telefonundan gelen konum bu süre taze sayılır; eskiyse kayıtlı konum kullanılır
CANLI_KONUM_DK = 10

KAPALI_DURUMLAR = {"tamamlandi", "iptal"}
DURUM_AD = {"alindi": "yeni çağrı", "atandi": "SPY kabul etti", "netlesti": "müşteri saati onayladı", "yolda": "SPY yola çıktı",
            "gorusme": "SPY yolda", "gorusmede": "kapıda doğrulandı, görüşmede", "tamamlandi": "görüşme tamamlandı", "iptal": "iptal edildi"}

# Müşteri hesabı (parola yok): telefon + SMS kodu
HATA_SINIR = 5   # aynı koda art arda 5 yanlış deneme → kod geçersiz, yenisi istenir
KOD_DK = 10      # SMS kodu (test: ekranda gösterilir) 10 dk geçerli

# Sunulan dosyalar (depo kökünden). Klasörlerin içindeki her dosya, yalnız aşağıdaki uzantılarla.
STATIK_UZANTI = {".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".css": "text/css; charset=utf-8",
                 ".json": "application/json; charset=utf-8", ".png": "image/png", ".jpg": "image/jpeg", ".svg": "image/svg+xml",
                 ".webp": "image/webp", ".ico": "image/x-icon", ".ttf": "font/ttf", ".mp4": "video/mp4"}
STATIK_KOK = {UYGULAMA, "index.html", "manifest.json", "eminevim-qr.png", "veri/spyler.js", "veri/sim-yollar.js", "veri/org-data.js", "web-basvuru/index.html"}
STATIK_KLASOR = ("assets/", "vendor/", "web-basvuru/", "uygulama/", "harita/")
# Bunlar değişince açık uygulamalar "Yeni sürüm hazır · Yenile" şeridi gösterir
SURUM_DOSYALARI = (UYGULAMA, "veri/spyler.js", "uygulama/canli.js", "uygulama/appointment.js", "uygulama/ayarlar.js",
                   "uygulama/bicim.js", "uygulama/finansman.js", "uygulama/personel.js", "uygulama/hesap.js", "uygulama/aydinlatma.js", "uygulama/ornek-veri.js")
