"""BÖLGE KAPISI — bir nokta pilot bölgede (Üsküdar, Ümraniye, Ataşehir) mi?
Sınırlar assets/pilot-sinirlar.js'ten okunur (takip haritasının çizdiği aynı veri: window.TY_SINIRLAR = {...};)."""
import json
import re
from pathlib import Path

DOSYA = Path(__file__).resolve().parent.parent.parent / "assets" / "pilot-sinirlar.js"
_halkalar = None
_ilceler = None


def _yukle():
    global _halkalar, _ilceler
    if _halkalar is None:
        try:
            m = re.search(r"window\.TY_SINIRLAR\s*=\s*(\{.*\});?\s*$", DOSYA.read_text(encoding="utf-8"), re.S)
            _ilceler = [(i["ad"], i["halkalar"]) for i in json.loads(m.group(1))["ilceler"]]
            _halkalar = [h for _, hs in _ilceler for h in hs]
        except Exception:
            _ilceler, _halkalar = [], []  # sınır okunamadıysa denetim yapılmaz (her yer bölge içi sayılır)
    return _halkalar


def _icinde(lat, lng, halka):
    ic = False
    j = len(halka) - 1
    for i, (a, b) in enumerate(halka):
        c, d = halka[j]
        if (b > lng) != (d > lng) and lat < (c - a) * (lng - b) / (d - b) + a:
            ic = not ic
        j = i
    return ic


def bolgede_mi(lat, lng):
    halkalar = _yukle()
    return not halkalar or any(_icinde(lat, lng, h) for h in halkalar)


def ilce_bul(lat, lng):
    """Noktanın pilot ilçesi (Üsküdar / Ümraniye / Ataşehir); bölge dışıysa ya da sınır okunamadıysa None."""
    _yukle()
    for ad, halkalar in _ilceler or []:
        if any(_icinde(lat, lng, h) for h in halkalar):
            return ad
    return None
