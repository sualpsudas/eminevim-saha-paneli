"""TRAFİK KAPISI — bir yolculuğun o gün ve saatteki tipik trafik çarpanı (atamada varış süresi = yol süresi × çarpan).

Şu an İBB Açık Veri "Saatlik Trafik Yoğunluk Veri Seti"nden üretilen veri/trafik-carpan.json (araclar/trafik_hazirla.py):
pilot bölgedeki her geohash-6 karesi için gün tipi (hafta içi / cumartesi / pazar) × saat çarpanı. Anlık trafik DEĞİL, geçmiş aylardaki tipik trafik.
Anlık trafik gerekirse (ücretli yönlendirme servisi ya da İBB'nin lisanslı verisi) yalnız bu dosya değişir.

canli_yollar(): takip sayfası haritasındaki trafik katmanı için İBB Şehir Haritası'nın (harita.istanbul) canlı trafik segmentlerinden
pilot bölge ilçe sınırları içindeki yol parçaları (İBB rengi + anlık hız). Her zaman o anki veri; geçmiş tutulmaz (2026-11-26 kararı).
3 dk bellekte tutulur; İBB'ye ulaşılamazsa son alınan döner.
Yalnız haritada gösterilir; atamadaki varış süresi yine yukarıdaki tipik çarpanla hesaplanır.
"""
import gzip
import json
import math
import threading
import time
import urllib.parse
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


# --- Canlı yol trafiği (İBB Şehir Haritası trafik segmentleri) ---
# harita.istanbul'un kendi kullandığı adresler: önce anonim oturum anahtarı alınır, segment sorgusu bu anahtarla yapılır.
# Resmi/açık bir hizmet değil (pilot bölge denemesi için); adres değişirse katman "veri yok" der, atama etkilenmez.
OTURUM_URL = "https://sehirharitasigateway.ibb.gov.tr/auth/anonim?lang=tr"
SEGMENT_URL = "https://sehirharitasigateway.ibb.gov.tr/api/ZJmA/arcgis/rest/services/TrafikSegment/MapServer/0/query"
ANAHTAR_BASLIK = "ABC-3903258-571632"   # anahtarın hem yanıttaki alan adı hem istek başlığı
CANLI_SN = 180
_canli = {"zaman": 0, "veri": None, "anahtar": None, "dizin": {}}
DIZIN_DERECE = 0.0005   # ~50 m'lik ızgara: rota noktasına yakın segment araması
ESLESME_M = 20          # rota noktası İBB segmentine bu kadar yakınsa o segmentin anlık hızı kullanılır
_kilit = threading.Lock()
_BASLIK = {"User-Agent": "TasarrufYanimda-merkez", "Origin": "https://harita.istanbul", "Referer": "https://harita.istanbul/"}


def _getir(url, baslik=None):
    with urllib.request.urlopen(urllib.request.Request(url, headers={**_BASLIK, **(baslik or {})}), timeout=30) as r:
        veri = r.read()
    return json.loads(gzip.decompress(veri) if veri[:2] == bytes((0x1F, 0x8B)) else veri)


def _anahtar(yenile=False):
    if yenile or not _canli["anahtar"]:
        _canli["anahtar"] = _getir(OTURUM_URL)[ANAHTAR_BASLIK]
    return _canli["anahtar"]


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


def _indir():
    halkalar = _pilot_halkalar()
    if not halkalar:
        raise OSError("pilot sınırı yok")
    nok = [p for h in halkalar for p in h]
    kutu = f"{min(p[1] for p in nok)},{min(p[0] for p in nok)},{max(p[1] for p in nok)},{max(p[0] for p in nok)}"
    url = SEGMENT_URL + "?" + urllib.parse.urlencode({
        "f": "geojson", "where": "1=1", "outFields": "color,speed,tip", "geometry": kutu, "geometryType": "esriGeometryEnvelope",
        "inSR": 4326, "outSR": 4326, "spatialRel": "esriSpatialRelIntersects", "geometryPrecision": 5})
    for deneme in (0, 1):
        veri = _getir(url, {ANAHTAR_BASLIK: _anahtar(yenile=deneme == 1)})
        if "features" in veri:
            break
    else:
        raise OSError("İBB anahtarı geçersiz")
    yollar, dizin = [], {}
    for f in veri["features"]:
        g, o = f.get("geometry") or {}, f.get("properties") or {}
        hatlar = g.get("coordinates") or []
        if g.get("type") == "LineString":
            hatlar = [hatlar]
        renk = o.get("color") if isinstance(o.get("color"), int) else 0
        hiz = o.get("speed") if isinstance(o.get("speed"), (int, float)) else None
        if hiz and hiz > 0 and renk:  # rota süresi için kırpılmamış hali ızgaraya
            for hat in hatlar:
                for a, b in zip(hat, hat[1:]):
                    oge = (a[1], a[0], b[1], b[0], hiz)
                    for gx in {int(a[0] / DIZIN_DERECE), int(b[0] / DIZIN_DERECE)}:
                        for gy in {int(a[1] / DIZIN_DERECE), int(b[1] / DIZIN_DERECE)}:
                            dizin.setdefault((gx, gy), []).append(oge)
        ana = 0 if o.get("tip") == 2 else 1  # İBB: tip 1/3 ana yol (her yakınlıkta), tip 2 ara yol (yalnız yakınlaşınca)
        for hat in hatlar:
            parca = []
            for p in [(round(c[1], 5), round(c[0], 5)) for c in hat] + [None]:  # sınır dışına çıkan noktada çizgi bölünür
                if p and _icinde(p[0], p[1], halkalar):
                    parca.append(p)
                    continue
                if len(parca) > 1:
                    yollar.append([renk, hiz, parca, ana])
                parca = []
    return yollar, dizin


def canli_yollar():
    """{"zaman": 'SS:DD' (İBB'den alındığı an), "eski": bool, "yollar": [[renk 0-5, hız km/s|None, [[enlem, boylam]…], ana yol 1/0]…]}
    renk İBB'nin kendi sınıfı: 1-2 akıcı, 3 yoğun, 4 çok yoğun, 5 tıkalı, 0 veri yok."""
    with _kilit:
        if _canli["veri"] is None or time.time() - _canli["zaman"] > CANLI_SN:
            try:
                yollar, _canli["dizin"] = _indir()
                _canli["veri"] = {"zaman": time.strftime("%H:%M"), "yollar": yollar}
                _canli["zaman"] = time.time()
            except (OSError, ValueError, KeyError) as h:
                if _canli["veri"] is None:
                    return {"zaman": "", "eski": True, "yollar": [], "hata": str(h)[:120]}
                return {**_canli["veri"], "eski": True}
        return {**_canli["veri"], "eski": False}


def _uzaklik_m(lat, lng, o):
    """Nokta ile segment parçası (lat1, lng1, lat2, lng2, hız) arası metre (yerel düzlem)."""
    kx = 111320 * math.cos(math.radians(lat))
    ax, ay, bx, by = (o[1] - lng) * kx, (o[0] - lat) * 110540, (o[3] - lng) * kx, (o[2] - lat) * 110540
    dx, dy = bx - ax, by - ay
    t = 0.0 if dx == dy == 0 else max(0.0, min(1.0, -(ax * dx + ay * dy) / (dx * dx + dy * dy)))
    return math.hypot(ax + t * dx, ay + t * dy)


def nokta_hizi(lat, lng):
    """Noktaya en yakın (ESLESME_M içinde) İBB segmentinin anlık hızı (km/s) ya da None."""
    gx, gy = int(lng / DIZIN_DERECE), int(lat / DIZIN_DERECE)
    en, hiz = ESLESME_M, None
    for x in (gx - 1, gx, gx + 1):
        for y in (gy - 1, gy, gy + 1):
            for o in _canli["dizin"].get((x, y), ()):
                u = _uzaklik_m(lat, lng, o)
                if u <= en:
                    en, hiz = u, o[4]
    return hiz


def canli_rota_dk(rota):
    """yol.rota() sonucunun anlık trafikle süresi: her parça İBB segmentiyle eşleşirse o hızla, yoksa yol servisinin süresiyle.
    Döner {"dk", "serbestDk", "kapsama" (eşleşen mesafe oranı)} ya da canlı veri yoksa None."""
    canli_yollar()  # 3 dk'dan eskiyse tazeler
    if not _canli["dizin"] or not rota:
        return None
    toplam = serbest = eslesen = uzun = 0.0
    k = rota["nokta"]
    for i, (m, sn) in enumerate(zip(rota["mesafe"], rota["sure"])):
        (la, lo), (lb, lob) = k[i], k[i + 1]
        hiz = nokta_hizi((la + lb) / 2, (lo + lob) / 2) if m > 0 else None
        toplam += m / (hiz / 3.6) if hiz else sn
        serbest += sn
        uzun += m
        eslesen += m if hiz else 0
    return {"dk": round(toplam / 60, 1), "serbestDk": round(serbest / 60, 1), "kapsama": round(eslesen / uzun, 2) if uzun else 0}
