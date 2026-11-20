"""HTTP SUNUCUSU — adresler, dosya sunma, başlat/durdur. İş kuralı yok (kurallar islemler.py ve kapılarda).

Adresler (hepsi gizli yolun altında: /<gizli_yol.txt>/...):
  GET  api/durum?surum=&spy=|ids=|hepsi   değişen çağrılar + SPY özetleri (uygulama 2-3 sn'de bir yoklar)
  GET  api/anahtar                        bildirim açık anahtarı
  POST api/cagri, api/kayit, ...          islemler.YOLLAR
  POST api/abone, api/abone-sil           bildirim aboneliği (bildirim.py)
  GET  takip                              yönetici takip sayfası (merkez/takip.html)
  GET  <uygulama dosyaları>               depo kökünden (ayarlar.STATIK_*); uygulama sayfasına window.TY_CANLI eklenir,
                                          böylece GitHub Pages'teki kopya gösteri modunda kalır, buradaki merkeze bağlanır.
"""
import gzip
import json
import re
import os
import secrets
import signal
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote

from . import bildirim, depo
from .atama import sureleri_denetle
from .ayarlar import ANAHTAR, KLASOR, KOK, PID, PORT, STATIK_KLASOR, STATIK_KOK, STATIK_UZANTI, SURUM_DOSYALARI, UYGULAMA
from .islemler import GORULME, YOLLAR, bugun_sayilar, spy_ozet, uygula
from .musteri import YazilanHata
from .personel import SPY_IDLER
from .yardim import simdi


def uygulama_surumu():
    """Uygulama dosyaları değişince (git pull) değişir; açık uygulamalar "Yeni sürüm hazır · Yenile" şeridi gösterir."""
    try:
        return str(max(int((KOK / ad).stat().st_mtime) for ad in SURUM_DOSYALARI))
    except OSError:
        return ""


SIKISTIRILAN = {"text/html", "text/javascript", "application/javascript", "text/css", "application/json", "image/svg+xml", "font/ttf"}


class Isleyici(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _yanit(self, kod, govde, tur="application/json; charset=utf-8", etag=None):
        veri = govde if isinstance(govde, bytes) else json.dumps(govde, ensure_ascii=False).encode("utf-8")
        if etag and self.headers.get("If-None-Match") == etag:  # değişmemiş dosya: gövde gönderilmez (telefonda hızlı açılış)
            self.send_response(304)
            self.send_header("ETag", etag)
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            return
        sikistir = len(veri) > 1024 and "gzip" in self.headers.get("Accept-Encoding", "") and tur.split(";")[0] in SIKISTIRILAN
        if sikistir:
            veri = gzip.compress(veri, 6)
        self.send_response(kod)
        self.send_header("Content-Type", tur)
        self.send_header("Content-Length", str(len(veri)))
        if sikistir:
            self.send_header("Content-Encoding", "gzip")
        if etag:
            self.send_header("ETag", etag)
        self.send_header("Cache-Control", "no-cache" if etag else "no-store")
        self.end_headers()
        self.wfile.write(veri)

    def _yol(self):
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

    def _video(self, dosya):
        # iPhone (WebKit) video için 'Range' (parça) isteği ister; 206 + Content-Range yanıtı
        boyut = dosya.stat().st_size
        bas, son, kod = 0, boyut - 1, 200
        m = re.match(r"bytes=(\d*)-(\d*)$", self.headers.get("Range", "").strip())
        if m and (m.group(1) or m.group(2)):
            if m.group(1):
                bas = int(m.group(1))
                son = min(int(m.group(2)), boyut - 1) if m.group(2) else boyut - 1
            else:
                bas = max(0, boyut - int(m.group(2)))
            if bas >= boyut or bas > son:
                self.send_response(416)
                self.send_header("Content-Range", "bytes */%d" % boyut)
                self.end_headers()
                return
            kod = 206
        with open(dosya, "rb") as f:
            f.seek(bas)
            veri = f.read(son - bas + 1)
        self.send_response(kod)
        self.send_header("Content-Type", "video/mp4")
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(len(veri)))
        if kod == 206:
            self.send_header("Content-Range", "bytes %d-%d/%d" % (bas, son, boyut))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        try:
            self.wfile.write(veri)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def _durum(self):
        q = parse_qs(self.path.partition("?")[2])
        try:
            surum = int((q.get("surum") or ["0"])[0])
        except ValueError:
            surum = 0
        spy = (q.get("spy") or [""])[0]
        ids = set(",".join(q.get("ids") or []).split(",")) - {""}
        if spy in SPY_IDLER:
            GORULME[spy] = simdi()  # uygulaması açık personel (takip sayfası için)
        with depo.kilit:
            veri = depo.oku()
            if sureleri_denetle(veri):
                depo.yaz(veri)

        def gorur(k):  # personel kendi çağrılarını (devrettikleri dahil), müşteri kendi kaydını, takip sayfası hepsini
            if spy:
                return k.get("repId") == spy or spy in k.get("eskiRepler", [])
            return k["id"] in ids if ids else "hepsi" in q
        return {"surum": veri["surum"], "simdi": simdi(), "sifirlama": veri.get("sifirlama", 0), "uygulama": uygulama_surumu(),
                "spyler": [spy_ozet(veri, s) for s in veri["spyler"].values()],
                "bugun": bugun_sayilar(veri),
                "kayitlar": [k for k in veri["kayitlar"].values() if k.get("surum", 0) > surum and gorur(k)],
                "olaylar": veri["olaylar"][:80] if "hepsi" in q else []}

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
            return self._yanit(200, {"anahtar": bildirim.VAPID_ACIK})
        if yol == "sw.js":  # merkezde önbelleksiz, yalnız bildirim gösteren servis çalışanı (Pages'teki sw.js değil)
            return self._yanit(200, (KLASOR / "canli-sw.js").read_bytes(), "text/javascript; charset=utf-8")
        if yol == "api/durum":
            return self._yanit(200, self._durum())
        dosya = self._statik(yol)
        if not dosya:
            return self._yanit(404, {"hata": "Bulunamadı"})
        if dosya.suffix.lower() == ".mp4":
            return self._video(dosya)
        icerik = dosya.read_bytes()
        if dosya.name == UYGULAMA or dosya.parent.name == "web-basvuru" and dosya.suffix == ".html":
            on = ("/" + self.server.gizli + "/").encode()  # tam yol: web formu kopyasında <base> eminevim.com'u gösterir
            icerik = icerik.replace(b"<head>", b'<head>\n<script>window.TY_CANLI={api:"' + on + b'api/"};</script>\n<script src="' + on
                                    + b'uygulama/canli.js"></script>', 1)
        durum = dosya.stat()
        self._yanit(200, icerik, STATIK_UZANTI.get(dosya.suffix.lower(), "application/octet-stream"),
                    etag='"%x-%x-%x"' % (durum.st_mtime_ns, durum.st_size, len(icerik)))

    def do_POST(self):
        yol = self._yol()
        if yol in ("api/abone", "api/abone-sil"):
            return self._abone(yol)
        if yol not in YOLLAR:
            return self._yanit(404, {"hata": "Bulunamadı"})
        uzunluk = int(self.headers.get("Content-Length") or 0)
        if uzunluk > 50_000:
            return self._yanit(413, {"hata": "İstek çok büyük"})
        try:
            istek = json.loads(self.rfile.read(uzunluk) or b"{}")
            with depo.kilit:
                veri = depo.oku()
                try:
                    sonuc = uygula(veri, yol, istek)
                except YazilanHata:
                    depo.yaz(veri)
                    raise
                depo.yaz(veri)
            self._yanit(200, {"surum": veri["surum"], "sonuc": sonuc})
        except (KeyError, ValueError, TypeError) as e:
            self._yanit(400, {"hata": str(e).strip("'\"")})

    def _abone(self, yol):
        uzunluk = int(self.headers.get("Content-Length") or 0)
        if uzunluk > 5_000:
            return self._yanit(413, {"hata": "İstek çok büyük"})
        try:
            self._yanit(200, {"sonuc": bildirim.abone_isle(yol, json.loads(self.rfile.read(uzunluk) or b"{}"))})
        except (KeyError, ValueError, TypeError, AttributeError) as e:
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
    with depo.kilit:
        depo.oku()
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
    bildirim.baslat()

    def bekci():
        while True:
            time.sleep(5)
            with depo.kilit:
                veri = depo.oku()
                if sureleri_denetle(veri):
                    depo.yaz(veri)
    threading.Thread(target=bekci, daemon=True).start()
    PID.write_text(str(os.getpid()))
    print(f"Hazır: http://127.0.0.1:{PORT}/{sunucu.gizli}/", flush=True)
    try:
        sunucu.serve_forever()
    finally:
        PID.unlink(missing_ok=True)
