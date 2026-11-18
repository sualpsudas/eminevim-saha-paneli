"""MÜŞTERİ HESABI KAPISI — telefon + parola (her telefonda aynı), SMS kodu, oturum jetonu.

Şu an hesaplar depoda (veri["musteriler"]); SMS gönderilmez, kod yanıtta döner ve ekranda gösterilir (test).
Gerçek sistemde: hesaplar Eminevim üye sistemine, kod_gonder() SMS servisine bağlanır (IT_DEVIR.md → Müşteri hesabı).
Parolanın kendisi saklanmaz (PBKDF2 özeti).
"""
import hashlib
import hmac
import secrets

from .ayarlar import DEMO_PAROLA, HATA_SINIR, KILIT_DK, KOD_DK, PAROLA_TUR
from .yardim import metin, olay, simdi, tel_temiz

KODLAR = {}  # tel -> {"kod", "bitis", "hata"} (yalnız bellekte)


def parola_ozet(parola, tuz=None):
    tuz = tuz or secrets.token_hex(16)
    return tuz, hashlib.pbkdf2_hmac("sha256", parola.encode("utf-8"), bytes.fromhex(tuz), PAROLA_TUR).hex()


AYSE_TEL = "5321456789"  # gösteri hesabı (Ayşe Kaya, parola test123); sıfırlamada yeniden kurulur
_t, _o = parola_ozet(DEMO_PAROLA)
AYSE = {"ad": "Ayşe Kaya", "tuz": _t, "ozet": _o, "kvkkTarih": 0, "olusma": 0}
# Örnek müşteriler (uygulamadaki uygulama/ornek-veri.js → ORNEK_MUSTERILER ile aynı; hepsi parola test123). Eksikse her okumada eklenir.
ORNEK_MUSTERILER = {AYSE_TEL: AYSE, **{tel: {**AYSE, "ad": ad} for tel, ad in [
    ("5332103456", "Zeynep Arslan"), ("5353204567", "Can Öztürk"), ("5414305678", "Elif Yıldız"), ("5436507890", "Burak Şahin")]}}


def kod_gonder(tel):
    """SMS kodu üretir. Gerçek SMS servisi bağlanınca kod burada gönderilir ve yanıtta DÖNMEZ."""
    kod = f"{secrets.randbelow(900000) + 100000}"
    KODLAR[tel] = {"kod": kod, "bitis": simdi() + KOD_DK * 60000, "hata": 0}
    return kod


def musteri_kayitlari(veri, tel):
    """Müşterinin merkezdeki çağrıları (en yenisi önde); giriş yapılan her telefonda Randevularım bunlarla dolar."""
    liste = [k for k in veri["kayitlar"].values() if tel_temiz((k.get("musteri") or {}).get("tel")) == tel]
    return [{a: d for a, d in k.items() if a not in ("girisKodu", "konumRizaTarih")} for k in sorted(liste, key=lambda x: -x.get("olusma", 0))]


def kod_dogru(tel, kod, harca=False):
    k = KODLAR.get(tel)
    if not k or k["bitis"] < simdi():
        raise ValueError("Kodun süresi doldu. “Kodu tekrar gönder”e dokunun.")
    if not hmac.compare_digest(k["kod"], metin(kod, 6)):
        k["hata"] += 1
        if k["hata"] >= HATA_SINIR:
            KODLAR.pop(tel, None)  # tahminle denemeye karşı: kod geçersiz olur
        raise ValueError("Kod eşleşmedi. SMS'teki 6 haneli kodu girin.")
    if harca:
        KODLAR.pop(tel, None)


def parola_gecerli(parola):
    parola = str(parola or "")
    if len(parola) < 6 or len(parola) > 128:
        raise ValueError("Parola en az 6 karakter olmalı.")
    return parola


def jeton_ozet(jeton):
    return hashlib.sha256(str(jeton or "").encode()).hexdigest()


def oturum(veri, tel, jeton=None):
    """Girişte dönen hesap + çağrılar. Jeton bu telefonun oturumudur: uygulama kapanıp açılınca parolasız devam
    (Çıkış yap'a kadar) ve bildirim aboneliği (müşteri adına abone olmayı kanıtlar). Telefonda parola saklanmaz."""
    m = veri["musteriler"][tel]
    if not jeton:
        jeton = secrets.token_urlsafe(24)
        m["jetonlar"] = (m.get("jetonlar", []) + [jeton_ozet(jeton)])[-10:]
    return {"tel": tel, "ad": m["ad"], "kvkkTarih": m.get("kvkkTarih", 0), "jeton": jeton, "kayitlar": musteri_kayitlari(veri, tel)}


class YazilanHata(ValueError):
    """Hata yanıtı döner ama veri yine kaydedilir (yanlış parola sayacı)."""


def musteri_islem(veri, istek):
    """islem: sorgu | kod | kodkontrol | kayit | giris | yenile | web | oturum | cikis. Hesap merkezde; her telefonda aynı parola."""
    islem, tel = istek.get("islem"), tel_temiz(istek.get("tel"))
    if len(tel) != 10:
        raise ValueError("Telefon numaranızı 10 hane olarak yazın.")
    hesaplar = veri["musteriler"]
    m = hesaplar.get(tel)
    if islem == "sorgu":
        return {"kayitli": bool(m)}
    if islem == "kod":  # gerçek SMS gelene kadar kod yanıtta döner ve ekranda gösterilir (test)
        return {"kod": kod_gonder(tel), "kayitli": bool(m)}
    if islem == "kodkontrol":
        kod_dogru(tel, istek.get("kod"))
        return {"kayitli": bool(m)}
    if islem in ("oturum", "cikis"):  # uygulama yeniden açıldı / Çıkış yap
        jeton = str(istek.get("jeton") or "")
        if not m or jeton_ozet(jeton) not in m.get("jetonlar", []):
            raise ValueError("Oturum doğrulanamadı. Yeniden giriş yapın.")
        if islem == "cikis":
            m["jetonlar"].remove(jeton_ozet(jeton))
            return {}
        return oturum(veri, tel, jeton)
    if islem == "giris":
        if not m:
            raise ValueError("Bu numarayla kayıt yok.")
        if m.get("kilitBitis", 0) > simdi():
            raise ValueError(f"Çok fazla hatalı deneme. {KILIT_DK} dakika sonra tekrar deneyin ya da “Parolamı unuttum”a dokunun.")
        if not hmac.compare_digest(parola_ozet(str(istek.get("parola") or ""), m["tuz"])[1], m["ozet"]):
            m["hata"] = m.get("hata", 0) + 1
            if m["hata"] >= HATA_SINIR:
                m.update({"hata": 0, "kilitBitis": simdi() + KILIT_DK * 60000})
            raise YazilanHata("Parola eşleşmedi.")
        m.update({"hata": 0, "kilitBitis": 0, "sonGiris": simdi()})
        return oturum(veri, tel)
    parola = parola_gecerli(istek.get("parola"))
    if islem == "kayit":  # yeni müşteri: SMS kodu + ad soyad + parola + KVKK onayı
        if m:
            raise ValueError("Bu numara kayıtlı. Parolanızla giriş yapın.")
        ad = metin(istek.get("ad"), 80)
        if len(ad) < 3:
            raise ValueError("Adınızı ve soyadınızı yazın.")
        if istek.get("kvkk") is not True:
            raise ValueError("Kişisel veri onayı eksik.")
        kod_dogru(tel, istek.get("kod"), harca=True)
        tuz, ozet = parola_ozet(parola)
        hesaplar[tel] = {"ad": ad, "tuz": tuz, "ozet": ozet, "kvkkTarih": simdi(), "olusma": simdi()}
        olay(veri, f"Yeni müşteri hesabı: {ad}")
        return oturum(veri, tel)
    if islem == "yenile":  # parolamı unuttum: SMS kodu + yeni parola
        if not m:
            raise ValueError("Bu numarayla kayıt yok.")
        kod_dogru(tel, istek.get("kod"), harca=True)
        m["tuz"], m["ozet"] = parola_ozet(parola)
        m.update({"hata": 0, "kilitBitis": 0, "sonGiris": simdi()})
        return oturum(veri, tel)
    if islem == "web":  # web formundan gelen: kod çağrının giriş kodu; onaylar (KVKK + konum) formda verildi
        rid, kod = str(istek.get("rid") or ""), metin(istek.get("kod"), 6)
        k = veri["kayitlar"].get(rid)
        if not k or not k.get("girisKodu") or not hmac.compare_digest(k["girisKodu"], kod) or tel_temiz(k["musteri"].get("tel")) != tel:
            raise ValueError("Kod ya da telefon eşleşmedi.")
        tuz, ozet = parola_ozet(parola)
        if m:
            m.update({"tuz": tuz, "ozet": ozet, "hata": 0, "kilitBitis": 0})
        else:
            hesaplar[tel] = {"ad": k["musteri"].get("ad") or "Müşteri", "tuz": tuz, "ozet": ozet, "kvkkTarih": k.get("konumRizaTarih", 0),
                             "konumRizaTarih": k.get("konumRizaTarih", 0), "olusma": simdi(), "kaynak": "web"}
            olay(veri, f"Yeni müşteri hesabı (web): {hesaplar[tel]['ad']}", rid)
        hesaplar[tel]["sonGiris"] = simdi()
        return oturum(veri, tel)
    raise ValueError("İşlem bilinmiyor.")
