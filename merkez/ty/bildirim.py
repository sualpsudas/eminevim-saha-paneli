"""BİLDİRİM KAPISI — SPY'ye ve müşteriye telefon bildirimi (Web Push).

Şu an: tarayıcı/Ana Ekran uygulaması aboneliği (pywebpush; yoksa bildirim gitmez, gerisi çalışır) + iPhone uygulaması (APNs, apns.py;
abonelik anahtarı "apns:<token>"). Bir telefon tek kişiye bağlı
(SPY ya da müşteri; sonuncusu geçerli), bir kişinin birden çok telefonu olabilir. Abonelikler ayrı dosyada (sıfırlamada SPY'ninkiler kalır).
Gerçek sistemde: bildir()/bildir_musteri() SMS'e de bağlanır; çağıran kod değişmez.
"""
import base64
import json
import re
import threading

from . import apns, depo
from .ayarlar import ABONELIK, BILDIRIM_TTL, VAPID, VAPID_SUB
from .musteri import jeton_ozet
from .personel import SPY_IDLER
from .yardim import metin, simdi, tel_temiz

abone_kilit = threading.Lock()
VAPID_NESNE, VAPID_ACIK = None, ""


def abone_oku():
    try:
        return json.loads(ABONELIK.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def abone_yaz(a):
    depo.json_yaz(ABONELIK, a)


def vapid():
    """Sunucunun bildirim anahtarı (ilk açılışta üretilir). Döner: (Vapid nesnesi, tarayıcıya verilen açık anahtar) ya da (None, "")."""
    try:
        from py_vapid import Vapid02 as Vapid  # RFC 8292 "vapid t=,k=" (Apple bunu ister)
        from cryptography.hazmat.primitives import serialization
    except ImportError:
        return None, ""
    if not VAPID.exists():
        v = Vapid()
        v.generate_keys()
        v.save_key(str(VAPID))
    v = Vapid.from_file(str(VAPID))
    acik = v.public_key.public_bytes(serialization.Encoding.X962, serialization.PublicFormat.UncompressedPoint)
    return v, base64.urlsafe_b64encode(acik).decode().rstrip("=")


def baslat():
    global VAPID_NESNE, VAPID_ACIK
    VAPID_NESNE, VAPID_ACIK = vapid()


def uygun_uc(uc):
    from urllib.parse import urlparse
    u = urlparse(str(uc or ""))
    return u.scheme == "https" or (u.scheme == "http" and u.hostname == "127.0.0.1")  # yerel olan yalnız test için


def bildir(spy_id, govde):
    """SPY'nin bildirim açtığı tüm telefonlara gönderir (arka planda; çağrı akışını bekletmez)."""
    if not (VAPID_NESNE or apns.hazir()):
        return
    hedefler = [x for x in abone_oku().values() if x.get("spy") == spy_id]
    if hedefler:
        threading.Thread(target=bildir_gonder, args=(hedefler, govde), daemon=True).start()


def bildir_musteri(k, baslik, govde):
    """Müşteriye (hesabına giriş yapıp bildirim açtığı telefonlara) çağrıyla ilgili haber; dokununca o randevu açılır.
    Yalnız web'den gelip uygulamaya hiç girmeyen müşterinin aboneliği yoktur: ona gitmez."""
    tel = tel_temiz((k.get("musteri") or {}).get("tel"))
    if not (VAPID_NESNE or apns.hazir()) or not tel:
        return
    hedefler = [x for x in abone_oku().values() if x.get("musteri") == tel]
    if hedefler:
        threading.Thread(target=bildir_gonder, args=(hedefler, {"baslik": baslik, "govde": govde, "etiket": "m-" + k["id"], "rid": k["id"]}),
                         daemon=True).start()


def bildir_gonder(hedefler, govde):
    bitti = []
    iphone = [h["apns"] for h in hedefler if h.get("apns")]
    if iphone:
        bitti += [("apns:" + t, sonuc) for t, sonuc in apns.gonder(iphone, govde)]
    web = [h for h in hedefler if not h.get("apns")] if VAPID_NESNE else []
    if web:
        from pywebpush import webpush, WebPushException
    for h in web:
        try:
            webpush({"endpoint": h["endpoint"], "keys": h["keys"]}, json.dumps(govde, ensure_ascii=False),
                    vapid_private_key=VAPID_NESNE, vapid_claims={"sub": VAPID_SUB}, ttl=BILDIRIM_TTL,
                    headers={"Urgency": "high"}, timeout=10)
            sonuc = "ok"
        except WebPushException as e:
            kod = getattr(e.response, "status_code", 0)
            sonuc = "silindi" if kod in (404, 410) else f"hata {kod}"
        except Exception as e:  # ağ hatası vb.: bir sonraki çağrıda yeniden denenir
            sonuc = "hata " + type(e).__name__
        bitti.append((h["endpoint"], sonuc))
    with abone_kilit:
        a = abone_oku()
        for uc, sonuc in bitti:
            if uc not in a:
                continue
            if sonuc == "silindi":
                del a[uc]  # telefon aboneliği bırakmış (uygulama silindi / izin kaldırıldı)
            else:
                a[uc].update({"son": simdi(), "sonuc": sonuc})
        abone_yaz(a)


def bildirim_sayisi(spy_id):
    return sum(1 for x in abone_oku().values() if x.get("spy") == spy_id)


def musteri_abonelerini_sil():
    """Test verisi sıfırlanınca: müşteri hesapları silindi, bildirim abonelikleri de (SPY'ninkiler kalır)."""
    with abone_kilit:
        a = abone_oku()
        abone_yaz({uc: x for uc, x in a.items() if not x.get("musteri")})


def abone_jeton_sil(tel, ozet):
    """Müşteri çıkış yapınca: o oturumun (jeton) abonelikleri ve jetonsuz eski kayıtları silinir. Kilit sırası: veri → abonelik."""
    with abone_kilit:
        a = abone_oku()
        abone_yaz({uc: x for uc, x in a.items() if not (x.get("musteri") == tel and x.get("jeton", ozet) == ozet)})


def abone_isle(yol, istek):
    # Kilit sırası her yerde: önce veri (depo.kilit), sonra abonelik (abone_kilit)
    tel = tel_temiz(istek.get("musteri"))
    if yol == "api/abone" and istek.get("spy") not in SPY_IDLER and tel:
        # müşteri bildirimi yalnız o hesaba giriş yapmış telefona (girişte verilen jeton)
        with depo.kilit:
            m = depo.oku()["musteriler"].get(tel) or {}
        if jeton_ozet(istek.get("jeton")) not in m.get("jetonlar", []):
            raise ValueError("Oturum doğrulanamadı. Yeniden giriş yapın.")
    with abone_kilit:
        a = abone_oku()
        if yol == "api/abone-sil":
            a.pop(str(istek.get("endpoint") or ""), None)
            abone_yaz(a)
            return {}
        ab = istek.get("abonelik") or {}
        uc, anahtar = ab.get("endpoint"), ab.get("keys") or {}
        kim_yok = istek.get("spy") not in SPY_IDLER and not tel
        kim = {"spy": istek["spy"]} if istek.get("spy") in SPY_IDLER else {"musteri": tel}
        if istek.get("apns"):  # iPhone uygulaması: Apple'ın verdiği cihaz kodu (hex)
            token = str(istek["apns"]).strip().lower()
            if kim_yok or not re.fullmatch(r"[0-9a-f]{32,200}", token):
                raise ValueError("Abonelik eksik.")
            a["apns:" + token] = {"endpoint": "apns:" + token, "apns": token, **kim, "jeton": jeton_ozet(istek.get("jeton")), "cihaz": metin(istek.get("cihaz"), 80), "eklenme": simdi()}
        else:
            if kim_yok or not uygun_uc(uc) or not anahtar.get("p256dh") or not anahtar.get("auth"):
                raise ValueError("Abonelik eksik.")
            # Telefon başka SPY/müşteri seçtiyse eski bağ kalkar (aynı uç tek kişiye bağlı)
            a[uc] = {"endpoint": uc, "keys": {"p256dh": metin(anahtar["p256dh"], 200), "auth": metin(anahtar["auth"], 100)},
                     **kim, "jeton": jeton_ozet(istek.get("jeton")), "cihaz": metin(istek.get("cihaz"), 80), "eklenme": simdi()}
        abone_yaz(a)
        anahtar_ad, deger = next(iter(kim.items()))
        return {**kim, "telefon": sum(1 for x in a.values() if x.get(anahtar_ad) == deger)}
