"""TRAFİK KAPISI — bir yolculuğun o gün ve saatteki tipik trafik çarpanı (atamada varış süresi = yol süresi × çarpan).

Şu an İBB Açık Veri "Saatlik Trafik Yoğunluk Veri Seti"nden üretilen veri/trafik-carpan.json (araclar/trafik_hazirla.py):
pilot bölgedeki her geohash-6 karesi için gün tipi (hafta içi / cumartesi / pazar) × saat çarpanı. Anlık trafik DEĞİL, geçmiş aylardaki tipik trafik.
Anlık trafik gerekirse (ücretli yönlendirme servisi ya da İBB'nin lisanslı verisi) yalnız bu dosya değişir.

canli_yollar(): takip sayfası haritasındaki trafik katmanı için İBB Şehir Haritası'nın (harita.istanbul) herkese açık canlı trafik
vektör karolarından (basemap.ibb.gov.tr/traffic.mbtiles, birkaç dakikada bir güncellenir) pilot bölge ilçe sınırları içindeki yol
parçaları. Renk 1 akıcı … 5 çok yoğun, 0 veri yok. 3 dk bellekte tutulur; İBB'ye ulaşılamazsa son alınan döner.
Yalnız haritada gösterilir; atamadaki varış süresi yine yukarıdaki tipik çarpanla hesaplanır.
"""
import gzip
import json
import math
import threading
import time
import urllib.request

from .ayarlar import KOK

DOSYA = KOK / "veri" / "trafik-carpan.json"
_B32 = "0123456789bcdefghjkmnpqrstuvwxyz"
_veri = None


def _yukle():
    global _veri
    if _veri is None:
        try:
            _veri = json.loads(DOSYA.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            _veri = {}  # dosya yoksa trafik çarpanı 1 (trafiksiz süre)
    return _veri


def geohash(lat, lng, uzunluk=6):
    la, lo, bit, ch, cift, sonuc = [-90.0, 90.0], [-180.0, 180.0], 0, 0, True, ""
    while len(sonuc) < uzunluk:
        ara, deger = (lo, lng) if cift else (la, lat)
        orta = (ara[0] + ara[1]) / 2
        if deger >= orta:
            ch, ara[0] = ch * 2 + 1, orta
        else:
            ch, ara[1] = ch * 2, orta
        cift, bit = not cift, bit + 1
        if bit == 5:
            sonuc, bit, ch = sonuc + _B32[ch], 0, 0
    return sonuc


def gun_saat(tarih=None, saat=None):
    """(gün tipi, saat): tarih 'YYYY-AA-GG', saat 'SS:DD'; boşsa şu an."""
    t = time.localtime()
    if tarih:
        try:
            t = time.strptime(f"{tarih} {saat or '12:00'}", "%Y-%m-%d %H:%M")
        except ValueError:
            pass
    g = t.tm_wday
    return ("hi" if g < 5 else "cmt" if g == 5 else "pzr"), t.tm_hour


def carpan(a, b, gun, saat):
    """a → b yolculuğunun çarpanı: düz hat üzerindeki 5 noktanın (başlangıç, ara noktalar, varış) karelerinin ortalaması.
    Kare veride yoksa pilot bölge geneli; dosya yoksa 1."""
    v = _yukle()
    if not v:
        return 1.0
    genel = v["genel"][gun][saat]
    degerler = []
    for i in range(5):
        f = i / 4
        h = v["hucre"].get(geohash(a["lat"] + (b["lat"] - a["lat"]) * f, a["lng"] + (b["lng"] - a["lng"]) * f))
        degerler.append(h[gun][saat] if h else genel)
    return round(sum(degerler) / len(degerler), 2)


def bilgi():
    v = _yukle()
    return {"kaynak": v.get("kaynak", ""), "donem": v.get("donem", []), "kare": len(v.get("hucre", {})), "var": bool(v)}


# --- Canlı yol trafiği (İBB vektör karoları) ---
KARO_URL = "https://basemap.ibb.gov.tr/traffic.mbtiles/{z}/{x}/{y}.pbf"
KARO_Z = 13
CANLI_SN = 180
_canli = {"zaman": 0, "veri": None}
_kilit = threading.Lock()


def _vint(b, i):
    r = s = 0
    while True:
        c = b[i]
        i += 1
        r |= (c & 0x7F) << s
        s += 7
        if c < 0x80:
            return r, i


def _alanlar(b):
    """Protobuf alanları: (alan no, değer); değer sayı ya da bayt dizisi."""
    i = 0
    while i < len(b):
        k, i = _vint(b, i)
        tur = k & 7
        if tur == 0:
            v, i = _vint(b, i)
        elif tur == 2:
            n, i = _vint(b, i)
            v, i = b[i:i + n], i + n
        elif tur in (1, 5):
            n = 8 if tur == 1 else 4
            v, i = b[i:i + n], i + n
        else:
            raise ValueError("protobuf")
        yield k >> 3, v


def _paket(b):
    out, i = [], 0
    while i < len(b):
        v, i = _vint(b, i)
        out.append(v)
    return out


def _zz(n):
    return (n >> 1) ^ -(n & 1)


def karo_coz(veri, z, x, y):
    """Mapbox vektör karosu → [(özellikler, [çizgi [(enlem, boylam)…]…])…] (yalnız çizgiler)."""
    if veri[:2] == b"\x1f\x8b":  # gzip
        veri = gzip.decompress(veri)
    sonuc = []
    for alan, katman in _alanlar(veri):
        if alan != 3:
            continue
        anahtar, deger, ogeler, olcek = [], [], [], 4096
        for a, v in _alanlar(katman):
            if a == 3:
                anahtar.append(v.decode())
            elif a == 4:
                d = None
                for a2, w in _alanlar(v):
                    d = w.decode() if a2 == 1 else _zz(w) if a2 == 6 else w
                deger.append(d)
            elif a == 2:
                ogeler.append(v)
            elif a == 5:
                olcek = v
        for oge in ogeler:
            etiket, geo, tip = [], [], 0
            for a, v in _alanlar(oge):
                if a == 2:
                    etiket = _paket(v)
                elif a == 3:
                    tip = v
                elif a == 4:
                    geo = _paket(v)
            if tip != 2:
                continue
            ozellik = {anahtar[etiket[j]]: deger[etiket[j + 1]] for j in range(0, len(etiket) - 1, 2)}
            cizgiler, hat, cx, cy, j = [], [], 0, 0, 0
            while j < len(geo):
                komut, n = geo[j] & 7, geo[j] >> 3
                j += 1
                if komut == 7:
                    continue
                if komut == 1 and hat:
                    cizgiler.append(hat)
                    hat = []
                for _ in range(n):
                    cx += _zz(geo[j])
                    cy += _zz(geo[j + 1])
                    j += 2
                    lng = (x + cx / olcek) / 2 ** z * 360 - 180
                    lat = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * (y + cy / olcek) / 2 ** z))))
                    hat.append((round(lat, 4), round(lng, 4)))
            if hat:
                cizgiler.append(hat)
            sonuc.append((ozellik, cizgiler))
    return sonuc


def _pilot_halkalar():
    try:
        t = (KOK / "assets" / "pilot-sinirlar.js").read_text(encoding="utf-8")
        return [h for i in json.loads(t[t.index("{"):t.rindex("}") + 1])["ilceler"] for h in i["halkalar"]]
    except (OSError, ValueError, KeyError):
        return []


def _icinde(lat, lng, halkalar):
    ic = False
    for h in halkalar:
        j = len(h) - 1
        for i in range(len(h)):
            (ya, xa), (yb, xb) = h[i], h[j]
            if (ya > lat) != (yb > lat) and lng < (xb - xa) * (lat - ya) / (yb - ya) + xa:
                ic = not ic
            j = i
    return ic


def _karolar(halkalar):
    noktalar = [p for h in halkalar for p in h]
    def xy(lat, lng):
        n = 2 ** KARO_Z
        return int((lng + 180) / 360 * n), int((1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n)
    x0, y0 = xy(max(p[0] for p in noktalar), min(p[1] for p in noktalar))
    x1, y1 = xy(min(p[0] for p in noktalar), max(p[1] for p in noktalar))
    return [(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)]


def _indir():
    halkalar = _pilot_halkalar()
    if not halkalar:
        raise OSError("pilot sınırı yok")
    yollar = []
    for x, y in _karolar(halkalar):
        istek = urllib.request.Request(KARO_URL.format(z=KARO_Z, x=x, y=y), headers={"User-Agent": "TasarrufYanimda-merkez"})
        with urllib.request.urlopen(istek, timeout=15) as r:
            veri = r.read()
        for ozellik, cizgiler in karo_coz(veri, KARO_Z, x, y):
            renk = ozellik.get("color") if isinstance(ozellik.get("color"), int) else 0
            for hat in cizgiler:
                parca = []
                for p in hat + [None]:  # sınır dışına çıkan noktada çizgi bölünür
                    if p and _icinde(p[0], p[1], halkalar):
                        parca.append(p)
                        continue
                    if len(parca) > 1:
                        orta = parca[len(parca) // 2]
                        yollar.append([renk, geohash(orta[0], orta[1]), parca])
                    parca = []
    return yollar


def canli_yollar():
    """{"zaman": 'SS:DD' (İBB'den alındığı an), "eski": bool, "yollar": [[renk, geohash-6, [[enlem, boylam]…]]…]}"""
    with _kilit:
        if _canli["veri"] is None or time.time() - _canli["zaman"] > CANLI_SN:
            try:
                _canli["veri"] = {"zaman": time.strftime("%H:%M"), "yollar": _indir()}
                _canli["zaman"] = time.time()
            except (OSError, ValueError) as h:
                if _canli["veri"] is None:
                    return {"zaman": "", "eski": True, "yollar": [], "hata": str(h)[:120]}
                return {**_canli["veri"], "eski": True}
        return {**_canli["veri"], "eski": False}
