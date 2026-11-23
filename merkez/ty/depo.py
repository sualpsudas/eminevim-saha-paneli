"""DEPO KAPISI — çağrılar, mesajlar, SPY durumları ve müşteri hesapları.

Şu an tek JSON dosyası (merkez/veri.json; deneme kopyasında TY_VERI). Her istek kilit altında oku → değiştir → yaz.
Gerçek sistemde oku()/yaz() şirket veritabanına bağlanır; yapının alanları IT_DEVIR.md → Depo.
"""
import json
import os
import threading
import time

from .ayarlar import VERI
from .musteri import ORNEK_MUSTERILER
from .personel import SPYLER

kilit = threading.Lock()


def bos_veri():
    return {"surum": 1, "spyler": {s["id"]: {**s, "durum": "musait", "sonGorulme": 0} for s in SPYLER}, "kayitlar": {},
            "musteriler": {t: dict(m) for t, m in ORNEK_MUSTERILER.items()}, "olaylar": [], "kimlikler": {}}


def oku():
    if not VERI.exists():
        yaz(bos_veri())
    veri = json.loads(VERI.read_text(encoding="utf-8"))
    veri.setdefault("kimlikler", {})
    musteriler = veri.setdefault("musteriler", {})
    for tel, m in ORNEK_MUSTERILER.items():
        musteriler.setdefault(tel, dict(m))
    eski = veri["spyler"]
    veri["spyler"] = {s["id"]: {**eski.get(s["id"], {"durum": "musait", "sonGorulme": 0}), **s} for s in SPYLER}  # listeden çıkan SPY düşer
    return veri


def degistir(gecici, hedef):
    # Windows: hedefi o an başka bir program (virüs tarayıcısı, yedekleme, okuyan süreç) açık tutuyorsa
    # yer değiştirme "erişim engellendi" verir; kısa aralıklarla yeniden dene
    for deneme in range(20):
        try:
            return os.replace(gecici, hedef)
        except PermissionError:
            if deneme == 19:
                raise
            time.sleep(0.05)


def json_yaz(dosya, icerik):
    gecici = dosya.with_suffix(".tmp")
    gecici.write_text(json.dumps(icerik, ensure_ascii=False), encoding="utf-8")
    degistir(gecici, dosya)


def yaz(veri):
    json_yaz(VERI, veri)
