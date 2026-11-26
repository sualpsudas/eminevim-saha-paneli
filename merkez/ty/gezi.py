"""Hareketli örnek SPY'lerin "dur-kalk" saha günü (2026-11-26).

Her hareketli SPY rastgele bir hedef seçer (pilot bölge + komşu ilçeler, tabanından en çok 8 km) → oraya en hızlı rotayla, yoldaki İBB anlık hızıyla gider
(atama.en_hizli_rota + trafik.zamanli_rota, sunumdaki yola çıkışla aynı) → varınca 3-10 dk durur ("ziyarette") → yeni hedef.
Süreler sunumdaki gibi hızlandırılmış: gerçek 1 dk = 3 sn (sunum.YOL_SN_DK). Plan yalnız bellekte tutulur (veri.json'a yazılmaz);
merkez yeniden başlayınca SPY bulunduğu yerden yeniden başlar. Çağrı alıp yola çıkınca (don/yolda/görüşme) ya da yönetici haritada
taşıyınca gezi biter; çağrı kapanınca SPY son yerinden (müşterinin adresi) devam eder. Konum: konum.py konum_ve_kaynak → gezi.konum;
takip sayfası aynı rotayı spy_ozet'teki geziRota ile aynı formülle canlandırır.

Gez / Dur (2026-11-26): takip sayfasında SPY'ye tıklayınca. veri["geziAcik"][id] örnek SPY'lerin varsayılanını (s["gezi"]) ezer;
gerçek SPY'ler de gezdirilebilir (telefondan canlı konum gelen hariç). Dur: SPY bulunduğu yerde kalır (elleKonum).
Hedef duruma göre seçilir (_sec): teklif bekliyorsa yerinde bekler · günlük sınırı dolduysa tabanına döner ·
yakında kimsenin almadığı çağrı varsa ona doğru yaklaşır · tabanından çok uzaklaştıysa geri döner · yoksa rastgele saha ziyareti.
"""
import math
import random
import threading
import time

from .yardim import simdi

HIZ_SN_DK = 3                 # gerçek 1 dk = sunumda 3 sn (sunum.YOL_SN_DK ile aynı)
DURAK_DK = (3, 10)            # hedefte bekleme (gerçek dk; 2026-11-26: 10-30 → 3-10, haritada uzun duruş akıcı görünmüyordu)
HEDEF_M = (1200, 5000)        # yeni hedef bulunduğu yerden bu kadar uzakta (kuş uçuşu)
EV_M = 8000                   # tabanından (kayıtlı yeri) en çok bu kadar uzaklaşır; uzaklaştıkça hedefler geri çeker
TUR_SN = 2                    # planlayıcı bu sıklıkla bakar
TALEP_M = 6000                # bu kadar yakındaki bekleyen çağrıya doğru yaklaşır
_durum = {}                   # id → {"r": [[enlem, boylam, varış sn]…], "bas": ms, "sure": ms, "bit": ms (durak sonu), "neden": metin}
_kilit = threading.Lock()


def _m(a, b):
    return math.hypot((b[0] - a[0]) * 110540, (b[1] - a[1]) * 111320 * math.cos(math.radians(a[0])))


def konum(spy_id, t_ms=None):
    """Planı olan hareketli SPY'nin o anki yeri {"lat", "lng"} ya da None (plan yoksa çağıran eski düzene düşer)."""
    with _kilit:
        d = _durum.get(spy_id)
    if not d:
        return None
    r = d["r"]
    p = min(1.0, max(0.0, ((t_ms if t_ms is not None else simdi()) - d["bas"]) / (d["sure"] or 1)))
    hedef = p * r[-1][2]
    i = next((j for j in range(1, len(r)) if r[j][2] >= hedef), len(r) - 1)
    a, b = r[i - 1], r[i]
    f = (hedef - a[2]) / (b[2] - a[2]) if b[2] > a[2] else 1
    return {"lat": a[0] + (b[0] - a[0]) * f, "lng": a[1] + (b[1] - a[1]) * f}


def ozet(spy_id):
    """Takip sayfası için: {"r", "bas", "sure", "bit"} ya da None."""
    with _kilit:
        d = _durum.get(spy_id)
        return dict(d) if d else None


def _hedef(ev, bas):
    """Yeni hedef: trafik katmanının alanı içinde (pilot + komşu ilçeler; 2026-11-26: pilot bölge dışına da çıkar), bulunduğu yerden
    HEDEF_M uzakta ve tabanından (SPY'nin kayıtlı yeri) en çok EV_M uzakta. Denizi ve alan dışını ilçe sınırı eler."""
    from . import trafik
    halkalar = trafik._sinir_halkalar()
    if not halkalar:
        return None
    for _ in range(80):
        aci, m = random.uniform(0, 2 * math.pi), random.uniform(*HEDEF_M)
        h = (bas[0] + m * math.sin(aci) / 110540, bas[1] + m * math.cos(aci) / (111320 * math.cos(math.radians(bas[0]))))
        if _m(ev, h) <= EV_M and trafik._icinde(h[0], h[1], halkalar):
            return {"lat": h[0], "lng": h[1]}
    return None


def acik(veri, s):
    """SPY geziyor mu: yöneticinin Gez/Dur seçimi, yoksa örnek SPY'nin varsayılanı."""
    o = (veri.get("geziAcik") or {}).get(s["id"])
    return bool(s.get("gezi")) if o is None else bool(o)


def bekle(spy_id, nokta, sn=0, neden=""):
    """SPY'yi verilen noktada durdurur (sn saniye sonra planlayıcı yeni hedef seçer)."""
    t = simdi()
    with _kilit:
        _durum[spy_id] = {"r": [[nokta["lat"], nokta["lng"], 0], [nokta["lat"], nokta["lng"], 0]], "bas": t, "sure": 1, "bit": t + int(sn * 1000), "neden": neden}


def birak(spy_id):
    with _kilit:
        _durum.pop(spy_id, None)


def _yakin(ev, hedef, oran, sapma=400):
    """ev → hedef yolunun oran kadarı, biraz saparak (tam üstüne gitmez)."""
    aci = random.uniform(0, 2 * math.pi)
    m = random.uniform(0, sapma)
    lat = ev[0] + (hedef[0] - ev[0]) * oran + m * math.sin(aci) / 110540
    lng = ev[1] + (hedef[1] - ev[1]) * oran + m * math.cos(aci) / (111320 * math.cos(math.radians(ev[0])))
    return {"lat": lat, "lng": lng}


def _sec(veri, s, bas):
    """Duruma göre (hedef ya da None = yerinde bekle, neden)."""
    from .atama import ayar
    from .yardim import bugun
    i, ev, b = s["id"], (s["lat"], s["lng"]), (bas["lat"], bas["lng"])
    kayit = veri["kayitlar"].values()
    if any(x.get("repId") == i and x.get("durum") == "alindi" and not x.get("sahipsiz") for x in kayit):
        return None, "çağrı teklifine bakıyor"
    bugunku = [x for x in kayit if x.get("repId") == i and x.get("tarih") == bugun() and x.get("durum") not in ("alindi", "iptal")]
    if len(bugunku) >= ayar(veri)["gunlukSinir"]:
        if _m(b, ev) < 300:
            return None, "günlük sınırı doldu"
        return {"lat": ev[0], "lng": ev[1]}, "günü bitti, tabanına dönüyor"
    bekleyen = [x["konum"] for x in kayit if x.get("durum") == "alindi" and x.get("sahipsiz") and not x.get("bolgeDisi") and not x.get("oneri")
                and isinstance(x.get("konum"), dict) and isinstance(x["konum"].get("lat"), (int, float))]
    bekleyen = sorted(((_m(b, (k["lat"], k["lng"])), k) for k in bekleyen), key=lambda y: y[0])
    if bekleyen and 800 < bekleyen[0][0] <= TALEP_M:
        k = bekleyen[0][1]
        return _yakin(b, (k["lat"], k["lng"]), 0.7), "bekleyen çağrıya yaklaşıyor"
    if _m(b, ev) > EV_M * 0.75:
        return _yakin(b, ev, 0.6, 600), "tabanına doğru dönüyor"
    return _hedef(ev, b), "saha ziyareti"


def _planla(veri, s, bas):
    from . import trafik
    from .atama import en_hizli_rota
    h, neden = _sec(veri, s, bas)
    if not h:
        t = simdi()
        return {"r": [[bas["lat"], bas["lng"], 0], [bas["lat"], bas["lng"], 0]], "bas": t, "sure": 1, "bit": t + 10000, "neden": neden}
    c = en_hizli_rota(bas, h)
    if c and c.get("rota"):
        r = trafik.zamanli_rota(c["rota"], en_az_m=60, en_cok=80)
    else:  # yol servisi yoksa düz çizgi, 25 km/s
        r = [[bas["lat"], bas["lng"], 0], [h["lat"], h["lng"], round(_m((bas["lat"], bas["lng"]), (h["lat"], h["lng"])) / (25 / 3.6))]]
    if len(r) < 2:
        return None
    t = simdi()
    sure = int(max(6, r[-1][2] / 60 * HIZ_SN_DK) * 1000)
    durak = int(random.uniform(*DURAK_DK) * HIZ_SN_DK * 1000)
    return {"r": r, "bas": t, "sure": sure, "bit": t + sure + durak, "neden": neden}


def _tur():
    from . import depo
    from .konum import canli_konum, konum_ve_kaynak
    with depo.kilit:
        veri = depo.oku()
    mesgul = {x.get("repId") for x in veri["kayitlar"].values() if x.get("durum") in ("yolda", "gorusme", "gorusmede") or x.get("don")}
    elle = veri.get("elleKonum") or {}
    for s in veri["spyler"].values():
        i = s["id"]
        if not acik(veri, s) or i in mesgul or i in elle or canli_konum(i):
            with _kilit:
                _durum.pop(i, None)
            continue
        with _kilit:
            d = _durum.get(i)
        if d and simdi() < d["bit"]:
            continue
        if d:
            bas = {"lat": d["r"][-1][0], "lng": d["r"][-1][1]}
        else:
            bas = dict(konum_ve_kaynak(veri, s)[0])
        try:
            yeni = _planla(veri, s, bas)
        except (OSError, ValueError, KeyError):
            yeni = None
        if yeni:
            with _kilit:
                _durum[i] = yeni


def baslat():
    def dongu():
        while True:
            try:
                _tur()
            except Exception:  # planlayıcı hiç durmasın; bir sonraki turda yeniden dener
                pass
            time.sleep(TUR_SN)
    threading.Thread(target=dongu, daemon=True).start()
