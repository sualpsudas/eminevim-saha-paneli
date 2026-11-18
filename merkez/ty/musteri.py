"""MÜŞTERİ HESABI KAPISI — telefon + SMS kodu (parola yok, 2026-11-18), oturum jetonu.

Akış: telefon → SMS kodu → kayıtlıysa içeri; yeni müşteriyse Ad + Soyad (aydınlatma metni gösterilir, onay kutusu yok;
ticari elektronik ileti izni isteğe bağlı, ayrı kutu). Oturum telefonda "Çıkış yap"a kadar kalır.
Şu an hesaplar depoda (veri["musteriler"]); SMS gönderilmez, kod yanıtta döner ve ekranda gösterilir (test).
Gerçek sistemde: hesaplar Eminevim üye sistemine (tek hesap: gerçek üyeler aynı hesapla girer), kod_gonder() SMS servisine
bağlanır (IT_DEVIR.md → Müşteri hesabı).
"""
import hashlib
import hmac
import secrets

from .ayarlar import HATA_SINIR, KOD_DK
from .yardim import metin, olay, simdi, tel_temiz

KODLAR = {}  # tel -> {"kod", "bitis", "hata"} (yalnız bellekte)

AYSE_TEL = "5321456789"  # gösteri hesabı (Ayşe Kaya); sıfırlamada yeniden kurulur
# Örnek müşteriler (uygulamadaki uygulama/ornek-veri.js → ORNEK_MUSTERILER ile aynı). Eksikse her okumada eklenir.
ORNEK_MUSTERILER = {tel: {"adi": adi, "soyadi": soyadi, "ad": f"{adi} {soyadi}", "aydinlatmaTarih": 0, "olusma": 0} for tel, adi, soyadi in [
    (AYSE_TEL, "Ayşe", "Kaya"), ("5332103456", "Zeynep", "Arslan"), ("5353204567", "Can", "Öztürk"),
    ("5414305678", "Elif", "Yıldız"), ("5436507890", "Burak", "Şahin")]}
AYSE = ORNEK_MUSTERILER[AYSE_TEL]


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


def jeton_ozet(jeton):
    return hashlib.sha256(str(jeton or "").encode()).hexdigest()


def ad_bol(ad):
    p = str(ad or "").split()
    return (" ".join(p[:-1]) or (p[0] if p else "")), (p[-1] if len(p) > 1 else "")


def oturum(veri, tel, jeton=None):
    """Girişte dönen hesap + çağrılar. Jeton bu telefonun oturumudur: uygulama kapanıp açılınca kodsuz devam
    (Çıkış yap'a kadar) ve bildirim aboneliği (müşteri adına abone olmayı kanıtlar)."""
    m = veri["musteriler"][tel]
    if not jeton:
        jeton = secrets.token_urlsafe(24)
        m["jetonlar"] = (m.get("jetonlar", []) + [jeton_ozet(jeton)])[-10:]
    adi, soyadi = (m["adi"], m.get("soyadi", "")) if m.get("adi") else ad_bol(m.get("ad"))
    return {"tel": tel, "ad": m.get("ad") or f"{adi} {soyadi}".strip(), "adi": adi, "soyadi": soyadi,
            "aydinlatmaTarih": m.get("aydinlatmaTarih") or m.get("kvkkTarih", 0), "kampanya": bool(m.get("kampanya")),
            "jeton": jeton, "kayitlar": musteri_kayitlari(veri, tel)}


class YazilanHata(ValueError):
    """Hata yanıtı döner ama veri yine kaydedilir."""


def hesap_ac(veri, tel, adi, soyadi, kampanya, kaynak="uygulama", rid=None, aydinlatma_tarih=None):
    an = simdi()
    veri["musteriler"][tel] = {"adi": adi, "soyadi": soyadi, "ad": f"{adi} {soyadi}".strip(), "aydinlatmaTarih": aydinlatma_tarih or an,
                              "kampanya": bool(kampanya), "kampanyaTarih": an if kampanya else 0, "olusma": an, "kaynak": kaynak}
    olay(veri, f"Yeni müşteri hesabı{' (web)' if kaynak == 'web' else ''}: {adi} {soyadi}", rid)


def musteri_islem(veri, istek):
    """islem: kod | dogrula | kayit | web | oturum | cikis | izin. Hesap merkezde; her telefonda aynı numara + SMS kodu."""
    islem, tel = istek.get("islem"), tel_temiz(istek.get("tel"))
    if len(tel) != 10:
        raise ValueError("Telefon numaranızı 10 hane olarak yazın.")
    hesaplar = veri["musteriler"]
    m = hesaplar.get(tel)
    if islem == "kod":  # gerçek SMS gelene kadar kod yanıtta döner ve ekranda gösterilir (test)
        return {"kod": kod_gonder(tel)}
    if islem in ("oturum", "cikis", "izin"):  # uygulama yeniden açıldı / Çıkış yap / Ayarlar'da ticari ileti izni
        jeton = str(istek.get("jeton") or "")
        if not m or jeton_ozet(jeton) not in m.get("jetonlar", []):
            raise ValueError("Oturum doğrulanamadı. Yeniden giriş yapın.")
        if islem == "cikis":
            m["jetonlar"].remove(jeton_ozet(jeton))
            return {}
        if islem == "izin":  # izin verildiği kadar kolay geri alınır; tarihiyle kaydedilir (İYS bildirimi şirket sürecinde)
            m["kampanya"], m["kampanyaTarih"] = istek.get("kampanya") is True, simdi()
            olay(veri, f"Ticari ileti izni {'verildi' if m['kampanya'] else 'geri alındı'}: {m.get('ad', '')}")
            return {"kampanya": m["kampanya"]}
        return oturum(veri, tel, jeton)
    if islem == "dogrula":  # kayıtlı müşteri: kod doğruysa içeri; yeni müşteri: kod geçerli kalır (kayıtta harcanır)
        kod_dogru(tel, istek.get("kod"), harca=bool(m))
        if not m:
            return {"kayitli": False}
        m["sonGiris"] = simdi()
        return {"kayitli": True, **oturum(veri, tel)}
    if islem == "kayit":  # yeni müşteri: SMS kodu + Ad + Soyad + "Aydınlatma Metni'ni okudum" onayı + isteğe bağlı ticari ileti izni
        if m:
            raise ValueError("Bu numara kayıtlı. Kodla giriş yapın.")
        adi, soyadi = metin(istek.get("adi"), 40), metin(istek.get("soyadi"), 40)
        if len(adi) < 2:
            raise ValueError("Adınızı yazın.")
        if len(soyadi) < 2:
            raise ValueError("Soyadınızı yazın.")
        if istek.get("aydinlatmaOnay") is not True:
            raise ValueError("Devam etmek için Aydınlatma Metni'ni okuduğunuzu onaylayın.")
        kod_dogru(tel, istek.get("kod"), harca=True)
        hesap_ac(veri, tel, adi, soyadi, istek.get("kampanya") is True)
        return oturum(veri, tel)
    if islem == "web":  # web formundan gelen: kod çağrının giriş kodu; ad, soyad, aydınlatma ve izin formda alındı
        rid, kod = str(istek.get("rid") or ""), metin(istek.get("kod"), 6)
        k = veri["kayitlar"].get(rid)
        if not k or not k.get("girisKodu") or not hmac.compare_digest(k["girisKodu"], kod) or tel_temiz(k["musteri"].get("tel")) != tel:
            raise ValueError("Kod ya da telefon eşleşmedi.")
        if not m:
            km = k["musteri"]
            adi, soyadi = (km["adi"], km.get("soyadi", "")) if km.get("adi") else ad_bol(km.get("ad") or "Müşteri")
            hesap_ac(veri, tel, adi, soyadi, k.get("kampanya"), "web", rid, k.get("aydinlatmaTarih") or k.get("olusma"))
        hesaplar[tel]["sonGiris"] = simdi()
        return oturum(veri, tel)
    raise ValueError("İşlem bilinmiyor.")
