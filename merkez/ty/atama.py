"""ATAMA KAPISI — gelen çağrıyı hangi SPY'nin alacağı (kurallar: rapor/tasarruf-yanimda-proje-calismasi/10-atama-ve-rota.md).

adaylar(): eleme + puan. teklif_et(): en yüksek puanlıya teklif (2 dk kabul süresi). sureleri_denetle(): süresi dolanı sıradakine geçirir.
Ağırlıklar ve sınırlar merkez/ty/ayarlar.py'de; konum konum.py'den; H/G değerleri personel listesinden (veri/spyler.js).
Şirket başka bir atama kuralı isterse yalnız bu dosya değişir.
"""
import time

from .ayarlar import AGIRLIK, ARALIK_DK, GUNLUK_SINIR, HEMEN_DK, HG_TAVAN, KABUL_SN, KAPALI_DURUMLAR, YAKINLIK_KM
from .bildirim import bildir
from .konum import anlik_konum
from .yardim import bugun, dakika, damga, km, olay, simdi


def acik_sayi(veri, spy_id):
    return sum(1 for k in veri["kayitlar"].values() if k.get("repId") == spy_id and k.get("durum") not in KAPALI_DURUMLAR)


def hemen_mi(k):
    """Bugün ve saati en geç 2 saat sonra olan çağrı: o an hazırda olan SPY'ye gider."""
    if (k.get("tarih") or bugun()) < bugun():
        return True
    if (k.get("tarih") or bugun()) > bugun():
        return False
    d = dakika(k.get("saat"))
    an = time.localtime()
    return d is None or d - (an.tm_hour * 60 + an.tm_min) <= HEMEN_DK


def randevuda_mi(veri, spy_id):
    return any(x.get("repId") == spy_id and x.get("durum") in ("yolda", "gorusmede") for x in veri["kayitlar"].values())


def adaylar(veri, k, haric=()):
    """Eleme + puan. Döner: puana göre sıralı [(puan, spy, gerekçe, km)].
    Hemen: molada, yolda/görüşmede, günlük sınırı dolan elenir (uygulaması kapalı olabilir: bildirim gider); puan yakınlık 50, H/G 30, bugünkü çağrı 20.
    İleri saat/gün: o gün sınırı dolan, o saatin ±90 dk'sında randevusu olan elenir; puan H/G 50, yakınlık 30, o günkü çağrı 20."""
    konum = k.get("konum") or {}
    tarih = k.get("tarih") or bugun()
    hemen = hemen_mi(k)
    a = AGIRLIK["hemen" if hemen else "ileri"]
    gun_kayit = [x for x in veri["kayitlar"].values() if x.get("tarih") == tarih and x.get("durum") != "iptal" and x["id"] != k.get("id")]
    sonuc = []
    for s in veri["spyler"].values():
        if s["id"] in haric:
            continue
        benim = [x for x in gun_kayit if x.get("repId") == s["id"]]
        if len(benim) >= GUNLUK_SINIR:
            continue
        if hemen:
            if s.get("durum") == "molada" or randevuda_mi(veri, s["id"]):
                continue
            uzak = km(anlik_konum(veri, s), konum)
        else:
            d = dakika(k.get("saat"))
            if d is not None and any(dakika(x.get("saat")) is not None and abs(dakika(x.get("saat")) - d) < ARALIK_DK for x in benim):
                continue
            noktalar = [s] + [x["konum"] for x in benim if isinstance(x.get("konum"), dict) and "lat" in x["konum"]]
            uzak = min(km(n, konum) for n in noktalar)  # kendi bölgesine ya da o günkü randevularına en yakın nokta
        p = {"randevu": min(max((s.get("randevuHG", 100) - 100) / HG_TAVAN, 0), 1),
             "ciro": min(max((s.get("ciroHG", 100) - 100) / HG_TAVAN, 0), 1),
             "yakinlik": max(0.0, 1 - uzak / YAKINLIK_KM),
             "yuk": 1 - len(benim) / GUNLUK_SINIR}
        puan = round(sum(a[x] * p[x] for x in a), 1)
        gerekce = f"{str(round(uzak, 1)).replace('.', ',')} km · H/G %{s.get('randevuHG')}/%{s.get('ciroHG')} · {'bugün' if tarih == bugun() else 'o gün'} {len(benim)} çağrı"
        sonuc.append((puan, s, gerekce, round(uzak, 1)))
    return sorted(sonuc, key=lambda x: -x[0])


ILETIM_BEKLEME_SN = 10  # çağrı geldikten sonra SPY'ye iletilene kadar (sunumda "alındı" aşaması görünsün)


def teklif_et(veri, k, neden=""):
    """Çağrıyı sıradaki en yüksek puanlı SPY'ye teklif eder; uygun kimse kalmadıysa "kimse almadı" (haritada kırmızı)."""
    k.pop("teklifZamani", None)
    t = k.setdefault("teklif", {"denenen": []})
    liste = adaylar(veri, k, set(t["denenen"]) | set(k.get("eskiRepler", [])))
    ad = (k.get("musteri") or {}).get("ad") or "Müşteri"
    if not liste:
        if k.get("repId"):
            k["eskiRepler"] = sorted(set(k.get("eskiRepler", [])) | {k["repId"]})
        ilk = not k.get("sahipsiz")
        k.update({"repId": None, "sahipsiz": True, "durum": "alindi", "gerekce": ""})
        t["bitis"] = 0
        if ilk:
            olay(veri, f"{ad}: uygun SPY kalmadı → kimse almadı{neden}", k["id"])
        return k
    puan, spy, gerekce, uzak = liste[0]
    if k.get("repId") and k["repId"] != spy["id"]:
        k["eskiRepler"] = sorted(set(k.get("eskiRepler", [])) | {k["repId"]})
    t["denenen"].append(spy["id"])
    t["bitis"] = simdi() + KABUL_SN * 1000
    k.update({"repId": spy["id"], "sahipsiz": False, "durum": "alindi", "atanma": simdi(), "uzaklikKm": uzak, "atamaPuan": puan, "gerekce": gerekce})
    olay(veri, f"{ad} ({k.get('yer') or ''}) → {spy['ad']} · puan {str(puan).replace('.', ',')} · {gerekce}{neden}", k["id"])
    zaman = " ".join(x for x in (k.get("gunYazi") or k.get("tarih") or "", k.get("saat") or "") if x)
    bildir(spy["id"], {"baslik": f"Yeni çağrı: {ad}", "govde": " · ".join(x for x in (k.get("yer"), zaman, "2 dk içinde kabul edin") if x),
                       "etiket": k["id"], "rid": k["id"]})
    return k


def sureleri_denetle(veri):
    """2 dakikada kabul edilmeyen teklifleri sıradaki SPY'ye geçirir; kimsenin almadığı çağrıya yeni uygun SPY
    çıktıysa (moladan döndü, uygulamayı açtı) ona teklif eder. Değişiklik olduysa True."""
    degisti = False
    for k in veri["kayitlar"].values():
        t = k.get("teklif") or {}
        if k.get("durum") == "alindi" and not k.get("repId") and not k.get("sahipsiz") and k.get("teklifZamani") and k["teklifZamani"] <= simdi():
            teklif_et(veri, k)
            damga(veri, k)
            degisti = True
        elif k.get("durum") == "alindi" and k.get("repId") and t.get("bitis") and t["bitis"] < simdi():
            teklif_et(veri, k, " (önceki 2 dk içinde kabul etmedi)")
            damga(veri, k)
            degisti = True
        elif k.get("durum") == "alindi" and k.get("sahipsiz") and adaylar(veri, k, set(t.get("denenen", [])) | set(k.get("eskiRepler", []))):
            teklif_et(veri, k, " (yeni uygun SPY)")
            damga(veri, k)
            degisti = True
    return degisti
