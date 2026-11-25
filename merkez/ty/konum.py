"""KONUM KAPISI — SPY'nin şu anki konumu (atamada uzaklık ve Saha Canlı haritası için).

Öncelik sırası:
  0. Elle taşınan konum: yönetici takip sayfasında SPY'yi sürükledi (veri["elleKonum"]; test sıfırlanınca ya da canlı konum gelince silinir).
  1. Canlı konum: SPY telefonundan ya da şirketin saha takip sisteminden gelen son konum (CANLI_KONUM_DK dakikadan yeniyse).
     Giriş noktası: konum_yaz(spy_id, lat, lng) — merkezde POST api/konum {id, lat, lng}. Uygulama bunu henüz göndermiyor;
     canlı takip devreye alınınca uygulama ya da IT'nin sistemi bu adrese yazar.
  2. Bugünkü son randevusunun yeri (yolda / görüşmede / tamamlandı).
  3. Kayıtlı sabit konumu (veri/spyler.js: lat, lng).
Canlı konum yalnız bellekte tutulur (merkez yeniden başlayınca silinir).
"""
import threading

from .ayarlar import CANLI_KONUM_DK
from .yardim import bugun, simdi

_kilit = threading.Lock()
CANLI = {}  # spy id -> {"lat", "lng", "t"}


def konum_yaz(spy_id, lat, lng):
    if not isinstance(lat, (int, float)) or not isinstance(lng, (int, float)) or not (-90 <= lat <= 90 and -180 <= lng <= 180):
        raise ValueError("Konum geçersiz.")
    with _kilit:
        CANLI[spy_id] = {"lat": float(lat), "lng": float(lng), "t": simdi()}
    return CANLI[spy_id]


def konum_sifirla():
    """Test verisi sıfırlanınca SPY'ler kayıtlı sabit konumlarına döner."""
    with _kilit:
        CANLI.clear()


def canli_konum(spy_id):
    with _kilit:
        k = CANLI.get(spy_id)
    return k if k and simdi() - k["t"] <= CANLI_KONUM_DK * 60000 else None


def anlik_konum(veri, s):
    elle = (veri.get("elleKonum") or {}).get(s["id"])  # yönetici haritada sürükleyerek taşıdı: test sıfırlanana ya da canlı konum gelene kadar geçerli
    if elle:
        return {"lat": elle["lat"], "lng": elle["lng"]}
    k = canli_konum(s["id"])
    if k:
        return {"lat": k["lat"], "lng": k["lng"]}
    son = [x for x in veri["kayitlar"].values() if x.get("repId") == s["id"] and x.get("tarih") == bugun()
           and x.get("durum") in ("yolda", "gorusmede", "tamamlandi") and isinstance(x.get("konum"), dict) and "lat" in x["konum"]]
    if son:
        x = max(son, key=lambda y: y.get("guncelleme", 0))["konum"]
        return {"lat": x["lat"], "lng": x["lng"]}
    return {"lat": s["lat"], "lng": s["lng"]}
