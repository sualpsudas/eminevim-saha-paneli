"""SUNUM KAPISI — "Otomatik ilerlet": açık çağrıların hepsini bir sonraki aşamaya taşır (bilgisayarda canlı saha sunumu için).

Aşamalar: yeni çağrı → SPY atandı → yola çıktı → görüşmede → tamamlandı. Yeni çağrıya atama kuralıyla (atama.py) SPY bulunur ve
hemen kabul etmiş sayılır; müşteriye her aşamada bildirim gider. SPY yola çıkınca yerinde kalır (haritada rota çizilir), görüşmede müşterinin yerine gelir.
"""
from . import bildirim
from .atama import teklif_et
from .ayarlar import KAPALI_DURUMLAR
from .konum import konum_yaz
from .yardim import damga, olay, saat_yaz, simdi

DAKIKA = 60000


def _ilerle(veri, k):
    """Çağrıyı bir aşama ilerletir; döner: yeni aşama adı ("" = ilerlemedi)."""
    ad = (k.get("musteri") or {}).get("ad") or "Müşteri"
    durum = k.get("durum")
    if durum == "alindi":
        if not k.get("repId"):
            teklif_et(veri, k)
        if not k.get("repId"):
            return ""  # uygun SPY yok: kimse almadı olarak kalır
        k["durum"] = "atandi"
        (k.get("teklif") or {})["bitis"] = 0
        spy = veri["spyler"][k["repId"]]
        olay(veri, f"{ad}: temsilci belli oldu · {spy['ad']}", k["id"])
        bildirim.bildir_musteri(k, f"Temsilciniz belli oldu: {spy['ad']}", "Randevunuzu görmek için dokunun.")
        yeni = "atandi"
    elif durum in ("atandi", "netlesti"):
        spy = veri["spyler"][k["repId"]]
        k["durum"], k["varisZamani"] = "yolda", simdi() + 10 * DAKIKA
        olay(veri, f"{ad}: {spy['ad']} yola çıktı", k["id"])
        bildirim.bildir_musteri(k, f"Temsilciniz yola çıktı · tahmini varış {saat_yaz(k['varisZamani'])}", f"{spy['ad']} size doğru geliyor.")
        yeni = "yolda"
    elif durum in ("yolda", "gorusme"):
        spy = veri["spyler"][k["repId"]]
        konum = k.get("konum") or {}
        konum_yaz(spy["id"], konum["lat"], konum["lng"])
        k["durum"], k["dogrulandi"] = "gorusmede", {"zaman": simdi(), "yol": "kod"}
        olay(veri, f"{ad}: {spy['ad']} kapıda, görüşme başladı", k["id"])
        bildirim.bildir_musteri(k, f"Temsilciniz doğrulandı: {spy['ad']}", "Görüşmeniz başladı. İyi görüşmeler!")
        yeni = "gorusmede"
    elif durum == "gorusmede":
        k["durum"] = "tamamlandi"
        olay(veri, f"{ad}: görüşme tamamlandı", k["id"])
        yeni = "tamamlandi"
    else:
        return ""
    damga(veri, k)
    return yeni


def ilerlet(veri, _istek=None):
    """api/ilerlet: açık çağrıların hepsi bir aşama ilerler. Döner: {"ilerleyen": sayı}."""
    sayi = 0
    for k in sorted(veri["kayitlar"].values(), key=lambda x: x.get("olusma", 0)):
        if k.get("durum") not in KAPALI_DURUMLAR and _ilerle(veri, k):
            sayi += 1
    return {"ilerleyen": sayi}
