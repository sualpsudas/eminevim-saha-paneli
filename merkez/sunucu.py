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

# Test için 4 kayıtlı SPY; konumlar sabit (hizmet bölgesi: Ataşehir, Üsküdar, Ümraniye)
SPYLER = [
    {"id": "s1", "ad": "Onur Kaya", "sube": "Ataşehir Şubesi", "lat": 40.9923, "lng": 29.1244, "yer": "Atatürk Mah., Ataşehir"},
    {"id": "s2", "ad": "Derya Aksoy", "sube": "Üsküdar Şubesi", "lat": 41.0255, "lng": 29.0160, "yer": "Mimar Sinan Mah., Üsküdar"},
    {"id": "s3", "ad": "Berk Cengiz", "sube": "Ümraniye Şubesi", "lat": 41.0256, "lng": 29.1100, "yer": "Namık Kemal Mah., Ümraniye"},
    {"id": "s4", "ad": "Selin Arslan", "sube": "Üsküdar Şubesi", "lat": 41.0180, "lng": 29.0600, "yer": "Bulgurlu Mah., Üsküdar"},
]
SPY_IDLER = {s["id"] for s in SPYLER}
KAPALI_DURUMLAR = {"tamamlandi", "iptal"}
DURUM_AD = {"alindi": "yeni çağrı", "atandi": "SPY kabul etti", "netlesti": "müşteri saati onayladı", "yolda": "SPY yola çıktı",
            "gorusme": "SPY yolda", "gorusmede": "kapıda doğrulandı, görüşmede", "tamamlandi": "görüşme tamamlandı", "iptal": "iptal edildi"}
STATIK_UZANTI = {".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".css": "text/css; charset=utf-8",
                 ".json": "application/json; charset=utf-8", ".png": "image/png", ".jpg": "image/jpeg", ".svg": "image/svg+xml",
                 ".webp": "image/webp", ".ico": "image/x-icon"}
STATIK_KLASOR = ("assets/", "vendor/")
STATIK_KOK = {UYGULAMA, "index.html", "appointment.js", "assignment.js", "org-data.js", "support.js", "konum-sec.html",
              "rota.html", "map.html", "manifest.json", "eminevim-qr.png", "canli.js"}


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


def en_yakin(veri, konum, haric=()):
    """Molada olmayan SPY'ler arasında müşteriye en yakını; eşitlikte açık çağrısı az olan."""
    adaylar = [s for s in veri["spyler"].values() if s["durum"] != "molada" and s["id"] not in haric] or \
              [s for s in veri["spyler"].values() if s["id"] not in haric] or list(veri["spyler"].values())
    return min(adaylar, key=lambda s: (round(km(s, konum), 3), acik_sayi(veri, s["id"])))


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
        spy = en_yakin(veri, konum)
        k.update({"repId": spy["id"], "durum": "alindi", "atanma": simdi(), "uzaklikKm": round(km(spy, konum), 1)})
        k["musteri"] = {"ad": metin(m.get("ad"), 80), "tel": metin(m.get("tel"), 20), "ekBilgi": m.get("ekBilgi") if isinstance(m.get("ekBilgi"), dict) else None}
        k["mesajlar"] = []
        k["olusma"] = simdi()
        kayitlar[k["id"]] = k
        damga(veri, k)
        olay(veri, f"Yeni çağrı: {k['musteri']['ad'] or 'Müşteri'} ({k.get('yer') or ''}) → {spy['ad']}, {str(k['uzaklikKm']).replace('.', ',')} km", k["id"])
        return k
    if yol == "api/kayit":
        k = temiz_kayit(istek.get("kayit"))
        eski = kayitlar.get(k["id"])
        if not eski:
            raise ValueError("Kayıt bulunamadı.")
        if not k.get("repId") or k["repId"] not in SPY_IDLER:
            k["repId"] = eski.get("repId")  # müşteri tarafı kabulden önce SPY'yi görmez, boş gönderir
        if k.get("durum") != eski.get("durum"):
            spy = veri["spyler"].get(k.get("repId") or eski.get("repId"), {})
            olay(veri, f"{eski.get('musteri', {}).get('ad') or 'Müşteri'}: {DURUM_AD.get(k.get('durum'), k.get('durum'))} ({spy.get('ad', '')})", k["id"])
        if k.get("repId") != eski.get("repId"):
            k["eskiRepler"] = sorted(set(eski.get("eskiRepler", [])) | {eski.get("repId")})
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
        if k and not rep:  # SPY "Devret" dedi: kendisi ve önceki SPY'ler dışında en yakın
            haric = set(k.get("eskiRepler", [])) | {k.get("repId")}
            rep = en_yakin(veri, k.get("konum") or veri["spyler"][k["repId"]], haric if len(haric) < len(SPY_IDLER) else {k.get("repId")})["id"]
        if not k or rep not in SPY_IDLER:
            raise ValueError("Aktarım eksik.")
        if k.get("repId") != rep:
            k["eskiRepler"] = sorted(set(k.get("eskiRepler", [])) | {k.get("repId")})
            k["repId"] = rep
            if k.get("durum") not in KAPALI_DURUMLAR and k.get("durum") != "alindi":
                k["durum"] = "alindi"  # yeni SPY kabul edene kadar yeni çağrı
            olay(veri, f"{'Devredildi' if not istek.get('repId') else 'Takip sayfasından aktarıldı'}: {k.get('musteri', {}).get('ad') or 'Müşteri'} → {veri['spyler'][rep]['ad']}", k["id"])
            damga(veri, k)
        return k
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

            def gorur(k):  # personel kendi çağrılarını (devrettikleri dahil), müşteri kendi kaydını, takip sayfası hepsini
                if spy:
                    return k.get("repId") == spy or spy in k.get("eskiRepler", [])
                return k["id"] in ids if ids else "hepsi" in q
            return self._yanit(200, {"surum": veri["surum"], "simdi": simdi(), "sifirlama": veri.get("sifirlama", 0),
                                     "spyler": [{**s, "sonGorulme": GORULME.get(s["id"], 0)} for s in veri["spyler"].values()],
                                     "kayitlar": [k for k in veri["kayitlar"].values() if k.get("surum", 0) > surum and gorur(k)],
                                     "olaylar": veri["olaylar"][:80] if "hepsi" in q else []})
        dosya = self._statik(yol)
        if not dosya:
            return self._yanit(404, {"hata": "Bulunamadı"})
        icerik = dosya.read_bytes()
        if dosya.name == UYGULAMA:
            icerik = icerik.replace(b"<head>", b'<head>\n<script>window.TY_CANLI={api:"api/"};</script>\n<script src="./canli.js"></script>', 1)
        self._yanit(200, icerik, STATIK_UZANTI.get(dosya.suffix.lower(), "application/octet-stream"))

    def do_POST(self):
        yol = self._yol()
        if yol not in ("api/cagri", "api/kayit", "api/mesaj", "api/spy", "api/aktar", "api/sifirla"):
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
    PID.write_text(str(os.getpid()))
    print(f"Hazır: http://127.0.0.1:{PORT}/{sunucu.gizli}/", flush=True)
    try:
        sunucu.serve_forever()
    finally:
        PID.unlink(missing_ok=True)


if __name__ == "__main__":
    sys.exit(main())
