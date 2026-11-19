"""KAPIDA KİMLİK DOĞRULAMA KAPISI — QR + 4 haneli yedek kod (2026-11-19: kod merkezde üretilir ve kontrol edilir).

  kod      müşteri "Kapıda kimliğini doğrula" dedi → randevuya özel 4 haneli kod (10 dk). Yalnız müşteriye döner:
           kayda yazılmaz, SPY'nin cihazına gitmez (api/durum'da görünmez). Süresi dolmadıysa aynı kod döner.
  dogrula  SPY müşterinin QR'ını okuttu ya da kodu girdi → randevu + SPY + randevu sürümü + süre kontrolü;
           doğruysa çağrı "gorusmede" olur, kod harcanır. Aynı koda 5 yanlış deneme → kod geçersiz, müşteri yeniler.
Kodlar yalnız bellekte (merkez yeniden başlarsa müşteri "Kodu yenile"ye dokunur).
Gerçek sistemde: SPY kimliği personel girişinden gelir (şu an SPY seçimi), müşteri oturumu Eminevim üye sisteminden.
"""
import hmac
import secrets

from . import bildirim
from .ayarlar import HATA_SINIR, KOD_DK
from .musteri import jeton_ozet
from .yardim import damga, metin, olay, simdi, tel_temiz

KAPI_KODLARI = {}  # çağrı id -> {"kod", "son", "revision", "hata"}
DOGRULANABILIR = ("yolda", "gorusme")


def _musteri_mi(veri, k, istek):
    tel = tel_temiz(istek.get("tel"))
    m = veri["musteriler"].get(tel)
    if not m or jeton_ozet(istek.get("jeton")) not in m.get("jetonlar", []) or tel_temiz((k.get("musteri") or {}).get("tel")) != tel:
        raise ValueError("Oturum doğrulanamadı. Yeniden giriş yapın.")


def kapi_kodu(veri, k, istek):
    _musteri_mi(veri, k, istek)
    if k.get("durum") not in DOGRULANABILIR or not k.get("repId"):
        raise ValueError("Kod, temsilciniz yola çıkınca açılır.")
    an, rev = simdi(), k.get("revision") or 1
    c = KAPI_KODLARI.get(k["id"])
    if not c or c["son"] <= an or c["revision"] != rev:
        c = KAPI_KODLARI[k["id"]] = {"kod": f"{secrets.randbelow(9000) + 1000}", "son": an + KOD_DK * 60000, "revision": rev, "hata": 0}
    return {"id": None, "kod": c["kod"], "son": c["son"], "revision": rev}  # id yok: istemci bunu kayıt sanmasın


def kapi_dogrula(veri, k, istek):
    spy = str(istek.get("spy") or "")
    if k.get("repId") != spy:
        raise ValueError("Bu randevu başka bir SPY'ye atanmış.")
    if k.get("durum") == "gorusmede":
        return k  # iki kez okutuldu: zaten doğrulandı
    if k.get("durum") not in DOGRULANABILIR:
        raise ValueError("Bu randevu şu an doğrulanamaz. Önce \"Yola çık\" deyin.")
    c, an = KAPI_KODLARI.get(k["id"]), simdi()
    if istek.get("revision") not in (None, k.get("revision") or 1):
        raise ValueError("Bu QR eski bir randevuya ait. Müşteriden kodu yenilemesini isteyin.")
    if not c or c["son"] <= an or c["revision"] != (k.get("revision") or 1):
        raise ValueError("Kodun süresi doldu. Müşteriden “Kodu yenile”ye dokunmasını isteyin.")
    if not hmac.compare_digest(c["kod"], metin(istek.get("kod"), 4)):
        c["hata"] += 1
        if c["hata"] >= HATA_SINIR:
            KAPI_KODLARI.pop(k["id"], None)
            raise ValueError("Çok fazla yanlış deneme. Müşteriden “Kodu yenile”ye dokunmasını isteyin.")
        raise ValueError("Kod eşleşmedi. Müşterinin ekranındaki 4 haneli kodu girin.")
    KAPI_KODLARI.pop(k["id"], None)
    k.update({"durum": "gorusmede", "dogrulama": None, "dogrulandi": {"bookingId": k["id"], "repId": spy, "zaman": an,
                                                                       "yol": "qr" if istek.get("qr") else "kod"}})
    spy_ad = veri["spyler"].get(spy, {}).get("ad", "")
    olay(veri, f"{(k.get('musteri') or {}).get('ad') or 'Müşteri'}: kapıda doğrulandı ({spy_ad})", k["id"])
    damga(veri, k)
    bildirim.bildir_musteri(k, "Temsilciniz doğrulandı: " + spy_ad, "Görüşmeniz başladı. İyi görüşmeler!")
    return k


def dogrulama_islem(veri, istek):
    k = veri["kayitlar"].get(str(istek.get("id") or ""))
    if not k:
        raise ValueError("Randevu bulunamadı.")
    islem = istek.get("islem")
    if islem == "kod":
        return kapi_kodu(veri, k, istek)
    if islem == "dogrula":
        return kapi_dogrula(veri, k, istek)
    raise ValueError("İşlem bilinmiyor.")
