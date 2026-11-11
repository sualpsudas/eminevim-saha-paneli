"""Tasarruf Yanımda merkezi: uygulamanın test sürümü için ortak veri (çağrılar, mesajlar, SPY durumları).

Çalıştır:  python sunucu.py          (127.0.0.1:8794/<gizli_yol.txt>/)
Durdur:    python sunucu.py --durdur
Ek kütüphane yok. Uygulama dosyalarını depo kökünden sunar; uygulama sayfasına window.TY_CANLI eklenir,
böylece GitHub Pages'teki kopya gösteri modunda kalır, buradaki kopya merkeze bağlanır.
"""
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

# Test SPY'leri depo kökündeki spyler.js'ten (uygulama da aynı dosyayı okur); konumlar sabit, H/G uydurma
def spyleri_oku():
    metin = (KOK / "spyler.js").read_text(encoding="utf-8")
    liste = json.loads(metin[metin.index("["):metin.rindex("]") + 1])
    return [{**x, "yer": f"{x['mahalle']}, {x['ilce']}"} for x in liste]


SPYLER = spyleri_oku()
SPY_IDLER = {s["id"] for s in SPYLER}

# Atama kuralları (rapor/tasarruf-yanimda-proje-calismasi/10-atama-ve-rota.md)
KABUL_SN = 120          # SPY bu sürede kabul etmezse çağrı sıradakine geçer
EN_FAZLA_DENEME = 3     # üç SPY kabul etmezse çağrı yöneticiye düşer
GUNLUK_SINIR = 4        # bir SPY'ye bir günde en fazla çağrı
ARALIK_DK = 90          # ileri tarihte aynı gün iki randevu arası en az
ACIK_SN = 30            # aynı gün çağrısı için uygulaması açık sayılma süresi
AGIRLIK = {"ayni": {"randevu": 15, "ciro": 15, "yakinlik": 50, "yuk": 10, "hiz": 10},
           "ileri": {"randevu": 25, "ciro": 25, "yakinlik": 20, "yuk": 20, "hiz": 10}}
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
    return {"surum": 1, "spyler": {s["id"]: {**s, "durum": "musait", "sonGorulme": 0} for s in SPYLER}, "kayitlar": {}, "olaylar": []}


def oku():
    if not VERI.exists():
        yaz(bos_veri())
    veri = json.loads(VERI.read_text(encoding="utf-8"))
    for s in SPYLER:  # sabit bilgiler kod değişince güncellenir, durum korunur
        veri["spyler"][s["id"]] = {**veri["spyler"].get(s["id"], {"durum": "musait", "sonGorulme": 0}), **s}
    return veri


def yaz(veri):
    gecici = VERI.with_suffix(".tmp")
    gecici.write_text(json.dumps(veri, ensure_ascii=False), encoding="utf-8")
    os.replace(gecici, VERI)


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


def aktif_mi(s):
    """Tasarruf Yanımda'da aktif SPY: son 3 ay randevu H/G ve ciro H/G ikisi de en az %100."""
    return s.get("randevuHG", 0) >= 100 and s.get("ciroHG", 0) >= 100


def adaylar(veri, k, haric=()):
    """Eleme + puan. Döner: puana göre sıralı [(puan, spy, gerekçe)]."""
    konum = k.get("konum") or {}
    tarih = k.get("tarih") or bugun()
    ayni_gun = tarih <= bugun()
    a = AGIRLIK["ayni" if ayni_gun else "ileri"]
    gun_kayit = [x for x in veri["kayitlar"].values() if x.get("tarih") == tarih and x.get("durum") != "iptal" and x["id"] != k.get("id")]
    hafta = {time.strftime("%Y-%m-%d", time.localtime(time.time() + g * 86400)) for g in range(-3, 4)}
    sonuc = []
    for s in veri["spyler"].values():
        if s["id"] in haric or not aktif_mi(s) or s.get("durum") == "molada":
            continue
        benim = [x for x in gun_kayit if x.get("repId") == s["id"]]
        if len(benim) >= GUNLUK_SINIR:
            continue
        if ayni_gun:
            if simdi() - GORULME.get(s["id"], 0) > ACIK_SN * 1000:
                continue  # aynı gün: hazırda olan (uygulaması açık) SPY
            if any(x.get("repId") == s["id"] and x.get("durum") in ("yolda", "gorusmede") for x in veri["kayitlar"].values()):
                continue
            uzak = km(s, konum)
        else:
            d = dakika(k.get("saat"))
            if d is not None and any(dakika(x.get("saat")) is not None and abs(dakika(x.get("saat")) - d) < ARALIK_DK for x in benim):
                continue
            noktalar = [s] + [x["konum"] for x in benim if isinstance(x.get("konum"), dict) and "lat" in x["konum"]]
            uzak = min(km(n, konum) for n in noktalar)  # o günkü rotasına ya da şubesine en yakın nokta
        haftalik = sum(1 for x in veri["kayitlar"].values() if x.get("repId") == s["id"] and x.get("tarih") in hafta and x.get("durum") != "iptal")
        p = {"randevu": min(max((s.get("randevuHG", 100) - 100) / 20, 0), 1),
             "ciro": min(max((s.get("ciroHG", 100) - 100) / 20, 0), 1),
             "yakinlik": max(0.0, 1 - uzak / 10),
             "yuk": (1 - len(benim) / GUNLUK_SINIR) if ayni_gun else 0.5 * (1 - len(benim) / GUNLUK_SINIR) + 0.5 * max(0.0, 1 - haftalik / 12),
             "hiz": 0.5 * min(max(1 - (s.get("kabulSn", 60) - 20) / 100, 0), 1) + 0.5 * min(max((s.get("kabulOrani", 90) - 80) / 20, 0), 1)}
        puan = round(sum(a[x] * p[x] for x in a), 1)
        gerekce = f"{str(round(uzak, 1)).replace('.', ',')} km · H/G %{s.get('randevuHG')}/%{s.get('ciroHG')} · {'bugün' if ayni_gun else 'o gün'} {len(benim)} çağrı"
        sonuc.append((puan, s, gerekce, round(uzak, 1)))
    return sorted(sonuc, key=lambda x: -x[0])


def teklif_et(veri, k, neden=""):
    """Çağrıyı sıradaki en yüksek puanlı SPY'ye teklif eder; kalmadıysa yöneticiye düşer."""
    t = k.setdefault("teklif", {"denenen": []})
    liste = adaylar(veri, k, set(t["denenen"]) | set(k.get("eskiRepler", [])))
    ad = (k.get("musteri") or {}).get("ad") or "Müşteri"
    if len(t["denenen"]) >= EN_FAZLA_DENEME or not liste:
        if k.get("repId"):
            k["eskiRepler"] = sorted(set(k.get("eskiRepler", [])) | {k["repId"]})
        k.update({"repId": None, "yonetici": True, "durum": "alindi", "gerekce": ""})
        t["bitis"] = 0
        olay(veri, f"{ad}: {'uygun SPY yok' if not liste else str(EN_FAZLA_DENEME) + ' SPY kabul etmedi'} → yöneticiye düştü{neden}", k["id"])
        return k
    puan, spy, gerekce, uzak = liste[0]
    if k.get("repId") and k["repId"] != spy["id"]:
        k["eskiRepler"] = sorted(set(k.get("eskiRepler", [])) | {k["repId"]})
    t["denenen"].append(spy["id"])
    t["bitis"] = simdi() + KABUL_SN * 1000
    k.update({"repId": spy["id"], "yonetici": False, "durum": "alindi", "atanma": simdi(), "uzaklikKm": uzak, "puan": puan, "gerekce": gerekce})
    olay(veri, f"{ad} ({k.get('yer') or ''}) → {spy['ad']} · puan {str(puan).replace('.', ',')} · {gerekce}{neden}", k["id"])
    return k


def sureleri_denetle(veri):
    """2 dakikada kabul edilmeyen teklifleri sıradaki SPY'ye geçirir. Değişiklik olduysa True."""
    degisti = False
    for k in veri["kayitlar"].values():
        t = k.get("teklif") or {}
        if k.get("durum") == "alindi" and k.get("repId") and t.get("bitis") and t["bitis"] < simdi():
            teklif_et(veri, k, " (önceki 2 dk içinde kabul etmedi)")
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
        konum = k.get("konum") or {}
        if not isinstance(konum.get("lat"), (int, float)) or not isinstance(konum.get("lng"), (int, float)):
            raise ValueError("Konum eksik.")
        m = istek.get("musteri") or {}
        k["musteri"] = {"ad": metin(m.get("ad"), 80), "tel": metin(m.get("tel"), 20), "ekBilgi": m.get("ekBilgi") if isinstance(m.get("ekBilgi"), dict) else None}
        k.update({"mesajlar": [], "olusma": simdi(), "repId": None, "teklif": {"denenen": []}})
        if istek.get("kaynak") == "web":
            k["girisKodu"] = f"{secrets.randbelow(900000) + 100000}"  # SMS yerine ekranda gösterilir (test)
        kayitlar[k["id"]] = k
        olay(veri, f"Yeni çağrı: {k['musteri']['ad'] or 'Müşteri'} ({k.get('yer') or ''}), {k.get('gunYazi') or k.get('tarih') or ''} {k.get('saat') or ''}", k["id"])
        teklif_et(veri, k)
        damga(veri, k)
        return k
    if yol == "api/kayit":
        k = temiz_kayit(istek.get("kayit"))
        for alan in ("teklif", "yonetici", "puan", "gerekce", "girisKodu"):
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
        eski.update(k)
        damga(veri, eski)
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
    if yol == "api/aktar":
        k = kayitlar.get(str(istek.get("id") or ""))
        rep = str(istek.get("repId") or "")
        if k and not rep:  # SPY "Devret" dedi: sıradaki SPY'ye teklif (yöneticiye düşebilir)
            if k.get("durum") not in KAPALI_DURUMLAR:
                k["durum"] = "alindi"
                teklif_et(veri, k, f" ({veri['spyler'].get(k.get('repId'), {}).get('ad', 'SPY')} devretti)")
                damga(veri, k)
            return k
        if not k or rep not in SPY_IDLER:
            raise ValueError("Aktarım eksik.")
        if k.get("repId") != rep:
            k["eskiRepler"] = sorted((set(k.get("eskiRepler", [])) | {k.get("repId")}) - {None})
            k["repId"] = rep
            k["yonetici"] = False
            k["gerekce"] = "Yönetici atadı"
            (k.get("teklif") or {})["bitis"] = 0  # yöneticinin atamasında süre işlemez
            if k.get("durum") not in KAPALI_DURUMLAR and k.get("durum") != "alindi":
                k["durum"] = "alindi"  # yeni SPY kabul edene kadar yeni çağrı
            olay(veri, f"Yönetici aktardı: {k.get('musteri', {}).get('ad') or 'Müşteri'} → {veri['spyler'][rep]['ad']}", k["id"])
            damga(veri, k)
        return k
    if yol == "api/kod":
        tel = "".join(c for c in str(istek.get("tel") or "") if c.isdigit())[-10:]
        kod = metin(istek.get("kod"), 6)
        for k in sorted(kayitlar.values(), key=lambda x: -x.get("olusma", 0)):
            if k.get("girisKodu") == kod and "".join(c for c in k.get("musteri", {}).get("tel", "") if c.isdigit())[-10:] == tel:
                return k
        raise ValueError("Kod ya da telefon eşleşmedi.")
    if yol == "api/sifirla":
        if istek.get("onay") != "evet":
            raise ValueError("Onay eksik.")
        yedek = KLASOR / "yedek"
        yedek.mkdir(exist_ok=True)
        (yedek / time.strftime("veri_%Y-%m-%d_%H%M%S.json")).write_text(json.dumps(veri, ensure_ascii=False), encoding="utf-8")
        surum = veri["surum"]
        veri.clear()
        veri.update(bos_veri())
        veri["surum"] = surum + 1
        veri["sifirlama"] = veri["surum"]  # cihazlar eski kayıtları bırakır
        olay(veri, "Test verisi sıfırlandı")
        return {}
    raise KeyError(yol)


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
            return self._yanit(200, {"surum": veri["surum"], "simdi": simdi(), "sifirlama": veri.get("sifirlama", 0),
                                     "spyler": [{**s, "aktif": aktif_mi(s), "sonGorulme": GORULME.get(s["id"], 0)} for s in veri["spyler"].values()],
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
        if yol not in ("api/cagri", "api/kayit", "api/mesaj", "api/spy", "api/aktar", "api/kod", "api/sifirla"):
            return self._yanit(404, {"hata": "Bulunamadı"})
        uzunluk = int(self.headers.get("Content-Length") or 0)
        if uzunluk > 50_000:
            return self._yanit(413, {"hata": "İstek çok büyük"})
        try:
            istek = json.loads(self.rfile.read(uzunluk) or b"{}")
            with kilit:
                veri = oku()
                sonuc = uygula(veri, yol, istek)
                yaz(veri)
            self._yanit(200, {"surum": veri["surum"], "sonuc": sonuc})
        except (KeyError, ValueError, TypeError) as e:
            self._yanit(400, {"hata": str(e).strip("'\"")})


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
    try:
        sunucu = ThreadingHTTPServer(("127.0.0.1", PORT), Isleyici)
    except OSError:
        print(f"Port {PORT} kullanımda: merkez zaten çalışıyor olabilir.", flush=True)
        return 1
    sunucu.gizli = os.environ.get("TY_YOL") or gizli_yol()

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
