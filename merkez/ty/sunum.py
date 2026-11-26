"""SUNUM KAPISI — "Otomatik ilerlet": açık çağrıların hepsini bir sonraki aşamaya taşır (bilgisayarda canlı saha sunumu için).

Aşamalar: yeni çağrı → SPY atandı → yola çıktı → görüşmede → tamamlandı. Yeni çağrıya atama kuralıyla (atama.py) SPY bulunur ve
hemen kabul etmiş sayılır; müşteriye her aşamada bildirim gider. SPY yola çıkınca yerinde kalır (haritada rota çizilir), görüşmede müşterinin yerine gelir.
Tahmini varış her SPY'nin kendi rotasından (atama.varis_dk: İBB anlık hızı); haritadaki yürüyüş de bu süreyle orantılı.
"""
from . import bildirim
from .atama import teklif_et, varis_dk
from .ayarlar import KAPALI_DURUMLAR
from .konum import anlik_konum, konum_yaz
from .yardim import damga, olay, saat_yaz, simdi

DAKIKA = 60000
YOL_SN_DK, YOL_SN_EN_AZ, YOL_SN_EN_COK = 3, 10, 90  # sunumda yürüyüş: gerçek varış süresinin her dakikası 3 sn (10-90 sn arası)


def _varis(veri, k):
    """SPY müşterinin yerine vardı: görüşme başlar (yürüyüş bitince kendiliğinden ya da erken basışta)."""
    ad = (k.get("musteri") or {}).get("ad") or "Müşteri"
    spy = veri["spyler"][k["repId"]]
    konum = k.get("konum") or {}
    veri.get("elleKonum", {}).pop(spy["id"], None)  # varış: elle taşınan konum bırakılır
    konum_yaz(spy["id"], konum["lat"], konum["lng"])
    k["durum"], k["dogrulandi"] = "gorusmede", {"zaman": simdi(), "yol": "kod"}
    olay(veri, f"{ad}: {spy['ad']} kapıda, görüşme başladı", k["id"])
    bildirim.bildir_musteri(k, f"Temsilciniz doğrulandı: {spy['ad']}", "Görüşmeniz başladı. İyi görüşmeler!")
    damga(veri, k)


def varis_denetle(veri):
    """Yürüyüş süresi dolan SPY müşteriye varmış sayılır, görüşme kendiliğinden başlar. Değişiklik olduysa True."""
    degisti = False
    for k in veri["kayitlar"].values():
        if k.get("durum") in ("yolda", "gorusme") and k.get("yolBasladi") and k.get("repId") and simdi() >= k["yolBasladi"] + (k.get("yolSure") or 0):
            _varis(veri, k)
            degisti = True
    return degisti


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
        konum = k.get("konum") or {}
        dk = varis_dk(anlik_konum(veri, spy), konum) if "lat" in konum else 10  # her SPY'nin kendi rotası (anlık trafikle)
        k["durum"], k["varisZamani"], k["yolaCikis"], k["yolDk"] = "yolda", simdi() + max(1, round(dk)) * DAKIKA, simdi(), dk
        if spy.get("sim"):  # temsilci belli olunca hareketli SPY durmaz; yola çıkınca durur: rota hep aynı yerden çizilir, yürüyüş buradan başlar
            k["don"] = dict(anlik_konum(veri, spy), id=spy["id"])
        olay(veri, f"{ad}: {spy['ad']} yola çıktı", k["id"])
        bildirim.bildir_musteri(k, f"Temsilciniz yola çıktı · tahmini varış {saat_yaz(k['varisZamani'])}", f"{spy['ad']} size doğru geliyor.")
        yeni = "yolda"
    elif durum in ("yolda", "gorusme") and not k.get("yolBasladi"):
        # SPY rota boyunca müşteriye doğru yürür (takip sayfası animasyonla gösterir; merkez zamana göre doğru çizgide hesaplar)
        spy = veri["spyler"][k["repId"]]
        k["yolBaslangic"] = dict(anlik_konum(veri, spy))
        k.pop("don", None)
        k["yolBasladi"] = simdi()
        k["yolSure"] = int(max(YOL_SN_EN_AZ, min(YOL_SN_EN_COK, (k.get("yolDk") or 10) * YOL_SN_DK)) * 1000)  # uzak SPY daha geç varır
        veri.get("elleKonum", {}).pop(spy["id"], None)
        olay(veri, f"{ad}: {spy['ad']} müşteriye doğru ilerliyor", k["id"])
        yeni = "yolda"
    elif durum in ("yolda", "gorusme"):
        _varis(veri, k)
        yeni = "gorusmede"
    elif durum == "gorusmede":
        k["durum"] = "tamamlandi"
        olay(veri, f"{ad}: görüşme tamamlandı", k["id"])
        yeni = "tamamlandi"
    else:
        return ""
    damga(veri, k)
    return yeni


SIM_KABUL_SN = 4  # hareketli örnek SPY teklifi bu kadar sonra kendiliğinden kabul eder (gerçek SPY uygulamadan kabul eder)


def sim_kabul(veri):
    """Hareketli örnek SPY'ye giden teklif birkaç saniye sonra kabul edilir (müşteriye "temsilciniz belli oldu" gider). Değişiklik olduysa True."""
    degisti = False
    for k in veri["kayitlar"].values():
        s = veri["spyler"].get(k.get("repId") or "")
        if s and s.get("sim") and k.get("durum") == "alindi" and k.get("kaynak") != "yonetici" and not k.get("sahipsiz") and k.get("atanma") and simdi() >= k["atanma"] + SIM_KABUL_SN * 1000:
            degisti = bool(_ilerle(veri, k)) or degisti
    return degisti


YOLA_CIKIS_BEKLEME_SN = 2  # "yola çıktı" yazıldıktan sonra ilerletilmezse SPY bu kadar sonra kendiliğinden yürümeye başlar


def yurume_baslat(veri):
    """Yola çıktı yazılıp 2 sn içinde ilerletilmediyse SPY müşteriye doğru yürümeye başlar. Değişiklik olduysa True."""
    degisti = False
    for k in veri["kayitlar"].values():
        if k.get("durum") == "yolda" and k.get("repId") and not k.get("yolBasladi") and k.get("yolaCikis") and simdi() >= k["yolaCikis"] + YOLA_CIKIS_BEKLEME_SN * 1000:
            degisti = bool(_ilerle(veri, k)) or degisti
    return degisti


def sunum_denetle(veri):
    """Bekçi (her saniye): örnek SPY kabulü + yola çıkınca yürüme + varışta görüşme. Değişiklik olduysa True."""
    return sim_kabul(veri) | yurume_baslat(veri) | varis_denetle(veri)


def ilerlet(veri, _istek=None):
    """api/ilerlet: açık çağrıların hepsi bir aşama ilerler. Döner: {"ilerleyen": sayı}.
    Önerilen ileri randevuyu kabul etmiş çağrılar (oneriKabul, SPY henüz yola çıkmadı) sıra bekler: öteki açık çağrılar bitene kadar
    ilerletilmez, bitince bir sonraki basışta birlikte ilerler (randevu saati geldi sayılır)."""
    acik = sorted((k for k in veri["kayitlar"].values() if k.get("durum") not in KAPALI_DURUMLAR), key=lambda x: x.get("olusma", 0))
    bekleyen = [k for k in acik if k.get("oneriKabul") and k.get("durum") in ("alindi", "atandi", "netlesti")]
    sahipsiz = [k for k in acik if k.get("sahipsiz") and not k.get("repId") and k not in bekleyen]  # SPY'si yok: engel olmaz, yine de SPY aranır
    simdiki = [k for k in acik if k not in bekleyen and k not in sahipsiz]
    sayi = 0
    for k in (simdiki or bekleyen) + sahipsiz:
        if _ilerle(veri, k):
            sayi += 1
    return {"ilerleyen": sayi, "bekleyen": len(bekleyen) if simdiki else 0}
