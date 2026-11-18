"""Ortak küçük yardımcılar (başka modüle bağımlı değil)."""
import math
import time


def simdi():
    return int(time.time() * 1000)


def bugun():
    return time.strftime("%Y-%m-%d")


def saat_yaz(ms):
    return time.strftime("%H:%M", time.localtime(ms / 1000)) if ms else ""


def dakika(saat):
    try:
        h, m = str(saat).split(":")[:2]
        return int(h) * 60 + int(m)
    except ValueError:
        return None


def metin(deger, uzunluk=1000):
    return str(deger or "").strip()[:uzunluk]


def tel_temiz(deger):
    return "".join(c for c in str(deger or "") if c.isdigit())[-10:]


def km(a, b):
    r = math.radians
    h = math.sin(r(b["lat"] - a["lat"]) / 2) ** 2 + math.cos(r(a["lat"])) * math.cos(r(b["lat"])) * math.sin(r(b["lng"] - a["lng"]) / 2) ** 2
    return 6371 * 2 * math.atan2(math.sqrt(h), math.sqrt(1 - h))


def olay(veri, metin_, kayit_id=""):
    """Takip sayfasındaki "Son olaylar" (en yeni 200)."""
    veri["olaylar"] = ([{"t": simdi(), "metin": metin_, "id": kayit_id}] + veri["olaylar"])[:200]


def damga(veri, kayit):
    """Kayıt değişti: sürüm artar, cihazlar yalnız değişeni çeker."""
    veri["surum"] += 1
    kayit["surum"] = veri["surum"]
    kayit["guncelleme"] = simdi()
