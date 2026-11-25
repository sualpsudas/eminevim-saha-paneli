"""ATAMA KAPISI — gelen çağrıyı hangi SPY'nin alacağı (kurallar: rapor/tasarruf-yanimda-proje-calismasi/10-atama-ve-rota.md).

adaylar(): eleme + puan. teklif_et(): en yüksek puanlıya teklif (2 dk kabul süresi). sureleri_denetle(): süresi dolanı sıradakine geçirir.
Ağırlıklar ve sınırlar merkez/ty/ayarlar.py'de; konum konum.py'den; H/G değerleri personel listesinden (veri/spyler.js).
Şirket başka bir atama kuralı isterse yalnız bu dosya değişir.
"""
import time

from .ayarlar import AGIRLIK, ARALIK_DK, GUNLUK_SINIR, HEMEN_DK, HG_TAVAN, KABUL_SN, KAPALI_DURUMLAR, YAKINLIK_KM
from .bildirim import bildir, bildir_musteri
from .bolge import ilce_bul
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


def mesgul_mu(veri, spy_id, haric_id=None):
    """SPY şu an başka bir müşteriye bağlı mı: yolda/görüşmede ya da teklif beklenen/atanmış ve zamanı yakın (hemen) çağrısı var.
    Aynı SPY aynı anda iki müşteriye gönderilmez; yeni çağrıya sıradaki uygun SPY atanır."""
    for x in veri["kayitlar"].values():
        if x.get("repId") != spy_id or x.get("id") == haric_id or x.get("durum") in KAPALI_DURUMLAR:
            continue
        if x.get("durum") in ("yolda", "gorusme", "gorusmede") or hemen_mi(x):
            return True
    return False


def adaylar(veri, k, haric=()):
    """Eleme + puan. Döner: puana göre sıralı [(puan, spy, gerekçe, km)].
    Yalnız müşterinin ilçesindeki SPY'ler aday olur (ilçe pilot sınırlarından bulunur; bölge dışıysa ilçe denetimi yok).
    Hemen: molada, başka müşteriye bağlı (teklif/atandı/yolda/görüşmede), günlük sınırı dolan elenir (uygulaması kapalı olabilir: bildirim gider); puan yakınlık 50, ciro H/G 25, randevu H/G 15, bugünkü çağrı 10.
    İleri saat/gün: o gün sınırı dolan, o saatin ±60 dk'sında randevusu olan elenir (hemen çağrıda da: bir SPY bir saatte en fazla bir randevu); puan aynı ağırlıklar (yakınlık 50, ciro 25, randevu 15, o günkü çağrı 10)."""
    konum = k.get("konum") or {}
    tarih = k.get("tarih") or bugun()
    hemen = hemen_mi(k)
    a = AGIRLIK["hemen" if hemen else "ileri"]
    gun_kayit = [x for x in veri["kayitlar"].values() if x.get("tarih") == tarih and x.get("durum") != "iptal" and x["id"] != k.get("id")]
    ilce = ilce_bul(konum.get("lat"), konum.get("lng")) if isinstance(konum.get("lat"), (int, float)) and isinstance(konum.get("lng"), (int, float)) else None
    sonuc = []
    for s in veri["spyler"].values():
        if s["id"] in haric or (ilce and s.get("ilce") != ilce):  # SPY yalnız kendi ilçesindeki müşteriye gider
            continue
        benim = [x for x in gun_kayit if x.get("repId") == s["id"]]
        if len(benim) >= GUNLUK_SINIR:
            continue
        d = dakika(k.get("saat"))
        if d is None and tarih == bugun():
            an = time.localtime()
            d = an.tm_hour * 60 + an.tm_min
        if d is not None and any(dakika(x.get("saat")) is not None and abs(dakika(x.get("saat")) - d) < ARALIK_DK for x in benim):
            continue  # bir SPY bir saatte en fazla bir randevu: o saatte randevusu olan elenir, çağrı sıradakine / sonraki saate gider
        if hemen:
            if s.get("durum") == "molada" or mesgul_mu(veri, s["id"], k.get("id")):
                continue
            uzak = km(anlik_konum(veri, s), konum)
        else:
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


GUN_AD = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
AY_AD = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
RANDEVU_BAS, RANDEVU_SON = 10 * 60, 20 * 60  # önerilebilen saat aralığı (web formundaki gibi 10:00–20:00)


def oneri_bul(veri, k):
    """İlçede o an uygun SPY yoksa müşteriye önerilecek ilk randevu: bugünden 7 gün içinde, 30 dakikalık adımlarla, ilçedeki bir SPY'nin
    ileri-saat kurallarına (günlük sınır, 60 dk içinde başka randevu yok) uyduğu ilk saat. Döner: {"tarih","saat","gunYazi","repId","repAd"} ya da None."""
    haric = set(k.get("eskiRepler", []))
    an = time.time() + (HEMEN_DK + 1) * 60
    ist = dakika(k.get("saat"))
    if k.get("tarih") and ist is not None:  # istenen saatten önce önerilmez
        try:
            an = max(an, time.mktime(time.strptime(k["tarih"], "%Y-%m-%d")) + ist * 60 + 30 * 60)
        except ValueError:
            pass
    adim = 30 * 60
    t = (int(an) // adim + 1) * adim
    for _ in range(7 * 48):
        yerel = time.localtime(t)
        dk = yerel.tm_hour * 60 + yerel.tm_min
        if RANDEVU_BAS <= dk <= RANDEVU_SON:
            tarih = time.strftime("%Y-%m-%d", yerel)
            k2 = {**k, "tarih": tarih, "saat": time.strftime("%H:%M", yerel)}
            liste = [x for x in adaylar(veri, k2, haric) if not any(  # başka müşteriye önerilmiş (henüz yanıtlanmamış) saat de dolu sayılır
                y["id"] != k.get("id") and (y.get("oneri") or {}).get("repId") == x[1]["id"] and (y["oneri"].get("tarih") == tarih)
                and abs(dakika(y["oneri"].get("saat")) - dk) < ARALIK_DK for y in veri["kayitlar"].values())]
            if liste:
                gun = "Bugün" if tarih == bugun() else f"{yerel.tm_mday} {AY_AD[yerel.tm_mon - 1]} {GUN_AD[yerel.tm_wday]}"
                return {"tarih": tarih, "saat": k2["saat"], "gunYazi": gun, "repId": liste[0][1]["id"], "repAd": liste[0][1]["ad"]}
        t += adim
    return None


ILETIM_BEKLEME_SN = 4  # çağrı geldikten sonra SPY'ye iletilene kadar (sunumda "alındı" aşaması görünsün)


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
        if not k.get("oneri") and not k.get("oneriYok") and not k.get("bolgeDisi"):
            o = oneri_bul(veri, k)
            if o:  # ilçede şu an uygun SPY yok: müşteriye sonraki uygun randevu saati önerilir (uygulamada kabul / başka saat)
                k["oneri"] = o
                olay(veri, f"{ad}: ilçede şu an uygun SPY yok → randevu önerildi: {o['gunYazi']} {o['saat']} ({o['repAd']}){neden}", k["id"])
                bildir_musteri(k, "Bu saatte uygun temsilcimiz yok", f"Size {o['gunYazi']} {o['saat']} için randevu önerelim. Uygulamadan onaylayabilirsiniz.")
                return k
        if ilk and not k.get("oneri"):
            olay(veri, f"{ad}: uygun SPY kalmadı → kimse almadı{neden}", k["id"])
        return k
    puan, spy, gerekce, uzak = liste[0]
    k.pop("oneri", None)  # uygun SPY çıktı: öneri geçersiz, çağrı doğrudan teklif edilir
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


def yeniden_ata(veri, k, neden=""):
    """Konum değişti (müşteri ya da SPY haritada taşındı): henüz kabul edilmemiş çağrıyı yeniden değerlendirir.
    Daha uygun bir SPY çıktıysa teklif ona geçer (eskisi artık kabul edemez); mevcut SPY hâlâ en iyisiyse teklif ve süre sürer, uzaklık/puan güncellenir.
    Kabul edilmiş (atandı, yolda...) ya da henüz iletilmemiş (ilk 10 sn) çağrıya dokunmaz. Teklifi başka SPY'ye geçirdiyse True."""
    if k.get("durum") != "alindi" or k.get("teklifZamani") or k.get("bolgeDisi"):
        return False
    liste = adaylar(veri, k, set(k.get("eskiRepler", [])))
    if liste and k.get("repId") == liste[0][1]["id"] and not k.get("sahipsiz"):
        puan, _, gerekce, uzak = liste[0]
        k.update({"uzaklikKm": uzak, "atamaPuan": puan, "gerekce": gerekce})
        damga(veri, k)
        return False
    if not liste and (k.get("sahipsiz") or not k.get("repId")):
        return False
    eski = k.get("repId")
    teklif_et(veri, k, neden)
    if eski and k.get("repId") != eski:  # eskisi reddetmedi, yalnız konum değişti: ileride yeniden uygun olabilir
        k["eskiRepler"] = [x for x in k.get("eskiRepler", []) if x != eski]
        k["teklif"]["denenen"] = [x for x in k["teklif"]["denenen"] if x != eski]
    damga(veri, k)
    return True


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
        elif k.get("durum") == "alindi" and k.get("sahipsiz") and not k.get("bolgeDisi") and adaylar(veri, k, set(t.get("denenen", [])) | set(k.get("eskiRepler", []))):
            teklif_et(veri, k, " (yeni uygun SPY)")
            damga(veri, k)
            degisti = True
    return degisti
