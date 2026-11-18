"""PERSONEL KAPISI — merkezin SPY listesi.

Şu an: veri/spyler.js (uygulama da aynı dosyayı okur). Bu dosya şirket verisinden üretilir:
    python araclar/veri_hazirla.py   (personel + şube/klasman + hedef + satış + randevu → H/G, otomatik liste)
Gerçek sistemde: spyleri_oku() IT'nin personel servisine bağlanır; dönen her SPY'de en az
    id, sicil, ad, sube, ilce, mahalle, lat, lng, randevuHG, ciroHG   (ayrıntı IT_DEVIR.md → Personel)
Liste değişince merkez yeniden başlatılır.
"""
import json

from .ayarlar import SPY_DOSYASI


def spyleri_oku():
    metin = SPY_DOSYASI.read_text(encoding="utf-8")
    liste = json.loads(metin[metin.index("["):metin.rindex("]") + 1])
    return [{**x, "yer": f"{x['mahalle']}, {x['ilce']}"} for x in liste]


SPYLER = spyleri_oku()
SPY_IDLER = {s["id"] for s in SPYLER}
