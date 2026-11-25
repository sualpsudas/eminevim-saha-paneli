"""TRAFİK KAPISI — bir yolculuğun o gün ve saatteki tipik trafik çarpanı (atamada varış süresi = yol süresi × çarpan).

Şu an İBB Açık Veri "Saatlik Trafik Yoğunluk Veri Seti"nden üretilen veri/trafik-carpan.json (araclar/trafik_hazirla.py):
pilot bölgedeki her geohash-6 karesi için gün tipi (hafta içi / cumartesi / pazar) × saat çarpanı. Anlık trafik DEĞİL, geçmiş aylardaki tipik trafik.
Anlık trafik gerekirse (ücretli yönlendirme servisi ya da İBB'nin lisanslı verisi) yalnız bu dosya değişir.
"""
import json
import time

from .ayarlar import KOK

DOSYA = KOK / "veri" / "trafik-carpan.json"
_B32 = "0123456789bcdefghjkmnpqrstuvwxyz"
_veri = None


def _yukle():
    global _veri
    if _veri is None:
        try:
            _veri = json.loads(DOSYA.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            _veri = {}  # dosya yoksa trafik çarpanı 1 (trafiksiz süre)
    return _veri


def geohash(lat, lng, uzunluk=6):
    la, lo, bit, ch, cift, sonuc = [-90.0, 90.0], [-180.0, 180.0], 0, 0, True, ""
    while len(sonuc) < uzunluk:
        ara, deger = (lo, lng) if cift else (la, lat)
        orta = (ara[0] + ara[1]) / 2
        if deger >= orta:
            ch, ara[0] = ch * 2 + 1, orta
        else:
            ch, ara[1] = ch * 2, orta
        cift, bit = not cift, bit + 1
        if bit == 5:
            sonuc, bit, ch = sonuc + _B32[ch], 0, 0
    return sonuc


def gun_saat(tarih=None, saat=None):
    """(gün tipi, saat): tarih 'YYYY-AA-GG', saat 'SS:DD'; boşsa şu an."""
    t = time.localtime()
    if tarih:
        try:
            t = time.strptime(f"{tarih} {saat or '12:00'}", "%Y-%m-%d %H:%M")
        except ValueError:
            pass
    g = t.tm_wday
    return ("hi" if g < 5 else "cmt" if g == 5 else "pzr"), t.tm_hour


def carpan(a, b, gun, saat):
    """a → b yolculuğunun çarpanı: düz hat üzerindeki 5 noktanın (başlangıç, ara noktalar, varış) karelerinin ortalaması.
    Kare veride yoksa pilot bölge geneli; dosya yoksa 1."""
    v = _yukle()
    if not v:
        return 1.0
    genel = v["genel"][gun][saat]
    degerler = []
    for i in range(5):
        f = i / 4
        h = v["hucre"].get(geohash(a["lat"] + (b["lat"] - a["lat"]) * f, a["lng"] + (b["lng"] - a["lng"]) * f))
        degerler.append(h[gun][saat] if h else genel)
    return round(sum(degerler) / len(degerler), 2)


def bilgi():
    v = _yukle()
    return {"kaynak": v.get("kaynak", ""), "donem": v.get("donem", []), "kare": len(v.get("hucre", {})), "var": bool(v)}
