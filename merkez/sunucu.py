"""Tasarruf Yanımda merkezi: uygulamanın test sürümü için ortak veri (çağrılar, mesajlar, SPY durumları).

Çalıştır:  python sunucu.py          (127.0.0.1:8794/<gizli_yol.txt>/)
Durdur:    python sunucu.py --durdur
Ek kütüphane: pywebpush (uygulaması kapalı SPY'ye bildirim; yoksa bildirim gitmez, gerisi çalışır).
Uygulama dosyalarını depo kökünden sunar; uygulama sayfasına window.TY_CANLI eklenir,
böylece GitHub Pages'teki kopya gösteri modunda kalır, buradaki kopya merkeze bağlanır.
"""
import base64
import hashlib
import hmac
import json
import math
import os
import secrets
import signal
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

KLASOR = Path(__file__).resolve().parent
KOK = KLASOR.parent
PORT = int(os.environ.get("TY_PORT", "8794"))
VERI = Path(os.environ.get("TY_VERI") or KLASOR / "veri.json")  # deneme kopyası ayrı dosya kullanır
PID = KLASOR / ("sunucu.pid" if PORT == 8794 else f"sunucu_{PORT}.pid")
ANAHTAR = KLASOR / "gizli_yol.txt"
UYGULAMA = "Eminevim Saha Paneli.dc.html"
kilit = threading.Lock()
GORULME = {}  # SPY id -> son yoklama zamanı (yalnız bellekte)
# Bildirim (Web Push): telefon başına abonelik; bir telefon tek SPY'ye bağlı, bir SPY'nin birden çok telefonu olabilir.
# Sıfırlamada silinmez (ayrı dosya). Anahtar yalnız sunucuda (depoda yok).
ABONELIK = VERI.with_name(VERI.stem + "_abonelik.json")
VAPID = KLASOR / "vapid.pem"
VAPID_SUB = "mailto:sualpsudas@users.noreply.github.com"  # bildirim servislerine iletişim (depodaki açık git kimliği)

# Test SPY'leri depo kökündeki spyler.js'ten (uygulama da aynı dosyayı okur); konumlar sabit, H/G uydurma.
# Listede yalnız randevu H/G ve ciro H/G ikisi de >= %100 olan SPY'ler bulunur (şartı sağlamayan uygulamada yer almaz).
def spyleri_oku():
    metin = (KOK / "spyler.js").read_text(encoding="utf-8")
    liste = json.loads(metin[metin.index("["):metin.rindex("]") + 1])
    return [{**x, "yer": f"{x['mahalle']}, {x['ilce']}"} for x in liste]


SPYLER = spyleri_oku()
SPY_IDLER = {s["id"] for s in SPYLER}

# Atama kuralları (rapor/tasarruf-yanimda-proje-calismasi/10-atama-ve-rota.md)
KABUL_SN = 120          # SPY bu sürede kabul etmezse çağrı sıradakine geçer (sınır yok; herkes reddederse "kimse almadı")
GUNLUK_SINIR = 4        # bir SPY'ye bir günde en fazla çağrı
ARALIK_DK = 90          # ileri saatte aynı gün iki randevu arası en az
HEMEN_DK = 120          # bugün ve saati en geç 2 saat sonra olan çağrı "hemen" sayılır (en erken seçilebilen saatler)
BILDIRIM_TTL = 120      # telefon kapalı/çevrimdışıysa bildirim bu süre bekler (teklif süresi kadar)
AGIRLIK = {"hemen": {"yakinlik": 50, "randevu": 15, "ciro": 15, "yuk": 20},
           "ileri": {"randevu": 25, "ciro": 25, "yakinlik": 30, "yuk": 20}}
KAPALI_DURUMLAR = {"tamamlandi", "iptal"}
DURUM_AD = {"alindi": "yeni çağrı", "atandi": "SPY kabul etti", "netlesti": "müşteri saati onayladı", "yolda": "SPY yola çıktı",
            "gorusme": "SPY yolda", "gorusmede": "kapıda doğrulandı, görüşmede", "tamamlandi": "görüşme tamamlandı", "iptal": "iptal edildi"}
STATIK_UZANTI = {".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".css": "text/css; charset=utf-8",
                 ".json": "application/json; charset=utf-8", ".png": "image/png", ".jpg": "image/jpeg", ".svg": "image/svg+xml",
                 ".webp": "image/webp", ".ico": "image/x-icon"}
STATIK_KOK = {UYGULAMA, "index.html", "appointment.js", "assignment.js", "org-data.js", "support.js", "konum-sec.html",
              "rota.html", "map.html", "manifest.json", "eminevim-qr.png", "canli.js", "spyler.js", "web-basvuru/index.html"}
STATIK_KLASOR = ("assets/", "vendor/", "web-basvuru/")


def simdi():
    return int(time.time() * 1000)


def bos_veri():
    return {"surum": 1, "spyler": {s["id"]: {**s, "durum": "musait", "sonGorulme": 0} for s in SPYLER}, "kayitlar": {},
            "musteriler": {AYSE_TEL: dict(AYSE)}, "olaylar": []}


# ---- Müşteri hesabı: telefon + parola her telefonda aynı. Parolanın kendisi saklanmaz (PBKDF2 özeti). ----
PAROLA_TUR = 100_000
HATA_SINIR, KILIT_DK = 5, 5   # art arda 5 yanlış parola → 5 dk giriş kapalı
KOD_DK = 10                   # SMS kodu (test: ekranda gösterilir) 10 dk geçerli
KODLAR = {}                   # tel -> {"kod", "bitis", "hata"} (yalnız bellekte)


def parola_ozet(parola, tuz=None):
    tuz = tuz or secrets.token_hex(16)
    return tuz, hashlib.pbkdf2_hmac("sha256", parola.encode("utf-8"), bytes.fromhex(tuz), PAROLA_TUR).hex()


def tel_temiz(deger):
    return "".join(c for c in str(deger or "") if c.isdigit())[-10:]


AYSE_TEL = "5321456789"  # gösteri hesabı (Ayşe Kaya, parola test123); sıfırlamada yeniden kurulur
_t, _o = parola_ozet("test123")
AYSE = {"ad": "Ayşe Kaya", "tuz": _t, "ozet": _o, "kvkkTarih": 0, "olusma": 0}


def oku():
    if not VERI.exists():
        yaz(bos_veri())
    veri = json.loads(VERI.read_text(encoding="utf-8"))
    veri.setdefault("musteriler", {AYSE_TEL: dict(AYSE)})
    eski = veri["spyler"]
    veri["spyler"] = {s["id"]: {**eski.get(s["id"], {"durum": "musait", "sonGorulme": 0}), **s} for s in SPYLER}  # listeden çıkan SPY düşer
    return veri


def degistir(gecici, hedef):
    # Windows: hedefi o an başka bir program (virüs tarayıcısı, yedekleme, okuyan süreç) açık tutuyorsa
    # yer değiştirme "erişim engellendi" verir; kısa aralıklarla yeniden dene
    for deneme in range(20):
        try:
            return os.replace(gecici, hedef)
        except PermissionError:
            if deneme == 19:
                raise
            time.sleep(0.05)


def yaz(veri):
    gecici = VERI.with_suffix(".tmp")
    gecici.write_text(json.dumps(veri, ensure_ascii=False), encoding="utf-8")
    degistir(gecici, VERI)


def km(a, b):
    r = math.radians
    h = math.sin(r(b["lat"] - a["lat"]) / 2) ** 2 + math.cos(r(a["lat"])) * math.cos(r(b["lat"])) * math.sin(r(b["lng"] - a["lng"]) / 2) ** 2
    return 6371 * 2 * math.atan2(math.sqrt(h), math.sqrt(1 - h))


def olay(veri, metin, kayit_id=""):
    veri["olaylar"] = ([{"t": simdi(), "metin": metin, "id": kayit_id}] + veri["olaylar"])[:200]


def acik_sayi(veri, spy_id):
    return sum(1 for k in veri["kayitlar"].values() if k.get("repId") == spy_id and k.get("durum") not in KAPALI_DURUMLAR)


def bugun():
    return time.strftime("%Y-%m-%d")


def dakika(saat):
    try:
        h, m = str(saat).split(":")[:2]
        return int(h) * 60 + int(m)
    except ValueError:
        return None


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


def anlik_konum(veri, s):
    """Canlı GPS yok: bugünkü son randevusunun yeri (yolda/görüşmede/tamamlandı), yoksa kendi mahallesi."""
    son = [x for x in veri["kayitlar"].values() if x.get("repId") == s["id"] and x.get("tarih") == bugun()
           and x.get("durum") in ("yolda", "gorusmede", "tamamlandi") and isinstance(x.get("konum"), dict) and "lat" in x["konum"]]
    if son:
        x = max(son, key=lambda y: y.get("guncelleme", 0))["konum"]
        return {"lat": x["lat"], "lng": x["lng"]}
    return {"lat": s["lat"], "lng": s["lng"]}


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
        p = {"randevu": min(max((s.get("randevuHG", 100) - 100) / 30, 0), 1),
             "ciro": min(max((s.get("ciroHG", 100) - 100) / 30, 0), 1),
             "yakinlik": max(0.0, 1 - uzak / 10),
             "yuk": 1 - len(benim) / GUNLUK_SINIR}
        puan = round(sum(a[x] * p[x] for x in a), 1)
        gerekce = f"{str(round(uzak, 1)).replace('.', ',')} km · H/G %{s.get('randevuHG')}/%{s.get('ciroHG')} · {'bugün' if tarih == bugun() else 'o gün'} {len(benim)} çağrı"
        sonuc.append((puan, s, gerekce, round(uzak, 1)))
    return sorted(sonuc, key=lambda x: -x[0])


def teklif_et(veri, k, neden=""):
    """Çağrıyı sıradaki en yüksek puanlı SPY'ye teklif eder; uygun kimse kalmadıysa "kimse almadı" (haritada kırmızı)."""
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
                       "etiket": k["id"]})
    return k


# ---- Bildirim (Web Push) ----
abone_kilit = threading.Lock()


def abone_oku():
    try:
        return json.loads(ABONELIK.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def abone_yaz(a):
    gecici = ABONELIK.with_suffix(".tmp")
    gecici.write_text(json.dumps(a, ensure_ascii=False), encoding="utf-8")
    degistir(gecici, ABONELIK)


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


VAPID_NESNE, VAPID_ACIK = None, ""


def uygun_uc(uc):
    from urllib.parse import urlparse
    u = urlparse(str(uc or ""))
    return u.scheme == "https" or (u.scheme == "http" and u.hostname == "127.0.0.1")  # yerel olan yalnız test için


def bildir(spy_id, govde):
    """SPY'nin bildirim açtığı tüm telefonlara gönderir (arka planda; çağrı akışını bekletmez)."""
    if not VAPID_NESNE:
        return
    hedefler = [x for x in abone_oku().values() if x.get("spy") == spy_id]
    if hedefler:
        threading.Thread(target=bildir_gonder, args=(hedefler, govde), daemon=True).start()


def bildir_musteri(k, baslik, govde):
    """Müşteriye (hesabına giriş yapıp bildirim açtığı telefonlara) çağrıyla ilgili haber; dokununca o randevu açılır.
    Yalnız web'den gelip uygulamaya hiç girmeyen müşterinin aboneliği yoktur: ona gitmez."""
    tel = tel_temiz((k.get("musteri") or {}).get("tel"))
    if not VAPID_NESNE or not tel:
        return
    hedefler = [x for x in abone_oku().values() if x.get("musteri") == tel]
    if hedefler:
        threading.Thread(target=bildir_gonder, args=(hedefler, {"baslik": baslik, "govde": govde, "etiket": "m-" + k["id"], "rid": k["id"]}),
                         daemon=True).start()


def saat_yaz(ms):
    return time.strftime("%H:%M", time.localtime(ms / 1000)) if ms else ""


def bildir_gonder(hedefler, govde):
    from pywebpush import webpush, WebPushException
    bitti = []
    for h in hedefler:
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


def sureleri_denetle(veri):
    """2 dakikada kabul edilmeyen teklifleri sıradaki SPY'ye geçirir; kimsenin almadığı çağrıya yeni uygun SPY
    çıktıysa (moladan döndü, uygulamayı açtı) ona teklif eder. Değişiklik olduysa True."""
    degisti = False
    for k in veri["kayitlar"].values():
        t = k.get("teklif") or {}
        if k.get("durum") == "alindi" and k.get("repId") and t.get("bitis") and t["bitis"] < simdi():
            teklif_et(veri, k, " (önceki 2 dk içinde kabul etmedi)")
            damga(veri, k)
            degisti = True
        elif k.get("durum") == "alindi" and k.get("sahipsiz") and adaylar(veri, k, set(t.get("denenen", [])) | set(k.get("eskiRepler", []))):
            teklif_et(veri, k, " (yeni uygun SPY)")
            damga(veri, k)
            degisti = True
    return degisti


def damga(veri, kayit):
    veri["surum"] += 1
    kayit["surum"] = veri["surum"]
    kayit["guncelleme"] = simdi()


def metin(deger, uzunluk=1000):
    return str(deger or "").strip()[:uzunluk]


def temiz_kayit(gelen):
    if not isinstance(gelen, dict) or not gelen.get("id"):
        raise ValueError("Kayıt eksik.")
    k = {a: d for a, d in gelen.items() if a not in ("mesajlar", "surum", "guncelleme", "musteri", "eskiRepler", "olusma", "atanma", "uzaklikKm")}
    if len(json.dumps(k, ensure_ascii=False)) > 20000:
        raise ValueError("Kayıt çok büyük.")
    return k


def uygula(veri, yol, istek):
    kayitlar = veri["kayitlar"]
    if yol == "api/cagri":
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
        kayitlar[k["id"]] = k
        olay(veri, f"Yeni çağrı: {k['musteri']['ad'] or 'Müşteri'} ({k.get('yer') or ''}), {k.get('gunYazi') or k.get('tarih') or ''} {k.get('saat') or ''}", k["id"])
        teklif_et(veri, k)
        damga(veri, k)
        return k
    if yol == "api/kayit":
        k = temiz_kayit(istek.get("kayit"))
        for alan in ("teklif", "sahipsiz", "atamaPuan", "gerekce", "girisKodu", "konumRizaTarih"):
            k.pop(alan, None)  # bunları yalnız merkez yazar
        eski = kayitlar.get(k["id"])
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
            bildir_musteri(eski, f"Temsilciniz belli oldu: {spy_ad}" + (f" · {zaman}" if zaman else ""), "Randevunuzu görmek için dokunun.")
        elif onceki != "yolda" and eski.get("durum") == "yolda":
            varis = saat_yaz(eski.get("varisZamani"))
            bildir_musteri(eski, "Temsilciniz yola çıktı" + (f" · tahmini varış {varis}" if varis else ""), f"{spy_ad} size doğru geliyor.")
        return eski
    if yol == "api/mesaj":
        k = kayitlar.get(str(istek.get("id") or ""))
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
                bildir_musteri(k, "Temsilcinizden mesaj: " + veri["spyler"].get(k.get("repId"), {}).get("ad", ""), yazi[:120])
        return k
    if yol == "api/spy":
        s = veri["spyler"].get(str(istek.get("id") or ""))
        if not s:
            raise ValueError("SPY bulunamadı.")
        if istek.get("durum") in ("musait", "molada") and istek["durum"] != s["durum"]:
            s["durum"] = istek["durum"]
            olay(veri, f"{s['ad']}: {'Müsait' if s['durum'] == 'musait' else 'Molada'}")
            veri["surum"] += 1
        s["sonGorulme"] = simdi()
        return s
    if yol == "api/aktar":  # SPY "Devret" dedi: sıradaki SPY'ye teklif (yönetici ataması yok)
        k = kayitlar.get(str(istek.get("id") or ""))
        if not k:
            raise ValueError("Çağrı bulunamadı.")
        if k.get("durum") not in KAPALI_DURUMLAR:
            k["durum"] = "alindi"
            teklif_et(veri, k, f" ({veri['spyler'].get(k.get('repId'), {}).get('ad', 'SPY')} devretti)")
            damga(veri, k)
        return k
    if yol == "api/kod":
        tel = "".join(c for c in str(istek.get("tel") or "") if c.isdigit())[-10:]
        kod = metin(istek.get("kod"), 6)
        for k in sorted(kayitlar.values(), key=lambda x: -x.get("olusma", 0)):
            if k.get("girisKodu") == kod and "".join(c for c in k.get("musteri", {}).get("tel", "") if c.isdigit())[-10:] == tel:
                return k
        raise ValueError("Kod ya da telefon eşleşmedi.")
    if yol == "api/musteri":
        return musteri_islem(veri, istek)
    if yol == "api/sifirla":
        KODLAR.clear()
        if istek.get("onay") != "evet":
            raise ValueError("Onay eksik.")
        yedek = KLASOR / "yedek"
        yedek.mkdir(exist_ok=True)
        (yedek / time.strftime("veri_%Y-%m-%d_%H%M%S.json")).write_text(json.dumps(veri, ensure_ascii=False), encoding="utf-8")
        surum = veri["surum"]
        veri.clear()
        veri.update(bos_veri())
        veri["surum"] = surum + 1
        veri["sifirlama"] = veri["surum"]  # cihazlar eski kayıtları bırakır, müşteri oturumları kapanır
        with abone_kilit:  # müşteri hesapları silindi: bildirim abonelikleri de (SPY'ninkiler kalır)
            a = abone_oku()
            abone_yaz({uc: x for uc, x in a.items() if not x.get("musteri")})
        olay(veri, "Test verisi sıfırlandı")
        return {}
    raise KeyError(yol)


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
    """islem: sorgu | kod | kodkontrol | kayit | giris | yenile | web. Hesap merkezde; her telefonda aynı parola."""
    islem, tel = istek.get("islem"), tel_temiz(istek.get("tel"))
    if len(tel) != 10:
        raise ValueError("Telefon numaranızı 10 hane olarak yazın.")
    hesaplar = veri["musteriler"]
    m = hesaplar.get(tel)
    if islem == "sorgu":
        return {"kayitli": bool(m)}
    if islem == "kod":  # gerçek SMS gelene kadar kod yanıtta döner ve ekranda gösterilir (test)
        kod = f"{secrets.randbelow(900000) + 100000}"
        KODLAR[tel] = {"kod": kod, "bitis": simdi() + KOD_DK * 60000, "hata": 0}
        return {"kod": kod, "kayitli": bool(m)}
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


def uygulama_surumu():
    """Uygulama dosyaları değişince (git pull) değişir; açık uygulamalar "Yeni sürüm hazır · Yenile" şeridi gösterir."""
    try:
        return str(max(int((KOK / ad).stat().st_mtime) for ad in (UYGULAMA, "canli.js", "appointment.js", "spyler.js")))
    except OSError:
        return ""


def spy_ozet(veri, s):
    hal = "molada" if s.get("durum") == "molada" else "randevuda" if randevuda_mi(veri, s["id"]) else "bosta"
    bugunku = sum(1 for x in veri["kayitlar"].values() if x.get("repId") == s["id"] and x.get("tarih") == bugun() and x.get("durum") != "iptal")
    return {**s, "hal": hal, "konumAn": anlik_konum(veri, s), "bugunCagri": bugunku, "sonGorulme": GORULME.get(s["id"], 0),
            "bildirim": bildirim_sayisi(s["id"])}


def bugun_sayilar(veri):
    """Gelen Çağrı: bugün merkeze gelen çağrı. Görüşme Sayısı: bugün kapıda doğrulanan (görüşmede ya da tamamlandı)."""
    gun = bugun()
    gelen = sum(1 for k in veri["kayitlar"].values() if time.strftime("%Y-%m-%d", time.localtime(k.get("olusma", 0) / 1000)) == gun)
    gorusme = sum(1 for k in veri["kayitlar"].values() if k.get("tarih") == gun and k.get("durum") in ("gorusmede", "tamamlandi"))
    return {"gelen": gelen, "gorusme": gorusme}


class Isleyici(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _yanit(self, kod, govde, tur="application/json; charset=utf-8"):
        veri = govde if isinstance(govde, bytes) else json.dumps(govde, ensure_ascii=False).encode("utf-8")
        self.send_response(kod)
        self.send_header("Content-Type", tur)
        self.send_header("Content-Length", str(len(veri)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(veri)

    def _yol(self):
        from urllib.parse import unquote
        on = "/" + self.server.gizli + "/"
        yol = unquote(self.path.split("?")[0])
        if yol == on.rstrip("/"):
            return "yonlendir"
        return yol[len(on):] if yol.startswith(on) else None

    def _statik(self, yol):
        if ".." in yol or "\\" in yol:
            return None
        if yol == "takip":
            return KLASOR / "takip.html"
        if yol in STATIK_KOK or (yol.startswith(STATIK_KLASOR) and Path(yol).suffix.lower() in STATIK_UZANTI):
            dosya = KOK / yol
            return dosya if dosya.is_file() else None
        return None

    def do_GET(self):
        yol = self._yol()
        if yol is None:
            return self._yanit(404, {"hata": "Bulunamadı"})
        if yol in ("yonlendir", ""):
            self.send_response(302)
            self.send_header("Location", "/" + self.server.gizli + "/" + UYGULAMA.replace(" ", "%20"))
            self.end_headers()
            return
        if yol == "api/anahtar":
            return self._yanit(200, {"anahtar": VAPID_ACIK})
        if yol == "sw.js":  # merkezde önbelleksiz, yalnız bildirim gösteren servis çalışanı (Pages'teki sw.js değil)
            return self._yanit(200, (KLASOR / "canli-sw.js").read_bytes(), "text/javascript; charset=utf-8")
        if yol == "api/durum":
            from urllib.parse import parse_qs
            q = parse_qs(self.path.partition("?")[2])
            try:
                surum = int((q.get("surum") or ["0"])[0])
            except ValueError:
                surum = 0
            spy = (q.get("spy") or [""])[0]
            ids = set(",".join(q.get("ids") or []).split(",")) - {""}
            if spy in SPY_IDLER:
                GORULME[spy] = simdi()  # uygulaması açık personel (takip sayfası için)
            with kilit:
                veri = oku()
                if sureleri_denetle(veri):
                    yaz(veri)

            def gorur(k):  # personel kendi çağrılarını (devrettikleri dahil), müşteri kendi kaydını, takip sayfası hepsini
                if spy:
                    return k.get("repId") == spy or spy in k.get("eskiRepler", [])
                return k["id"] in ids if ids else "hepsi" in q
            return self._yanit(200, {"surum": veri["surum"], "simdi": simdi(), "sifirlama": veri.get("sifirlama", 0), "uygulama": uygulama_surumu(),
                                     "spyler": [spy_ozet(veri, s) for s in veri["spyler"].values()],
                                     "bugun": bugun_sayilar(veri),
                                     "kayitlar": [k for k in veri["kayitlar"].values() if k.get("surum", 0) > surum and gorur(k)],
                                     "olaylar": veri["olaylar"][:80] if "hepsi" in q else []})
        dosya = self._statik(yol)
        if not dosya:
            return self._yanit(404, {"hata": "Bulunamadı"})
        icerik = dosya.read_bytes()
        if dosya.name == UYGULAMA or dosya.parent.name == "web-basvuru" and dosya.suffix == ".html":
            on = ("/" + self.server.gizli + "/").encode()  # tam yol: web formu kopyasında <base> eminevim.com'u gösterir
            icerik = icerik.replace(b"<head>", b'<head>\n<script>window.TY_CANLI={api:"' + on + b'api/"};</script>\n<script src="' + on + b'canli.js"></script>', 1)
        self._yanit(200, icerik, STATIK_UZANTI.get(dosya.suffix.lower(), "application/octet-stream"))

    def do_POST(self):
        yol = self._yol()
        if yol in ("api/abone", "api/abone-sil"):
            return self._abone(yol)
        if yol not in ("api/cagri", "api/kayit", "api/mesaj", "api/spy", "api/aktar", "api/kod", "api/musteri", "api/sifirla"):
            return self._yanit(404, {"hata": "Bulunamadı"})
        uzunluk = int(self.headers.get("Content-Length") or 0)
        if uzunluk > 50_000:
            return self._yanit(413, {"hata": "İstek çok büyük"})
        try:
            istek = json.loads(self.rfile.read(uzunluk) or b"{}")
            with kilit:
                veri = oku()
                try:
                    sonuc = uygula(veri, yol, istek)
                except YazilanHata:
                    yaz(veri)
                    raise
                yaz(veri)
            self._yanit(200, {"surum": veri["surum"], "sonuc": sonuc})
        except (KeyError, ValueError, TypeError) as e:
            self._yanit(400, {"hata": str(e).strip("'\"")})

    def _abone(self, yol):
        uzunluk = int(self.headers.get("Content-Length") or 0)
        if uzunluk > 5_000:
            return self._yanit(413, {"hata": "İstek çok büyük"})
        try:
            self._yanit(200, {"sonuc": abone_isle(yol, json.loads(self.rfile.read(uzunluk) or b"{}"))})
        except (KeyError, ValueError, TypeError, AttributeError) as e:
            self._yanit(400, {"hata": str(e).strip("'\"")})


def abone_isle(yol, istek):
    # Kilit sırası her yerde: önce veri (kilit), sonra abonelik (abone_kilit)
    tel = tel_temiz(istek.get("musteri"))
    if yol == "api/abone" and istek.get("spy") not in SPY_IDLER and tel:
        # müşteri bildirimi yalnız o hesaba giriş yapmış telefona (girişte verilen jeton)
        with kilit:
            m = oku()["musteriler"].get(tel) or {}
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
        if (istek.get("spy") not in SPY_IDLER and not tel) or not uygun_uc(uc) or not anahtar.get("p256dh") or not anahtar.get("auth"):
            raise ValueError("Abonelik eksik.")
        kim = {"spy": istek["spy"]} if istek.get("spy") in SPY_IDLER else {"musteri": tel}
        # Telefon başka SPY/müşteri seçtiyse eski bağ kalkar (aynı uç tek kişiye bağlı)
        a[uc] = {"endpoint": uc, "keys": {"p256dh": metin(anahtar["p256dh"], 200), "auth": metin(anahtar["auth"], 100)},
                 **kim, "cihaz": metin(istek.get("cihaz"), 80), "eklenme": simdi()}
        abone_yaz(a)
        anahtar_ad, deger = next(iter(kim.items()))
        return {**kim, "telefon": sum(1 for x in a.values() if x.get(anahtar_ad) == deger)}


def gizli_yol():
    if not ANAHTAR.exists():
        ANAHTAR.write_text("ty-" + secrets.token_urlsafe(9), encoding="utf-8")
    return ANAHTAR.read_text(encoding="utf-8").strip()


def durdur():
    if not PID.exists():
        print("Çalışan sunucu yok.")
        return
    pid = int(PID.read_text())
    try:
        os.kill(pid, signal.SIGTERM)
        print(f"Durduruldu (PID {pid}).")
    except OSError:
        print("Süreç zaten kapalıymış.")
    PID.unlink(missing_ok=True)


def main():
    if "--durdur" in sys.argv:
        return durdur()
    with kilit:
        oku()
    # Windows'ta adres yeniden kullanımı aynı porta ikinci sunucunun bağlanmasına izin veriyor: kapat
    ThreadingHTTPServer.allow_reuse_address = False
    # Telefon sayfayı açarken ~20 dosyayı aynı anda ister; varsayılan 5'lik bekleme sırası taşınca Funnel 502 veriyordu
    ThreadingHTTPServer.request_queue_size = 128
    try:
        sunucu = ThreadingHTTPServer(("127.0.0.1", PORT), Isleyici)
    except OSError:
        print(f"Port {PORT} kullanımda: merkez zaten çalışıyor olabilir.", flush=True)
        return 1
    sunucu.gizli = os.environ.get("TY_YOL") or gizli_yol()
    global VAPID_NESNE, VAPID_ACIK
    VAPID_NESNE, VAPID_ACIK = vapid()

    def bekci():
        while True:
            time.sleep(5)
            with kilit:
                veri = oku()
                if sureleri_denetle(veri):
                    yaz(veri)
    threading.Thread(target=bekci, daemon=True).start()
    PID.write_text(str(os.getpid()))
    print(f"Hazır: http://127.0.0.1:{PORT}/{sunucu.gizli}/", flush=True)
    try:
        sunucu.serve_forever()
    finally:
        PID.unlink(missing_ok=True)


if __name__ == "__main__":
    sys.exit(main())
