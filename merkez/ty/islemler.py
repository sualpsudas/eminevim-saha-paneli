"""İSTEK KURALLARI — uygulamadan gelen her yazma isteği burada işlenir (api.py çağırır, kilit altında).

  api/cagri    müşteri temsilci çağırdı → kayıt + atama
  api/kayit    çağrı güncellendi (SPY kabul etti, yola çıktı, görüşme bitti, iptal ...)
  api/mesaj    müşteri ↔ SPY mesajı
  api/spy      SPY müsait / molada (ve "uygulaması açık" sinyali)
  api/aktar    SPY "Devret" dedi → sıradaki SPY
  api/konum    SPY'nin canlı konumu (konum.py; canlı takip devreye alınınca)
  api/kod      web formundan gelen müşterinin giriş kodu
  api/musteri  müşteri hesabı (musteri.py)
  api/dogrulama kapıda kimlik doğrulama: müşteriye kod, SPY okutur (dogrulama.py)
  api/sifirla  test verisini sıfırla (atama seçenekleri korunur)
  api/atama-ayar takip sayfasının "Atama seçenekleri" bölümü: oku / kaydet / varsayılana dön (atama.ayar_kaydet)
Okuma (api/durum) için özetler de burada: spy_ozet, bugun_sayilar.
"""
import json
import secrets
import time

from . import aktarim, bildirim, trafik
from .bolge import bolgede_mi
from .atama import ILETIM_BEKLEME_SN, adaylar, ayar, ayar_kaydet, hemen_mi, randevuda_mi, siralama_ozet, teklif_et, yeniden_ata
from .ayarlar import ATAMA_VARSAYILAN, DURUM_AD, KAPALI_DURUMLAR, UZAKLIK_TURLERI, YEDEK
from .depo import bos_veri
from .dogrulama import KAPI_KODLARI, dogrulama_islem
from . import gezi
from .konum import konum_sifirla, anlik_konum, canli_konum, konum_yaz, konum_ve_kaynak
from .musteri import KODLAR, hesap_ac, musteri_islem
from .personel import SPY_IDLER
from .sunum import ilerlet
from .yardim import bugun, damga, metin, olay, saat_yaz, simdi, tel_temiz

GORULME = {}  # SPY id -> son yoklama zamanı (yalnız bellekte)
YOLLAR = ("api/cagri", "api/kayit", "api/mesaj", "api/spy", "api/aktar", "api/konum", "api/kod", "api/musteri", "api/dogrulama", "api/sifirla", "api/kimlik", "api/ilerlet", "api/konum-tasi", "api/cagri-ekle", "api/oneri", "api/atama-ayar")


def temiz_kayit(gelen):
    if not isinstance(gelen, dict) or not gelen.get("id"):
        raise ValueError("Kayıt eksik.")
    k = {a: d for a, d in gelen.items() if a not in ("mesajlar", "surum", "guncelleme", "musteri", "eskiRepler", "olusma", "atanma", "uzaklikKm", "yolRota", "yolDk")}
    if len(json.dumps(k, ensure_ascii=False)) > 20000:
        raise ValueError("Kayıt çok büyük.")
    return k


def cagri(veri, istek):
    k = temiz_kayit(istek.get("kayit"))
    web = istek.get("kaynak") == "web" or k.get("kaynak") == "web"
    if web and istek.get("aydinlatmaOnay") is not True:
        raise ValueError("Aydınlatma Metni onaylanmadı. Formdaki kutuyu işaretleyip yeniden deneyin.")
    for alan in ("konumRizaTarih", "aydinlatmaTarih", "kampanya"):
        k.pop(alan, None)
    konum = k.get("konum") or {}
    if not isinstance(konum.get("lat"), (int, float)) or not isinstance(konum.get("lng"), (int, float)):
        raise ValueError("Konum eksik.")
    m = istek.get("musteri") or {}
    k["musteri"] = {"ad": metin(m.get("ad"), 80), "adi": metin(m.get("adi"), 40), "soyadi": metin(m.get("soyadi"), 40), "tel": metin(m.get("tel"), 20),
                    "ekBilgi": m.get("ekBilgi") if isinstance(m.get("ekBilgi"), dict) else None}
    k.update({"mesajlar": [], "olusma": simdi(), "repId": None, "teklif": {"denenen": []}})
    if web:
        k["kaynak"] = "web"
        k["aydinlatmaTarih"] = k["olusma"]  # müşteri formda "Aydınlatma Metni'ni okudum" kutusunu işaretledi (açık rıza değil)
        k["kampanya"] = istek.get("kampanya") is True  # isteğe bağlı ticari elektronik ileti izni
        k["girisKodu"] = f"{secrets.randbelow(900000) + 100000}"  # SMS yerine ekranda gösterilir (test)
    veri["kayitlar"][k["id"]] = k
    olay(veri, f"Yeni çağrı: {k['musteri']['ad'] or 'Müşteri'} ({k.get('yer') or ''}), {k.get('gunYazi') or k.get('tarih') or ''} {k.get('saat') or ''}", k["id"])
    k.update({"durum": "alindi", "sahipsiz": False})
    k["teklifZamani"] = k["olusma"] + ILETIM_BEKLEME_SN * 1000  # çağrı önce "alındı"; iletim zamanını bekçi / durum yoklaması getirir
    damga(veri, k)
    aktarim.yeni_cagri(k)
    return k


def kayit(veri, istek):
    k = temiz_kayit(istek.get("kayit"))
    for alan in ("teklif", "sahipsiz", "atamaPuan", "gerekce", "girisKodu", "konumRizaTarih", "aydinlatmaTarih", "kampanya", "dogrulama", "dogrulandi"):
        k.pop(alan, None)  # bunları yalnız merkez yazar
    eski_durum = (veri["kayitlar"].get(k["id"]) or {}).get("durum")
    if k.get("durum") == "gorusmede" and eski_durum != "gorusmede":
        raise ValueError("Görüşme, kapıda QR ya da kod doğrulanınca başlar.")  # yalnız api/dogrulama başlatır
    if eski_durum == "gorusmede" and k.get("durum") in ("atandi", "netlesti", "yolda", "gorusme"):
        k["durum"] = "gorusmede"  # doğrulamadan önceki eski kopya görüşmeyi geri almasın
    eski = veri["kayitlar"].get(k["id"])
    if not eski:
        raise ValueError("Kayıt bulunamadı.")
    if eski.get("durum") == "alindi" and k.get("durum") == "atandi" and k.get("repId") not in (None, eski.get("repId")):
        raise ValueError("Bu çağrı artık size ait değil.")  # süre dolup başkasına geçtiyse eski SPY kabul edemez
    if eski.get("durum") == "alindi" and k.get("durum") not in (None, "alindi"):
        (eski.get("teklif") or {})["bitis"] = 0  # kabul edildi: süre durur
    if not k.get("repId") or k["repId"] not in SPY_IDLER:
        k["repId"] = eski.get("repId")  # müşteri tarafı kabulden önce SPY'yi görmez, boş gönderir
    if k.get("durum") != eski.get("durum"):
        spy = veri["spyler"].get(k.get("repId") or eski.get("repId"), {})
        olay(veri, f"{eski.get('musteri', {}).get('ad') or 'Müşteri'}: {DURUM_AD.get(k.get('durum'), k.get('durum'))} ({spy.get('ad', '')})", k["id"])
    if k.get("repId") != eski.get("repId"):
        k["eskiRepler"] = sorted((set(eski.get("eskiRepler", [])) | {eski.get("repId")}) - {None})
        olay(veri, f"{eski.get('musteri', {}).get('ad') or 'Müşteri'} çağrısı devredildi → {veri['spyler'].get(k.get('repId'), {}).get('ad', '')}", k["id"])
    onceki = eski.get("durum")
    eski.update(k)
    damga(veri, eski)
    spy_ad = veri["spyler"].get(eski.get("repId"), {}).get("ad", "")
    if onceki == "alindi" and eski.get("durum") == "atandi":
        zaman = " ".join(x for x in (eski.get("gunYazi") if eski.get("tarih") != bugun() else "", eski.get("saat")) if x)
        bildirim.bildir_musteri(eski, f"Temsilciniz belli oldu: {spy_ad}" + (f" · {zaman}" if zaman else ""), "Randevunuzu görmek için dokunun.")
    elif onceki != "yolda" and eski.get("durum") == "yolda":
        varis = saat_yaz(eski.get("varisZamani"))
        bildirim.bildir_musteri(eski, "Temsilciniz yola çıktı" + (f" · tahmini varış {varis}" if varis else ""), f"{spy_ad} size doğru geliyor.")
    aktarim.cagri_degisti(veri, eski, onceki)
    return eski


def mesaj(veri, istek):
    k = veri["kayitlar"].get(str(istek.get("id") or ""))
    yazi = metin(istek.get("text"))
    kimden = istek.get("from")
    if not k or not yazi or kimden not in ("musteri", "temsilci"):
        raise ValueError("Mesaj eksik.")
    mid = metin(istek.get("mid"), 64) or secrets.token_hex(6)
    if not any(x.get("mid") == mid for x in k["mesajlar"]):
        k["mesajlar"].append({"mid": mid, "from": kimden, "t": simdi(), "text": yazi})
        k["mesajlar"] = k["mesajlar"][-300:]
        damga(veri, k)
        if kimden == "temsilci" and not istek.get("oto"):  # kabul/yola çıkış mesajının bildirimi durumdan gider
            bildirim.bildir_musteri(k, "Temsilcinizden mesaj: " + veri["spyler"].get(k.get("repId"), {}).get("ad", ""), yazi[:120])
    return k


def spy_durum(veri, istek):
    s = veri["spyler"].get(str(istek.get("id") or ""))
    if not s:
        raise ValueError("SPY bulunamadı.")
    if istek.get("durum") in ("musait", "molada") and istek["durum"] != s["durum"]:
        s["durum"] = istek["durum"]
        olay(veri, f"{s['ad']}: {'Müsait' if s['durum'] == 'musait' else 'Molada'}")
        veri["surum"] += 1
    s["sonGorulme"] = simdi()
    return s


def aktar(veri, istek):  # SPY "Devret" dedi: sıradaki SPY'ye teklif (yönetici ataması yok)
    k = veri["kayitlar"].get(str(istek.get("id") or ""))
    if not k:
        raise ValueError("Çağrı bulunamadı.")
    if k.get("durum") not in KAPALI_DURUMLAR:
        k["durum"] = "alindi"
        teklif_et(veri, k, f" ({veri['spyler'].get(k.get('repId'), {}).get('ad', 'SPY')} devretti)")
        damga(veri, k)
    return k


def konum(veri, istek):
    """Canlı konum girişi: {id, lat, lng}. Veri dosyasına yazılmaz (yalnız bellekte; konum.py)."""
    spy_id = str(istek.get("id") or "")
    if spy_id not in SPY_IDLER:
        raise ValueError("SPY bulunamadı.")
    (veri.get("elleKonum") or {}).pop(spy_id, None)  # gerçek canlı konum gelince elle taşınan konum geçersiz
    return konum_yaz(spy_id, istek.get("lat"), istek.get("lng"))


ATANMIS = ("atandi", "netlesti", "yolda", "gorusme", "gorusmede")  # kabul edilmiş: konum artık taşınamaz


def _nokta(istek):
    lat, lng = istek.get("lat"), istek.get("lng")
    if not isinstance(lat, (int, float)) or not isinstance(lng, (int, float)) or not (-90 <= lat <= 90 and -180 <= lng <= 180):
        raise ValueError("Konum geçersiz.")
    return float(lat), float(lng)


def konum_tasi(veri, istek):
    """Yönetici takip sayfasında müşteriyi ya da SPY'yi sürükledi: {tur: musteri|spy, id, lat, lng}.
    Müşteri: çağrı henüz kabul edilmemişse (alındı / kimse almadı). SPY: üzerinde kabul edilmiş çağrı yoksa.
    Taşıma sonrası kabul edilmemiş çağrılar yeniden değerlendirilir (atama.yeniden_ata)."""
    tur, kid = istek.get("tur"), str(istek.get("id") or "")
    lat, lng = _nokta(istek)
    if tur == "musteri":
        k = veri["kayitlar"].get(kid)
        if not k:
            raise ValueError("Çağrı bulunamadı.")
        if k.get("durum") != "alindi":
            raise ValueError("Bu çağrıya temsilci atandı ya da çağrı kapandı; konumu değiştirilemez.")
        k["konum"] = {**(k.get("konum") or {}), "lat": lat, "lng": lng}
        ad = (k.get("musteri") or {}).get("ad") or "Müşteri"
        if not bolgede_mi(lat, lng):  # pilot bölge dışı: temsilci gidemez, telefonla görüşme (çağrı kimse almadı gibi bekler)
            if k.get("repId"):
                k["eskiRepler"] = sorted(set(k.get("eskiRepler", [])) | {k["repId"]})
            k.update({"repId": None, "sahipsiz": True, "bolgeDisi": True, "gerekce": "", "teklifZamani": None})
            k.setdefault("teklif", {"denenen": []})["bitis"] = 0
            olay(veri, f"{ad}: pilot bölge dışına taşındı → temsilci gönderilmez, telefonla görüşülür", kid)
            damga(veri, k)
            return k
        if k.pop("bolgeDisi", None):  # bölgeye geri döndü: baştan teklif edilir
            k["eskiRepler"] = []
            k["teklif"] = {"denenen": []}
            teklif_et(veri, k, " (pilot bölgeye döndü)")
            damga(veri, k)
            return k
        damga(veri, k)
        yeniden_ata(veri, k, " (müşteri konumu değişti)")
        return k
    if tur == "spy":
        s = veri["spyler"].get(kid)
        if not s:
            raise ValueError("SPY bulunamadı.")
        if any(x.get("repId") == kid and x.get("durum") in ATANMIS for x in veri["kayitlar"].values()):
            raise ValueError("Bu SPY'ye kabul ettiği bir çağrı atanmış; konumu değiştirilemez.")
        if not bolgede_mi(lat, lng):
            raise ValueError("SPY pilot bölge (Üsküdar, Ümraniye, Ataşehir) dışına taşınamaz.")
        veri.setdefault("elleKonum", {})[kid] = {"lat": lat, "lng": lng}
        veri["surum"] += 1
        for k in list(veri["kayitlar"].values()):
            yeniden_ata(veri, k, f" ({s['ad']} konumu değişti)")
        return {"id": kid}
    raise ValueError("Tür bilinmiyor.")


def cagri_ekle(veri, istek):
    """Yönetici takip sayfasında haritaya tıklayıp çağrı ekledi: {ad, yer, tel, lat, lng}. Gerçek çağrı gibi kaydedilir (test sıfırlanana kadar)."""
    lat, lng = _nokta(istek)
    if not bolgede_mi(lat, lng):
        raise ValueError("Bu nokta pilot bölge (Üsküdar, Ümraniye, Ataşehir) dışında; çağrı eklenemez.")
    k = {"id": "y-" + secrets.token_hex(5), "konum": {"lat": lat, "lng": lng}, "yer": metin(istek.get("yer"), 120) or "Haritada seçilen nokta",
         "tarih": bugun(), "saat": time.strftime("%H:%M"), "gunYazi": "Bugün", "kaynak": "yonetici"}
    ad, tel = metin(istek.get("ad"), 80) or "Test müşterisi", tel_temiz(istek.get("tel"))
    adi, _, soyadi = ad.partition(" ")
    if len(tel) == 10 and tel not in veri["musteriler"]:  # KVKK/Aydınlatma adımları geçmiş yeni üye: uygulamada giriş listesinde görünür, randevu oradan yanıtlanır
        hesap_ac(veri, tel, adi, soyadi, False, "yonetici")
    return cagri(veri, {"kayit": k, "musteri": {"ad": ad, "adi": adi, "soyadi": soyadi, "tel": tel}})


def oneri_islem(veri, istek):
    """Müşteri, ilçede uygun SPY olmadığında önerilen randevuya yanıt verdi: {id, karar: kabul|red}.
    kabul: çağrı önerilen gün/saate alınır ve o saate uygun SPY'ye teklif edilir. red: öneri kalkar, çağrı "kimse almadı" olarak bekler (müşteri başka saat seçer)."""
    k = veri["kayitlar"].get(str(istek.get("id") or ""))
    if not k or not k.get("oneri") or k.get("durum") != "alindi":
        raise ValueError("Bekleyen bir randevu önerisi yok.")
    o = k.pop("oneri")
    ad = (k.get("musteri") or {}).get("ad") or "Müşteri"
    k["oneriYok"] = True  # bir daha otomatik öneri üretilmez
    if istek.get("karar") == "kabul":
        k.update({"tarih": o["tarih"], "saat": o["saat"], "gunYazi": o["gunYazi"], "oneriKabul": True, "sahipsiz": False, "repId": None, "teklif": {"denenen": []}})
        olay(veri, f"{ad}: önerilen randevuyu kabul etti → {o['gunYazi']} {o['saat']}", k["id"])
        teklif_et(veri, k, " (önerilen randevu)")
    else:
        olay(veri, f"{ad}: önerilen randevuyu kabul etmedi, başka saat seçecek", k["id"])
    damga(veri, k)
    return k


def giris_kodu(veri, istek):
    tel = tel_temiz(istek.get("tel"))
    kod = metin(istek.get("kod"), 6)
    for k in sorted(veri["kayitlar"].values(), key=lambda x: -x.get("olusma", 0)):
        if k.get("girisKodu") == kod and tel_temiz(k.get("musteri", {}).get("tel", "")) == tel:
            return k
    raise ValueError("Kod ya da telefon eşleşmedi.")


def kimlik(veri, istek):
    """Test aşaması: personel kimliği (SPY) aynı anda tek cihazda kullanılır. islem: bos | al | birak.
    veri["kimlikler"]["spy:<id>"] = {cihaz, tarih}; müşteri kimlikleri musteri.py'de aynı sözlükte tutulur."""
    islem, cihaz = istek.get("islem"), metin(istek.get("cihaz"), 64)
    kim = veri.setdefault("kimlikler", {})
    if islem == "bos":  # başka cihazın aldığı personel kimlikleri (giriş listesinden çıkarılır)
        return {"dolu": [a[4:] for a, k in kim.items() if a.startswith("spy:") and k.get("cihaz") != cihaz]}
    spy = metin(istek.get("spy"), 40)
    if spy not in veri["spyler"]:
        raise ValueError("SPY bulunamadı.")
    kullanan = (kim.get("spy:" + spy) or {}).get("cihaz")
    if islem == "al":
        if kullanan not in (None, cihaz):
            raise ValueError("Bu personel kimliği başka bir cihazda kullanımda. Boş bir kimlik seçin.")
        kim["spy:" + spy] = {"cihaz": cihaz, "tarih": simdi()}
        return {}
    if islem == "birak":
        if kullanan in (None, cihaz):
            kim.pop("spy:" + spy, None)
        return {}
    raise ValueError("İşlem bilinmiyor.")


def sifirla(veri, istek):
    KODLAR.clear()
    KAPI_KODLARI.clear()
    if istek.get("onay") != "evet":
        raise ValueError("Onay eksik.")
    YEDEK.mkdir(exist_ok=True)
    (YEDEK / time.strftime("veri_%Y-%m-%d_%H%M%S.json")).write_text(json.dumps(veri, ensure_ascii=False), encoding="utf-8")
    surum, eski_ayar = veri["surum"], veri.get("atamaAyar")
    veri.clear()
    veri.update(bos_veri())
    if eski_ayar:
        veri["atamaAyar"] = eski_ayar
    veri["surum"] = surum + 1
    konum_sifirla()
    veri["sifirlama"] = veri["surum"]  # cihazlar eski kayıtları bırakır, müşteri oturumları kapanır
    bildirim.musteri_abonelerini_sil()
    olay(veri, "Test verisi sıfırlandı")
    return {}


def atama_ayar(veri, istek):
    islem = istek.get("islem") or "oku"
    if islem == "kaydet":
        a = ayar_kaydet(veri, istek.get("ayar") or {"bos": 1})
        olay(veri, "Atama seçenekleri değişti: " + atama_ozet(a))
    elif islem == "varsayilan":
        a = ayar_kaydet(veri, None)
        olay(veri, "Atama seçenekleri varsayılana döndü: " + atama_ozet(a))
    elif islem == "dene":  # seçili çağrı şimdiki seçeneklerle nasıl sıralanırdı (hiçbir şey değişmez)
        k = veri["kayitlar"][istek["id"]]
        elenen = []
        liste = adaylar(veri, k, (), elenen)
        return {"id": k["id"], **siralama_ozet(veri, k, liste, elenen)}
    else:
        a = ayar(veri)
    return {"ayar": a, "varsayilan": ATAMA_VARSAYILAN, "turler": UZAKLIK_TURLERI, "trafik": trafik.bilgi()}


def _sayi(x):
    return f"{x:g}".replace(".", ",")


def atama_ozet(a):
    g = a["agirlik"]
    km_yazi = f"{_sayi(a['oncelikKm'])} km altı önce" if a["oncelikKm"] else "km önceliği kapalı"
    return (f"yakınlık {g['yakinlik']}, çağrı sayısı {g['yuk']}, ciro H/G {g['ciro']}, randevu H/G {g['randevu']} · {UZAKLIK_TURLERI[a['uzaklik']]}"
            f" · {km_yazi} · {a['subeSaat']} saat ve sonrası şubeden · {a['canliSaat']} saatten yakın randevuda anlık trafik · günlük en fazla {a['gunlukSinir']} · randevu arası {a['aralikDk']} dk"
            f" · ilçe önceliği {'açık' if a['ilceOnceligi'] else 'kapalı'}")


ISLEMLER = {"api/cagri": cagri, "api/kayit": kayit, "api/mesaj": mesaj, "api/spy": spy_durum, "api/aktar": aktar,
            "api/konum": konum, "api/kod": giris_kodu, "api/musteri": musteri_islem, "api/dogrulama": dogrulama_islem, "api/sifirla": sifirla, "api/kimlik": kimlik, "api/ilerlet": ilerlet,
            "api/konum-tasi": konum_tasi, "api/cagri-ekle": cagri_ekle, "api/oneri": oneri_islem, "api/atama-ayar": atama_ayar}


def uygula(veri, yol, istek):
    if yol not in ISLEMLER:
        raise KeyError(yol)
    return ISLEMLER[yol](veri, istek)


def spy_ozet(veri, s):
    hal = "molada" if s.get("durum") == "molada" else "randevuda" if randevuda_mi(veri, s["id"]) else "bosta"
    bugunku = sum(1 for x in veri["kayitlar"].values() if x.get("repId") == s["id"] and x.get("tarih") == bugun() and x.get("durum") != "iptal")
    konum_, kaynak = konum_ve_kaynak(veri, s)
    return {**s, "hal": hal, "konumAn": konum_, "geziyor": kaynak == "gezi", "geziRota": gezi.ozet(s["id"]) if kaynak == "gezi" else None, "canliKonum": bool(canli_konum(s["id"])), "bugunCagri": bugunku,
            "sonGorulme": GORULME.get(s["id"], 0), "bildirim": bildirim.bildirim_sayisi(s["id"])}


def bugun_sayilar(veri):
    """Gelen Çağrı: bugün merkeze gelen çağrı. Görüşme Sayısı: bugün kapıda doğrulanan (görüşmede ya da tamamlandı)."""
    gun = bugun()
    gelen = sum(1 for k in veri["kayitlar"].values() if time.strftime("%Y-%m-%d", time.localtime(k.get("olusma", 0) / 1000)) == gun)
    gorusme = sum(1 for k in veri["kayitlar"].values() if k.get("tarih") == gun and k.get("durum") in ("gorusmede", "tamamlandi"))
    return {"gelen": gelen, "gorusme": gorusme}
