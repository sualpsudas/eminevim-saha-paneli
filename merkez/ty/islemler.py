"""İSTEK KURALLARI — uygulamadan gelen her yazma isteği burada işlenir (api.py çağırır, kilit altında).

  api/cagri    müşteri temsilci çağırdı → kayıt + atama
  api/kayit    çağrı güncellendi (SPY kabul etti, yola çıktı, görüşme bitti, iptal ...)
  api/mesaj    müşteri ↔ SPY mesajı
  api/spy      SPY müsait / molada (ve "uygulaması açık" sinyali)
  api/aktar    SPY "Devret" dedi → sıradaki SPY
  api/konum    SPY'nin canlı konumu (konum.py; canlı takip devreye alınınca)
  api/kod      web formundan gelen müşterinin giriş kodu
  api/musteri  müşteri hesabı (musteri.py)
  api/sifirla  test verisini sıfırla
Okuma (api/durum) için özetler de burada: spy_ozet, bugun_sayilar.
"""
import json
import secrets
import time

from . import aktarim, bildirim
from .atama import randevuda_mi, teklif_et
from .ayarlar import DURUM_AD, KAPALI_DURUMLAR, YEDEK
from .depo import bos_veri
from .konum import anlik_konum, canli_konum, konum_yaz
from .musteri import KODLAR, musteri_islem
from .personel import SPY_IDLER
from .yardim import bugun, damga, metin, olay, saat_yaz, simdi, tel_temiz

GORULME = {}  # SPY id -> son yoklama zamanı (yalnız bellekte)
YOLLAR = ("api/cagri", "api/kayit", "api/mesaj", "api/spy", "api/aktar", "api/konum", "api/kod", "api/musteri", "api/sifirla")


def temiz_kayit(gelen):
    if not isinstance(gelen, dict) or not gelen.get("id"):
        raise ValueError("Kayıt eksik.")
    k = {a: d for a, d in gelen.items() if a not in ("mesajlar", "surum", "guncelleme", "musteri", "eskiRepler", "olusma", "atanma", "uzaklikKm")}
    if len(json.dumps(k, ensure_ascii=False)) > 20000:
        raise ValueError("Kayıt çok büyük.")
    return k


def cagri(veri, istek):
    k = temiz_kayit(istek.get("kayit"))
    web = istek.get("kaynak") == "web" or k.get("kaynak") == "web"
    if web and istek.get("konumRiza") is not True:
        raise ValueError("Temsilci çağırmak için konum onayı verin.")
    k.pop("konumRizaTarih", None)
    konum = k.get("konum") or {}
    if not isinstance(konum.get("lat"), (int, float)) or not isinstance(konum.get("lng"), (int, float)):
        raise ValueError("Konum eksik.")
    m = istek.get("musteri") or {}
    k["musteri"] = {"ad": metin(m.get("ad"), 80), "tel": metin(m.get("tel"), 20), "ekBilgi": m.get("ekBilgi") if isinstance(m.get("ekBilgi"), dict) else None}
    k.update({"mesajlar": [], "olusma": simdi(), "repId": None, "teklif": {"denenen": []}})
    if web:
        k["kaynak"] = "web"
        k["konumRizaTarih"] = k["olusma"]
        k["girisKodu"] = f"{secrets.randbelow(900000) + 100000}"  # SMS yerine ekranda gösterilir (test)
    veri["kayitlar"][k["id"]] = k
    olay(veri, f"Yeni çağrı: {k['musteri']['ad'] or 'Müşteri'} ({k.get('yer') or ''}), {k.get('gunYazi') or k.get('tarih') or ''} {k.get('saat') or ''}", k["id"])
    teklif_et(veri, k)
    damga(veri, k)
    aktarim.yeni_cagri(k)
    return k


def kayit(veri, istek):
    k = temiz_kayit(istek.get("kayit"))
    for alan in ("teklif", "sahipsiz", "atamaPuan", "gerekce", "girisKodu", "konumRizaTarih"):
        k.pop(alan, None)  # bunları yalnız merkez yazar
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
    return konum_yaz(spy_id, istek.get("lat"), istek.get("lng"))


def giris_kodu(veri, istek):
    tel = tel_temiz(istek.get("tel"))
    kod = metin(istek.get("kod"), 6)
    for k in sorted(veri["kayitlar"].values(), key=lambda x: -x.get("olusma", 0)):
        if k.get("girisKodu") == kod and tel_temiz(k.get("musteri", {}).get("tel", "")) == tel:
            return k
    raise ValueError("Kod ya da telefon eşleşmedi.")


def sifirla(veri, istek):
    KODLAR.clear()
    if istek.get("onay") != "evet":
        raise ValueError("Onay eksik.")
    YEDEK.mkdir(exist_ok=True)
    (YEDEK / time.strftime("veri_%Y-%m-%d_%H%M%S.json")).write_text(json.dumps(veri, ensure_ascii=False), encoding="utf-8")
    surum = veri["surum"]
    veri.clear()
    veri.update(bos_veri())
    veri["surum"] = surum + 1
    veri["sifirlama"] = veri["surum"]  # cihazlar eski kayıtları bırakır, müşteri oturumları kapanır
    bildirim.musteri_abonelerini_sil()
    olay(veri, "Test verisi sıfırlandı")
    return {}


ISLEMLER = {"api/cagri": cagri, "api/kayit": kayit, "api/mesaj": mesaj, "api/spy": spy_durum, "api/aktar": aktar,
            "api/konum": konum, "api/kod": giris_kodu, "api/musteri": musteri_islem, "api/sifirla": sifirla}


def uygula(veri, yol, istek):
    if yol not in ISLEMLER:
        raise KeyError(yol)
    return ISLEMLER[yol](veri, istek)


def spy_ozet(veri, s):
    hal = "molada" if s.get("durum") == "molada" else "randevuda" if randevuda_mi(veri, s["id"]) else "bosta"
    bugunku = sum(1 for x in veri["kayitlar"].values() if x.get("repId") == s["id"] and x.get("tarih") == bugun() and x.get("durum") != "iptal")
    return {**s, "hal": hal, "konumAn": anlik_konum(veri, s), "canliKonum": bool(canli_konum(s["id"])), "bugunCagri": bugunku,
            "sonGorulme": GORULME.get(s["id"], 0), "bildirim": bildirim.bildirim_sayisi(s["id"])}


def bugun_sayilar(veri):
    """Gelen Çağrı: bugün merkeze gelen çağrı. Görüşme Sayısı: bugün kapıda doğrulanan (görüşmede ya da tamamlandı)."""
    gun = bugun()
    gelen = sum(1 for k in veri["kayitlar"].values() if time.strftime("%Y-%m-%d", time.localtime(k.get("olusma", 0) / 1000)) == gun)
    gorusme = sum(1 for k in veri["kayitlar"].values() if k.get("tarih") == gun and k.get("durum") in ("gorusmede", "tamamlandi"))
    return {"gelen": gelen, "gorusme": gorusme}
