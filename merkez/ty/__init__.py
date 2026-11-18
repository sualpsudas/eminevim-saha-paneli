"""Tasarruf Yanımda merkezi — parçalar (her dış sistem tek dosyanın arkasında; IT_DEVIR.md):

  ayarlar.py   yollar, port, atama kuralları, sabitler
  yardim.py    küçük ortak yardımcılar (zaman, metin, uzaklık, olay kaydı)
  personel.py  PERSONEL KAPISI  — SPY listesi (veri/spyler.js; araclar/veri_hazirla.py üretir)
  depo.py      DEPO KAPISI      — çağrılar, mesajlar, SPY durumları, müşteri hesapları (şu an merkez/veri.json)
  konum.py     KONUM KAPISI     — SPY'nin anlık konumu (canlı takip girişi: api/konum)
  atama.py     ATAMA KAPISI     — çağrıyı hangi SPY alır
  bildirim.py  BİLDİRİM KAPISI  — telefon bildirimi (Web Push; ileride APNs/SMS)
  musteri.py   MÜŞTERİ HESABI KAPISI — telefon + parola, SMS kodu, oturum
  aktarim.py   AKTARIM KAPISI   — çağrıları şirketin randevu / müşteri kartı biçiminde dışarı verir
  islemler.py  istekleri işleyen kurallar (api/cagri, api/kayit, ...)
  api.py       HTTP sunucusu (adresler, dosya sunma, başlat/durdur)
"""
