"""YOL KAPISI — noktalardan müşteriye araçla yol mesafesi (km) ve trafiksiz süre (dk); atamada uzaklık bundan hesaplanır.

Şu an OSRM genel sunucusu (uygulama/servisler.js'teki aynı adres; prototip, kullanım sınırı belirsiz). Tek istekte tüm noktalar ölçülür.
Servis yanıt vermezse kuş uçuşuna düşülür (km × 1,3 yol payı, 25 km/sa) ve sonuç "kus" kaynağıyla işaretlenir; 60 sn yeniden denenmez.
Gerçek sistemde şirketin ya da ücretli bir yönlendirme servisi yalnız bu dosyanın arkasına girer.
"""
import json
import threading
import time
import urllib.request

from .yardim import km

ADRES = "https://router.project-osrm.org/table/v1/driving/"
ZAMAN_ASIMI = 3       # sn
YOL_PAYI, KUS_HIZ = 1.3, 25  # servis yokken: kuş uçuşu × pay, km/sa
_kilit = threading.Lock()
_onbellek = {}        # ((lat,lng),(lat,lng)) -> (km, dk)
_hata_zamani = 0.0


def _anahtar(n):
    return (round(n["lat"], 4), round(n["lng"], 4))  # ~10 m


def _kus(a, b):
    d = km(a, b)
    return {"km": round(d * YOL_PAYI, 1), "dk": round(d * YOL_PAYI / KUS_HIZ * 60, 1), "kaynak": "kus"}


def _iste(kaynaklar, hedef):
    nk = kaynaklar + [hedef]
    adres = (ADRES + ";".join(f"{n['lng']:.5f},{n['lat']:.5f}" for n in nk)
             + f"?sources={';'.join(str(i) for i in range(len(kaynaklar)))}&destinations={len(kaynaklar)}&annotations=distance,duration")
    with urllib.request.urlopen(urllib.request.Request(adres, headers={"User-Agent": "TasarrufYanimda-test"}), timeout=ZAMAN_ASIMI) as r:
        v = json.load(r)
    if v.get("code") != "Ok":
        raise ValueError(v.get("code"))
    return [(m[0], s[0]) for m, s in zip(v["distances"], v["durations"])]


def olc(kaynaklar, hedef):
    """Her kaynak noktadan hedefe {"km", "dk", "kaynak": "yol" | "kus"} (sıra korunur)."""
    global _hata_zamani
    h = _anahtar(hedef)
    with _kilit:
        eksik = [n for n in kaynaklar if (_anahtar(n), h) not in _onbellek]
        servis_acik = time.time() - _hata_zamani > 60
    if eksik and servis_acik:
        tekil = list({_anahtar(n): n for n in eksik}.values())
        try:
            for i in range(0, len(tekil), 90):  # genel sunucu en fazla 100 nokta
                parca = tekil[i:i + 90]
                for n, (m, s) in zip(parca, _iste(parca, hedef)):
                    if m is not None and s is not None:
                        with _kilit:
                            if len(_onbellek) > 20000:
                                _onbellek.clear()
                            _onbellek[(_anahtar(n), h)] = (round(m / 1000, 1), round(s / 60, 1))
        except Exception:
            _hata_zamani = time.time()
    sonuc = []
    for n in kaynaklar:
        with _kilit:
            v = _onbellek.get((_anahtar(n), h))
        sonuc.append({"km": v[0], "dk": v[1], "kaynak": "yol"} if v else _kus(n, hedef))
    return sonuc


ROTA_ADRES = "https://router.project-osrm.org/route/v1/driving/"
_rota_onbellek = {}   # ((lat,lng),(lat,lng)) -> rota


def rota(a, b):
    """a → b araç rotası: {"nokta": [(enlem, boylam)…], "mesafe": [m…], "sure": [sn…]} (parça başına) ya da servis yoksa None.
    Anlık trafikli süre için (trafik.canli_rota_dk); tek istek, 3 sn zaman aşımı, 60 sn hata bekleme olc() ile ortak."""
    global _hata_zamani
    anahtar = (_anahtar(a), _anahtar(b))
    with _kilit:
        if anahtar in _rota_onbellek:
            return _rota_onbellek[anahtar]
        if time.time() - _hata_zamani <= 60:
            return None
    adres = (ROTA_ADRES + f"{a['lng']:.5f},{a['lat']:.5f};{b['lng']:.5f},{b['lat']:.5f}"
             + "?overview=full&geometries=geojson&annotations=distance,duration")
    try:
        with urllib.request.urlopen(urllib.request.Request(adres, headers={"User-Agent": "TasarrufYanimda-test"}), timeout=ZAMAN_ASIMI) as r:
            v = json.load(r)
        if v.get("code") != "Ok":
            raise ValueError(v.get("code"))
        y = v["routes"][0]
        sonuc = {"nokta": [(c[1], c[0]) for c in y["geometry"]["coordinates"]],
                 "mesafe": y["legs"][0]["annotation"]["distance"], "sure": y["legs"][0]["annotation"]["duration"]}
    except Exception:
        _hata_zamani = time.time()
        return None
    with _kilit:
        if len(_rota_onbellek) > 2000:
            _rota_onbellek.clear()
        _rota_onbellek[anahtar] = sonuc
    return sonuc
