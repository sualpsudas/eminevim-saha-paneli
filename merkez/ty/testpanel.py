"""TEST PANELİ KAPISI — yöneticinin çok kişili testi izlemesi ve hızlı yanıt vermesi (takip sayfasındaki "Test paneli").

Katılımcı = bir cihazın aldığı müşteri ya da personel kimliği (veri["kimlikler"]). Panel yalnız yöneticinin takip sayfasında görünür.
Hızlı yanıtlar mevcut çağrı akışını kullanır (durum değişir, müşteriye bildirim gider); her bildirim veri["bildirimGunlugu"]'na yazılır.
"""
from . import bildirim
from .ayarlar import DURUM_AD, KAPALI_DURUMLAR
from .yardim import damga, metin, olay, simdi, tel_temiz


def son_kayit(veri, tel):
    liste = [k for k in veri["kayitlar"].values() if tel_temiz((k.get("musteri") or {}).get("tel")) == tel]
    return max(liste, key=lambda k: k.get("olusma", 0)) if liste else None


def katilimcilar(veri, gorulme):
    abone = list(bildirim.abone_oku().values())
    liste = []
    for anahtar, kim in veri.get("kimlikler", {}).items():
        if anahtar.startswith("spy:"):
            s = veri["spyler"].get(anahtar[4:])
            if not s:
                continue
            liste.append({"anahtar": anahtar, "tur": "personel", "ad": s["ad"], "kimlik": s.get("yer", ""), "alinma": kim.get("tarih", 0),
                          "sonGorulme": max(gorulme.get(s["id"], 0), s.get("sonGorulme", 0)),
                          "bildirim": sum(1 for x in abone if x.get("spy") == s["id"]),
                          "adim": "Müsait" if s.get("durum") == "musait" else "Molada", "cizelge": []})
            continue
        m = veri["musteriler"].get(anahtar)
        if not m:
            continue
        k = son_kayit(veri, anahtar)
        idler = {x["id"] for x in veri["kayitlar"].values() if tel_temiz((x.get("musteri") or {}).get("tel")) == anahtar}
        liste.append({"anahtar": "tel:" + anahtar, "tur": "musteri", "ad": m.get("ad", ""), "kimlik": "0" + anahtar, "alinma": kim.get("tarih", 0),
                      "sonGorulme": max(m.get("sonGiris", 0), kim.get("tarih", 0)),
                      "bildirim": sum(1 for x in abone if x.get("musteri") == anahtar),
                      "adim": str(DURUM_AD.get(k.get("durum"), k.get("durum"))).capitalize() if k else "Giriş yaptı, çağrı yok",
                      "cizelge": [{"t": o["t"], "metin": o["metin"]} for o in veri["olaylar"] if o.get("id") in idler][:8]})
    return sorted(liste, key=lambda x: (x["tur"], x["ad"]))


def adlandir(veri, kim):
    tur, _, ad = kim.partition(":")
    if tur == "spy":
        return (veri["spyler"].get(ad) or {}).get("ad", ad)
    return (veri["musteriler"].get(ad) or {}).get("ad") or "0" + ad


def test_durum(veri, gorulme):
    return {"simdi": simdi(), "katilimcilar": katilimcilar(veri, gorulme),
            "spyler": [{"id": s["id"], "ad": s["ad"]} for s in veri["spyler"].values()],
            "gunluk": [{**g, "ad": adlandir(veri, g["kim"])} for g in veri.get("bildirimGunlugu", [])[:60]]}


def haber(veri, kim, baslik, govde, rid=""):
    """Tek kişiye bildirim (günlüğe yazılır). Döner: telefon sayısı."""
    tur, _, ad = kim.partition(":")
    hedefler = [x for x in bildirim.abone_oku().values() if x.get(tur) == ad]
    if not hedefler or not bildirim.gonderilebilir():
        bildirim.gunluk_yaz(veri, kim, {"baslik": baslik, "govde": govde}, "bildirim açık değil" if not hedefler else "bildirim servisi kapalı")
        return 0
    bildirim.gonder_arka_planda(hedefler, {"baslik": baslik, "govde": govde, "etiket": "t-" + (rid or ad), "rid": rid}, kim)
    return len(hedefler)


def acik_cagri(veri, tel):
    k = son_kayit(veri, tel)
    return k if k and k.get("durum") not in KAPALI_DURUMLAR else None


def yanit(veri, istek):
    tur, hedef = istek.get("tur"), str(istek.get("hedef") or "")
    anahtarlar = [a for a in veri.get("kimlikler", {}) if hedef in ("hepsi", a if a.startswith("spy:") else "tel:" + a)]
    if tur in ("onayla", "ata", "kabul", "iptal"):  # çağrı işlemleri yalnız müşterilere
        anahtarlar = [a for a in anahtarlar if not a.startswith("spy:")]
    if not anahtarlar:
        raise ValueError("Bu kişi artık listede yok.")
    ozet = []
    for a in anahtarlar:
        kim = a if a.startswith("spy:") else "musteri:" + a
        ad = adlandir(veri, kim)
        k = None if a.startswith("spy:") else acik_cagri(veri, a)
        if tur == "bildirim":
            n = haber(veri, kim, "Test bildirimi", "Bu bir deneme bildirimidir; görüyorsanız bildirimler çalışıyor.")
        elif tur == "mesaj":
            yazi = metin(istek.get("metin"), 200)
            if not yazi:
                raise ValueError("Mesajı yazın.")
            n = haber(veri, kim, "Yönetimden mesaj", yazi, k["id"] if k else "")
        elif not k:
            ozet.append(f"{ad}: açık çağrısı yok")
            continue
        elif tur == "onayla":
            if k["durum"] == "atandi":
                k["durum"] = "netlesti"
                olay(veri, f"{ad}: {DURUM_AD['netlesti']} (yönetici)", k["id"])
                damga(veri, k)
            n = haber(veri, kim, "Randevunuz onaylandı", "Randevunuzu görmek için dokunun.", k["id"])
        elif tur in ("ata", "kabul"):
            spy = veri["spyler"].get(metin(istek.get("spy"), 40) if tur == "ata" else k.get("repId"))
            if not spy:
                ozet.append(f"{ad}: SPY seçilmedi")
                continue
            k.update({"repId": spy["id"], "durum": "atandi"})
            (k.get("teklif") or {})["bitis"] = 0
            olay(veri, f"{ad}: {DURUM_AD['atandi']} ({spy['ad']}, yönetici)", k["id"])
            damga(veri, k)
            n = haber(veri, kim, f"Temsilciniz belli oldu: {spy['ad']}", "Randevunuzu görmek için dokunun.", k["id"])
        elif tur == "iptal":
            k["durum"] = "iptal"
            olay(veri, f"{ad}: {DURUM_AD['iptal']} (yönetici)", k["id"])
            damga(veri, k)
            n = haber(veri, kim, "Randevunuz iptal edildi", "Ayrıntı için dokunun.", k["id"])
        else:
            raise ValueError("İşlem bilinmiyor.")
        ozet.append(f"{ad}: " + (f"{n} telefona gitti" if n else "bildirim açık değil"))
    return {"ozet": ozet}


def birak(veri, anahtar):
    """Kimliği serbest bırakır; müşteride oturum jetonları da silinir (cihaz bir sonraki açılışta girişe döner)."""
    if anahtar.startswith("tel:"):
        anahtar = anahtar[4:]
        if anahtar in veri["musteriler"]:
            veri["musteriler"][anahtar]["jetonlar"] = []
        kim = "musteri:" + anahtar
    else:
        kim = anahtar
    veri.setdefault("kimlikler", {}).pop(anahtar, None)
    olay(veri, f"Test kimliği serbest bırakıldı: {adlandir(veri, kim)}")
    return {}


def test_islem(veri, istek):
    islem = istek.get("islem")
    if islem == "yanit":
        return yanit(veri, istek)
    if islem == "birak":
        return birak(veri, str(istek.get("anahtar") or ""))
    raise ValueError("İşlem bilinmiyor.")
