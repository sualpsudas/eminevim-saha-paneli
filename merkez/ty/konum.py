"""KONUM KAPISI — SPY'nin şu anki konumu (atamada uzaklık ve Saha Canlı haritası için).

Öncelik sırası:
  0. Elle taşınan konum: yönetici takip sayfasında SPY'yi sürükledi (veri["elleKonum"]; test sıfırlanınca ya da canlı konum gelince silinir).
  1. Canlı konum: SPY telefonundan ya da şirketin saha takip sisteminden gelen son konum (CANLI_KONUM_DK dakikadan yeniyse).
     Giriş noktası: konum_yaz(spy_id, lat, lng) — merkezde POST api/konum {id, lat, lng}. Uygulama bunu henüz göndermiyor;
     canlı takip devreye alınınca uygulama ya da IT'nin sistemi bu adrese yazar.
  2. Bugünkü son randevusunun yeri (görüşmede / tamamlandı; yolda iken SPY henüz varmadı, eski yerinde kalır ki rota çizilsin).
  3. Hareketli örnek SPY: ilçesinde dolaşma (gezi_konum); diğerleri kayıtlı sabit konumu (veri/spyler.js: lat, lng).
Canlı konum yalnız bellekte tutulur (merkez yeniden başlayınca silinir).
"""
import json
import math
import threading

from .ayarlar import CANLI_KONUM_DK, KOK
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


_YOLLAR = None


def _yollar():
    """veri/sim-yollar.js (araclar/sim_yol_uret.py üretir): her hareketli SPY için yol üstünde kapalı tur; metre cinsinden birikimli uzunluklarla."""
    global _YOLLAR
    if _YOLLAR is None:
        _YOLLAR = {}
        try:
            ham = (KOK / "veri" / "sim-yollar.js").read_text(encoding="utf-8")
            for i, nk in json.loads(ham[ham.index("{"):ham.rindex("}") + 1]).items():
                cum = [0.0]
                for a, b in zip(nk, nk[1:]):
                    cum.append(cum[-1] + math.hypot((b[0] - a[0]) * 111320, (b[1] - a[1]) * 111320 * math.cos(math.radians(a[0]))))
                _YOLLAR[i] = (nk, cum)
        except (OSError, ValueError):
            pass
    return _YOLLAR


def gezi_konum(s, t_ms=None):
    """Hareketli örnek SPY'nin zamana bağlı konumu: yol üstündeki kapalı turda hiz (m/sn) ile ilerler, faz turun başlangıç payı.
    Takip sayfası aynı formülü tarayıcıda hesaplar (akıcı hareket için). Yol dosyası yoksa tabanında durur."""
    yol = _yollar().get(s["id"])
    if not yol:
        return {"lat": s["lat"], "lng": s["lng"]}
    nk, cum = yol
    t = (t_ms if t_ms is not None else simdi()) / 1000
    d = (t * s["gezi"]["hiz"] + s["gezi"]["faz"] * cum[-1]) % cum[-1]
    lo, hi = 0, len(cum) - 1
    while hi - lo > 1:
        m = (lo + hi) // 2
        lo, hi = (m, hi) if cum[m] <= d else (lo, m)
    f = (d - cum[lo]) / ((cum[hi] - cum[lo]) or 1)
    return {"lat": nk[lo][0] + (nk[hi][0] - nk[lo][0]) * f, "lng": nk[lo][1] + (nk[hi][1] - nk[lo][1]) * f}


def konum_ve_kaynak(veri, s):
    """(konum, kaynak): kaynak yol | elle | canli | randevu | gezi | sabit."""
    for x in veri["kayitlar"].values():  # sunumda yola çıkmış: başlangıçtan müşteriye zamana göre ilerler
        if x.get("repId") == s["id"] and x.get("durum") in ("yolda", "gorusme") and x.get("yolBasladi") and x.get("yolBaslangic") and isinstance(x.get("konum"), dict):
            p = min(1.0, max(0.0, (simdi() - x["yolBasladi"]) / (x.get("yolSure") or 1)))
            a, b = x["yolBaslangic"], x["konum"]
            return {"lat": a["lat"] + (b["lat"] - a["lat"]) * p, "lng": a["lng"] + (b["lng"] - a["lng"]) * p}, "yol"
    elle = (veri.get("elleKonum") or {}).get(s["id"])  # yönetici haritada sürükleyerek taşıdı: test sıfırlanana ya da canlı konum gelene kadar geçerli
    if elle:
        return {"lat": elle["lat"], "lng": elle["lng"]}, "elle"
    k = canli_konum(s["id"])
    if k:
        return {"lat": k["lat"], "lng": k["lng"]}, "canli"
    son = [x for x in veri["kayitlar"].values() if x.get("repId") == s["id"] and x.get("tarih") == bugun()
           and x.get("durum") in ("gorusmede", "tamamlandi") and isinstance(x.get("konum"), dict) and "lat" in x["konum"]]
    if son:
        x = max(son, key=lambda y: y.get("guncelleme", 0))["konum"]
        return {"lat": x["lat"], "lng": x["lng"]}, "randevu"
    if s.get("gezi"):
        return gezi_konum(s), "gezi"
    return {"lat": s["lat"], "lng": s["lng"]}, "sabit"


def anlik_konum(veri, s):
    return konum_ve_kaynak(veri, s)[0]
