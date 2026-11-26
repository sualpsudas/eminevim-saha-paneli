"""ATAMA KAPISI — gelen çağrıyı hangi SPY'nin alacağı (kurallar: rapor/tasarruf-yanimda-proje-calismasi/10-atama-ve-rota.md).

adaylar(): eleme + puan. teklif_et(): en yüksek puanlıya teklif (2 dk kabul süresi). sureleri_denetle(): süresi dolanı sıradakine geçirir.
Seçenekler (ağırlıklar, uzaklık türü, sınırlar): varsayılan ayarlar.ATAMA_VARSAYILAN, takip sayfasında değiştirilen veri["atamaAyar"] (ayar()).
Konum konum.py'den, yol mesafesi/süresi yol.py'den, trafik çarpanı trafik.py'den; H/G değerleri personel listesinden (veri/spyler.js).
Şirket başka bir atama kuralı isterse yalnız bu dosya değişir.
"""
import copy
import time

from . import trafik, yol
from .ayarlar import ATAMA_VARSAYILAN, HEMEN_DK, HG_TAVAN, KABUL_SN, KAPALI_DURUMLAR, UZAKLIK_TURLERI
from .bildirim import bildir, bildir_musteri
from .bolge import ilce_bul
from .konum import anlik_konum
from .personel import SUBELER
from .yardim import bugun, dakika, damga, km, olay, simdi


def ayar(veri):
    """Geçerli atama seçenekleri: varsayılanlar + takip sayfasında değiştirilenler."""
    a = copy.deepcopy(ATAMA_VARSAYILAN)
    kayitli = veri.get("atamaAyar") or {}
    a["agirlik"].update({x: v for x, v in (kayitli.get("agirlik") or {}).items() if x in a["agirlik"]})
    a.update({x: v for x, v in kayitli.items() if x != "agirlik" and x in a})
    return a


def ayar_kaydet(veri, gelen):
    """Takip sayfasından gelen seçenekleri denetleyip kaydeder; gelen boşsa varsayılana döner. Döner: geçerli ayar."""
    if not gelen:
        veri.pop("atamaAyar", None)
        return ayar(veri)
    a = ayar(veri)
    for x, v in (gelen.get("agirlik") or {}).items():
        if x in a["agirlik"]:
            a["agirlik"][x] = max(0, min(100, int(v)))
    if sum(a["agirlik"].values()) <= 0:
        raise ValueError("En az bir ölçütün ağırlığı sıfırdan büyük olmalı.")
    if "uzaklik" in gelen:
        if gelen["uzaklik"] not in UZAKLIK_TURLERI:
            raise ValueError("Uzaklık türü geçersiz.")
        a["uzaklik"] = gelen["uzaklik"]
    for x, en_az, en_cok in (("sifirDk", 5, 180), ("sifirKm", 1, 60), ("gunlukSinir", 1, 20), ("aralikDk", 0, 240), ("subeSaat", 1, 48), ("canliSaat", 0, 12)):
        if x in gelen:
            a[x] = max(en_az, min(en_cok, int(gelen[x])))
    if "oncelikKm" in gelen:
        a["oncelikKm"] = max(0.0, min(20.0, round(float(gelen["oncelikKm"]), 1)))
    if "ilceOnceligi" in gelen:
        a["ilceOnceligi"] = bool(gelen["ilceOnceligi"])
    veri["atamaAyar"] = a
    return a


def acik_sayi(veri, spy_id):
    return sum(1 for k in veri["kayitlar"].values() if k.get("repId") == spy_id and k.get("durum") not in KAPALI_DURUMLAR)


def hemen_mi(k):
    """Bugün ve saati en geç HEMEN_DK (1 saat) sonra olan çağrı: o an hazırda olan SPY'ye gider."""
    if (k.get("tarih") or bugun()) < bugun():
        return True
    if (k.get("tarih") or bugun()) > bugun():
        return False
    d = dakika(k.get("saat"))
    an = time.localtime()
    return d is None or d - (an.tm_hour * 60 + an.tm_min) <= HEMEN_DK


def kalan_dk(k):
    """Randevu saatine kaç dakika var (geçmiş/saatsiz bugün: 0, ileri gün: gün farkıyla)."""
    tarih = k.get("tarih") or bugun()
    d = dakika(k.get("saat"))
    an = time.localtime()
    simdi_dk = an.tm_hour * 60 + an.tm_min
    try:
        gun = round((time.mktime(time.strptime(tarih, "%Y-%m-%d")) - time.mktime(time.strptime(bugun(), "%Y-%m-%d"))) / 86400)
    except ValueError:
        gun = 0
    return max(0, gun * 1440 + (d if d is not None else simdi_dk) - simdi_dk)


def sube_yeri(s):
    """SPY'nin şubesinin konumu; şube listede yoksa kendi kayıtlı yeri."""
    sb = SUBELER.get(s.get("sube"))
    return ({"lat": sb["lat"], "lng": sb["lng"]}, "şubesinden") if sb else ({"lat": s["lat"], "lng": s["lng"]}, "kayıtlı yerinden")


def sube_ilce(s):
    """SPY'nin şubesinin ilçesi (şube konumundan); şube listede yoksa SPY'nin kayıtlı ilçesi."""
    sb = SUBELER.get(s.get("sube"))
    return (ilce_bul(sb["lat"], sb["lng"]) if sb else None) or s.get("ilce")


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


def _sayi(x):
    return str(x).replace(".", ",")


def adaylar(veri, k, haric=(), elenen=None, olc=True):
    """Eleme + puan. Döner: puana göre sıralı [(puan, spy, gerekçe, km, ayrıntı)]; elenen listesi verilirse elenenler gerekçesiyle eklenir.
    olc=False: yalnız uygunluk (uzaklık ölçülmez, puan 0) — sık yoklamada yol servisine istek gitmesin.
    Eleme: günlük sınırı dolan, istenen saatin ±aralikDk'sında randevusu olan;
    hemen çağrıda ayrıca molada olan ya da başka müşteriye bağlı olan (teklif/atandı/yolda/görüşmede).
    Puan (ağırlıklar seçeneklerde; varsayılan yakınlık 40, çağrı sayısı 30, ciro H/G 20, randevu H/G 10):
      yakınlık: hemen çağrıda SPY'nin şu anki yerinden; ileri çağrıda şu anki yerinden (randevuya subeSaat saatten az varsa) ya da
                şubesinden (subeSaat ve fazlası), ayrıca o günkü randevularından en yakını;
                uzaklık türü trafikli (yol süresi × İBB tipik trafik çarpanı), yol süresi, yol km ya da kuş uçuşu km.
    Öncelik (eleme değil, sıra): 1) şubesi müşterinin ilçesinde olanlar (ilceOnceligi), 2) bunların içinde yol mesafesi oncelikKm'nin
      altındakiler, sonra puan. Öndekilerin hepsi reddederse sıra arkadakilere (başka ilçedeki SPY'ler de alabilir) geçer.
      çağrı sayısı: o gün az çağrısı olan önde. H/G: %100'de sıfır, %100+HG_TAVAN'da tam puan."""
    A = ayar(veri)
    konum = k.get("konum") or {}
    tarih = k.get("tarih") or bugun()
    hemen = hemen_mi(k)
    subeden = not hemen and kalan_dk(k) >= A["subeSaat"] * 60
    a = A["agirlik"]
    sinir = A["gunlukSinir"]
    gun_kayit = [x for x in veri["kayitlar"].values() if x.get("tarih") == tarih and x.get("durum") != "iptal" and x["id"] != k.get("id")]
    konumlu = isinstance(konum.get("lat"), (int, float)) and isinstance(konum.get("lng"), (int, float))
    ilce = ilce_bul(konum["lat"], konum["lng"]) if konumlu and A["ilceOnceligi"] else None
    d = dakika(k.get("saat"))
    if d is None and tarih == bugun():
        an = time.localtime()
        d = an.tm_hour * 60 + an.tm_min

    def ele(s, neden):
        if elenen is not None:
            elenen.append({"id": s["id"], "ad": s["ad"], "neden": neden})

    uygun = []  # (spy, noktalar, o günkü kayıtları)
    for s in veri["spyler"].values():
        if s["id"] in haric:
            ele(s, "daha önce teklif edildi ya da devretti")
            continue
        benim = [x for x in gun_kayit if x.get("repId") == s["id"]]
        if len(benim) >= sinir:
            ele(s, f"günlük sınır dolu ({len(benim)}/{sinir})")
            continue
        if d is not None and any(dakika(x.get("saat")) is not None and abs(dakika(x.get("saat")) - d) < A["aralikDk"] for x in benim):
            ele(s, f"{A['aralikDk']} dk içinde başka randevusu var")
            continue  # o saatte randevusu olan elenir, çağrı sıradakine / sonraki saate gider
        if hemen:
            if s.get("durum") == "molada":
                ele(s, "molada")
                continue
            if mesgul_mu(veri, s["id"], k.get("id")):
                ele(s, "başka müşteride")
                continue
            noktalar = [(anlik_konum(veri, s), "şu anki yerinden")]
        else:
            bas = sube_yeri(s) if subeden else (anlik_konum(veri, s), "şu anki yerinden")
            noktalar = [bas] + [(x["konum"], "o günkü randevusundan") for x in benim if isinstance(x.get("konum"), dict) and "lat" in x["konum"]]
        uygun.append((s, noktalar, benim))
    if not olc:
        return [(0, s, "", 0, {}) for s, _, _ in uygun]
    if not uygun:
        return []

    tur = A["uzaklik"]
    hepsi = [n for _, nk, _ in uygun for n, _ in nk]
    if not konumlu:
        olcum = [{"km": 0.0, "dk": 0.0, "kaynak": "yok"} for _ in hepsi]
    elif tur == "kus":
        olcum = [{"km": round(km(n, konum), 1), "dk": None, "kaynak": "kus"} for n in hepsi]
    else:
        olcum = yol.olc(hepsi, konum)  # tek istekte tüm adaylar
    gun, saat = trafik.gun_saat(tarih)
    if d is not None:
        saat = min(23, d // 60)
    sure_ile = tur in ("trafikli", "yol")
    canli = tur == "trafikli" and konumlu and A["canliSaat"] > 0 and kalan_dk(k) < A["canliSaat"] * 60
    sifir = A["sifirDk"] if sure_ile else A["sifirKm"]
    sonuc, i = [], 0
    for s, noktalar, benim in uygun:
        enyakin = None
        for n, nereden in noktalar:
            o = dict(olcum[i], nereden=nereden, trafik="tipik" if tur == "trafikli" else "")
            o["_n"] = n
            i += 1
            o["carpan"] = trafik.carpan(n, konum, gun, saat) if tur == "trafikli" and konumlu else 1.0
            if o["dk"] is not None:
                o["dk"] = round(o["dk"] * o["carpan"], 1)
            o["deger"] = o["dk"] if sure_ile else o["km"]
            if enyakin is None or o["deger"] < enyakin["deger"]:
                enyakin = o
        if canli and enyakin["kaynak"] == "yol":  # randevuya canliSaat'ten az: en yakın noktadan rota, İBB anlık hızıyla
            c = trafik.canli_rota_dk(yol.rota(enyakin["_n"], konum))
            if c and c["serbestDk"] > 0:
                enyakin.update(dk=c["dk"], carpan=round(c["dk"] / c["serbestDk"], 2), trafik="canlı")
                enyakin["deger"] = enyakin["dk"]
        enyakin.pop("_n", None)
        yakin = A["oncelikKm"] > 0 and konumlu and enyakin["km"] < A["oncelikKm"]
        ayni_ilce = bool(ilce) and sube_ilce(s) == ilce
        p = {"yakinlik": max(0.0, 1 - enyakin["deger"] / sifir),
             "yuk": max(0.0, 1 - len(benim) / sinir),
             "ciro": min(max((s.get("ciroHG", 100) - 100) / HG_TAVAN, 0), 1),
             "randevu": min(max((s.get("randevuHG", 100) - 100) / HG_TAVAN, 0), 1)}
        parca = {x: round(a[x] * p[x], 1) for x in a}
        puan = round(sum(parca.values()), 1)
        yol_yazi = (f"{_sayi(enyakin['km'])} km" + (f" · ~{round(enyakin['dk'])} dk" if enyakin["dk"] is not None else "")
                    + (" (kuş uçuşu)" if enyakin["kaynak"] == "kus" else ""))
        gerekce = f"{yol_yazi} ({enyakin['nereden']}) · {'bugün' if tarih == bugun() else 'o gün'} {len(benim)} çağrı · ciro/randevu H/G %{s.get('ciroHG')}/%{s.get('randevuHG')}"
        ayrinti = {"parca": parca, "km": enyakin["km"], "dk": enyakin["dk"], "carpan": enyakin["carpan"], "trafik": enyakin["trafik"], "kaynak": enyakin["kaynak"], "cagri": len(benim),
                   "nereden": enyakin["nereden"], "oncelik": yakin, "ayniIlce": ayni_ilce, "subeIlce": sube_ilce(s)}
        sonuc.append((puan, s, gerekce, enyakin["km"], ayrinti))
    return sorted(sonuc, key=lambda x: (not x[4]["ayniIlce"], not x[4]["oncelik"], -x[0]))


GUN_AD = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
AY_AD = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
RANDEVU_BAS, RANDEVU_SON = 10 * 60, 20 * 60  # önerilebilen saat aralığı (web formundaki gibi 10:00–20:00)


def oneri_bul(veri, k):
    """İlçede o an uygun SPY yoksa müşteriye önerilecek ilk randevu: bugünden 7 gün içinde, 30 dakikalık adımlarla, ilçedeki bir SPY'nin
    ileri-saat kurallarına (günlük sınır, randevu arası boşluk) uyduğu ilk saat. Döner: {"tarih","saat","gunYazi","repId","repAd"} ya da None."""
    haric = set(k.get("eskiRepler", []))
    aralik = ayar(veri)["aralikDk"]
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
                and abs(dakika(y["oneri"].get("saat")) - dk) < aralik for y in veri["kayitlar"].values())]
            if liste:
                gun = "Bugün" if tarih == bugun() else f"{yerel.tm_mday} {AY_AD[yerel.tm_mon - 1]} {GUN_AD[yerel.tm_wday]}"
                return {"tarih": tarih, "saat": k2["saat"], "gunYazi": gun, "repId": liste[0][1]["id"], "repAd": liste[0][1]["ad"]}
        t += adim
    return None


def varis_dk(bas, konum):
    """Şimdi yola çıkan SPY'nin varış süresi (dk): rota + İBB anlık hızı; olmazsa yol süresi × tipik çarpan; o da yoksa kuş uçuşu."""
    c = trafik.canli_rota_dk(yol.rota(bas, konum))
    if c:
        return c["dk"]
    o = yol.olc([bas], konum)[0]
    gun, saat = trafik.gun_saat()
    return round(o["dk"] * trafik.carpan(bas, konum, gun, saat), 1)


def _siralama_yaz(veri, k, liste, elenen):
    """Takip sayfasındaki "Atama seçenekleri" bölümü için: bu çağrıda adaylar puan dökümüyle, elenenler gerekçesiyle."""
    k["siralama"] = {"t": simdi(), **siralama_ozet(veri, k, liste, elenen)}


def siralama_ozet(veri, k, liste, elenen):
    A = ayar(veri)
    hemen = hemen_mi(k)
    return {"uzaklik": A["uzaklik"], "agirlik": A["agirlik"], "hemen": hemen, "oncelikKm": A["oncelikKm"],
            "subeden": not hemen and kalan_dk(k) >= A["subeSaat"] * 60, "subeSaat": A["subeSaat"], "canli": A["uzaklik"] == "trafikli" and A["canliSaat"] > 0 and kalan_dk(k) < A["canliSaat"] * 60, "canliSaat": A["canliSaat"],
            "adaylar": [{"id": s["id"], "ad": s["ad"], "puan": p, "gerekce": g, **ay} for p, s, g, _, ay in liste], "elenen": elenen}


ILETIM_BEKLEME_SN = 4  # çağrı geldikten sonra SPY'ye iletilene kadar (sunumda "alındı" aşaması görünsün)


def teklif_et(veri, k, neden=""):
    """Çağrıyı sıradaki en yüksek puanlı SPY'ye teklif eder; uygun kimse kalmadıysa "kimse almadı" (haritada kırmızı)."""
    k.pop("teklifZamani", None)
    t = k.setdefault("teklif", {"denenen": []})
    elenen = []
    liste = adaylar(veri, k, set(t["denenen"]) | set(k.get("eskiRepler", [])), elenen)
    _siralama_yaz(veri, k, liste, elenen)
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
    puan, spy, gerekce, uzak, ayrinti = liste[0]
    k.pop("oneri", None)  # uygun SPY çıktı: öneri geçersiz, çağrı doğrudan teklif edilir
    if k.get("repId") and k["repId"] != spy["id"]:
        k["eskiRepler"] = sorted(set(k.get("eskiRepler", [])) | {k["repId"]})
    t["denenen"].append(spy["id"])
    t["bitis"] = simdi() + KABUL_SN * 1000
    k.update({"repId": spy["id"], "sahipsiz": False, "durum": "alindi", "atanma": simdi(), "uzaklikKm": uzak, "varisDk": ayrinti["dk"],
              "atamaPuan": puan, "gerekce": gerekce})
    olay(veri, f"{ad} ({k.get('yer') or ''}) → {spy['ad']} · puan {_sayi(puan)} · {gerekce}{neden}", k["id"])
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
    elenen = []
    liste = adaylar(veri, k, set(k.get("eskiRepler", [])), elenen)
    if liste and k.get("repId") == liste[0][1]["id"] and not k.get("sahipsiz"):
        puan, _, gerekce, uzak, ayrinti = liste[0]
        _siralama_yaz(veri, k, liste, elenen)
        k.update({"uzaklikKm": uzak, "varisDk": ayrinti["dk"], "atamaPuan": puan, "gerekce": gerekce})
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
        elif (k.get("durum") == "alindi" and k.get("sahipsiz") and not k.get("bolgeDisi")
              and adaylar(veri, k, set(t.get("denenen", [])) | set(k.get("eskiRepler", [])), olc=False)):
            teklif_et(veri, k, " (yeni uygun SPY)")
            damga(veri, k)
            degisti = True
    return degisti
